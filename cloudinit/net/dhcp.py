# Copyright (C) 2017 Canonical Ltd.
#
# Author: Chad Smith <chad.smith@canonical.com>
#
# This file is part of cloud-init. See LICENSE file for license information.

import abc
import glob
import logging
import os
import re
import signal
import time
from contextlib import suppress
from io import StringIO
from typing import Any, Dict, List, Optional

import configobj

from cloudinit import subp, temp_utils, util
from cloudinit.net import (
    find_fallback_nic,
    get_devicelist,
    get_ib_interface_hwaddr,
    get_interface_mac,
    is_ib_interface,
)

LOG = logging.getLogger(__name__)

NETWORKD_LEASES_DIR = "/run/systemd/netif/leases"
UDHCPC_SCRIPT = """#!/bin/sh
log() {
    echo "udhcpc[$PPID]" "$interface: $2"
}
[ -z "$1" ] && echo "Error: should be called from udhcpc" && exit 1
case $1 in
    bound|renew)
    cat <<JSON > "$LEASE_FILE"
{
    "interface": "$interface",
    "fixed-address": "$ip",
    "subnet-mask": "$subnet",
    "routers": "${router%% *}",
    "static_routes" : "${staticroutes}"
}
JSON
    ;;
    deconfig)
    log err "Not supported"
    exit 1
    ;;
    leasefail | nak)
    log err "configuration failed: $1: $message"
    exit 1
    ;;
    *)
    echo "$0: Unknown udhcpc command: $1" >&2
    exit 1
    ;;
esac
"""


class NoDHCPLeaseError(Exception):
    """Raised when unable to get a DHCP lease."""


class InvalidDHCPLeaseFileError(NoDHCPLeaseError):
    """Raised when parsing an empty or invalid dhclient.lease file.

    Current uses are DataSourceAzure and DataSourceEc2 during ephemeral
    boot to scrape metadata.
    """


class NoDHCPLeaseInterfaceError(NoDHCPLeaseError):
    """Raised when unable to find a viable interface for DHCP."""


class NoDHCPLeaseMissingDhclientError(NoDHCPLeaseError):
    """Raised when unable to find dhclient."""


class NoDHCPLeaseMissingUdhcpcError(NoDHCPLeaseError):
    """Raised when unable to find udhcpc client."""


def select_dhcp_client(distro):
    """distros set priority list, select based on this order which to use

    If the priority dhcp client isn't found, fall back to lower in list.
    """
    for client in distro.dhcp_client_priority:
        try:
            dhcp_client = client()
            LOG.debug("DHCP client selected: %s", client.client_name)
            return dhcp_client
        except (
            NoDHCPLeaseMissingDhclientError,
            NoDHCPLeaseMissingUdhcpcError,
        ):
            LOG.warning("DHCP client not found: %s", client.client_name)
    raise NoDHCPLeaseMissingDhclientError()


def maybe_perform_dhcp_discovery(distro, nic=None, dhcp_log_func=None):
    """Perform dhcp discovery if nic valid and dhclient command exists.

    If the nic is invalid or undiscoverable or dhclient command is not found,
    skip dhcp_discovery and return an empty dict.

    @param nic: Name of the network interface we want to run dhclient on.
    @param dhcp_log_func: A callable accepting the dhclient output and error
        streams.
    @return: A list of dicts representing dhcp options for each lease obtained
        from the dhclient discovery if run, otherwise an empty list is
        returned.
    """
    if nic is None:
        nic = find_fallback_nic()
        if nic is None:
            LOG.debug("Skip dhcp_discovery: Unable to find fallback nic.")
            raise NoDHCPLeaseInterfaceError()
    elif nic not in get_devicelist():
        LOG.debug(
            "Skip dhcp_discovery: nic %s not found in get_devicelist.", nic
        )
        raise NoDHCPLeaseInterfaceError()
    client = select_dhcp_client(distro)
    return client.dhcp_discovery(nic, dhcp_log_func, distro)


def networkd_parse_lease(content):
    """Parse a systemd lease file content as in /run/systemd/netif/leases/

    Parse this (almost) ini style file even though it says:
      # This is private data. Do not parse.

    Simply return a dictionary of key/values."""

    return dict(configobj.ConfigObj(StringIO(content), list_values=False))


def networkd_load_leases(interface):
    """Load the systemd dhcp lease file for the given network interface.

    @param interface: Name of the network interface we want to run dhclient on.
    @raises: InvalidDHCPLeaseFileError on empty or unparseable leasefile
        content.
    """
    try:
        return cls.parse_dhcpcd_lease(
            subp.subp(
                [
                    "dhcpcd",
                    "--dumplease",
                    interface,
                ],
                rcs=[0, 1],
            ).stdout,
            interface,
        )

    except subp.ProcessExecutionError as error:
        LOG.debug(
            "dhclient exited with code: %s stderr: %r stdout: %r",
            error.exit_code,
            error.stderr,
            error.stdout,
        )
        raise NoDHCPLeaseError from error


class Udhcpc(DhcpClient):
    client_name = "udhcpc"

    def __init__(self):
        self.udhcpc_path = subp.which("udhcpc")
        if not self.udhcpc_path:
            LOG.debug("Skip udhcpc configuration: No udhcpc command found.")
            raise NoDHCPLeaseMissingUdhcpcError()

    def dhcp_discovery(
        self,
        interface,
        dhcp_log_func=None,
        distro=None,
    ):
        """Run udhcpc on the interface without scripts or filesystem artifacts.

        @param interface: Name of the network interface on which to run udhcpc.
        @param dhcp_log_func: A callable accepting the udhcpc output and
            error streams.

        @return: A list of dicts of representing the dhcp leases parsed from
            the udhcpc lease file.
        """
        LOG.debug("Performing a dhcp discovery on %s", interface)

        tmp_dir = temp_utils.get_tmp_ancestor(needs_exe=True)
        lease_file = os.path.join(tmp_dir, interface + ".lease.json")
        with suppress(FileNotFoundError):
            os.remove(lease_file)

        # udhcpc needs the interface up to send initial discovery packets
        distro.net_ops.link_up(interface)

        udhcpc_script = os.path.join(tmp_dir, "udhcpc_script")
        util.write_file(udhcpc_script, UDHCPC_SCRIPT, 0o755)

        cmd = [
            self.udhcpc_path,
            "-O",
            "staticroutes",
            "-i",
            interface,
            "-s",
            udhcpc_script,
            "-n",  # Exit if lease is not obtained
            "-q",  # Exit after obtaining lease
            "-f",  # Run in foreground
            "-v",
        ]

        # For INFINIBAND port the dhcpc must be running with
        # client id option. So here we are checking if the interface is
        # INFINIBAND or not. If yes, we are generating the the client-id to be
        # used with the udhcpc
        if is_ib_interface(interface):
            dhcp_client_identifier = get_ib_interface_hwaddr(
                interface, ethernet_format=True
            )
            cmd.extend(
                ["-x", "0x3d:%s" % dhcp_client_identifier.replace(":", "")]
            )
        try:
            out, err = subp.subp(
                cmd, update_env={"LEASE_FILE": lease_file}, capture=True
            )
        except subp.ProcessExecutionError as error:
            LOG.debug(
                "udhcpc exited with code: %s stderr: %r stdout: %r",
                error.exit_code,
                error.stderr,
                error.stdout,
            )
            raise NoDHCPLeaseError from error

        if dhcp_log_func is not None:
            dhcp_log_func(out, err)

        lease_json = util.load_json(util.load_file(lease_file))
        static_routes = lease_json["static_routes"].split()
        if static_routes:
            # format: dest1/mask gw1 ... destn/mask gwn
            lease_json["static_routes"] = [
                i for i in zip(static_routes[::2], static_routes[1::2])
            ]
        return [lease_json]

