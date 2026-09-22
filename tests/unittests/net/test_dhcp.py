# This file is part of cloud-init. See LICENSE file for license information.

import os
import signal
from textwrap import dedent

import pytest
import responses

from cloudinit.net.dhcp import (
    InvalidDHCPLeaseFileError,
    IscDhclient,
    NoDHCPLeaseError,
    NoDHCPLeaseInterfaceError,
    NoDHCPLeaseMissingDhclientError,
    Udhcpc,
    maybe_perform_dhcp_discovery,
    networkd_load_leases,
)
from cloudinit.net.ephemeral import EphemeralDHCPv4
from cloudinit.util import ensure_file, subp, write_file
from tests.unittests.helpers import (
    CiTestCase,
    ResponsesTestCase,
    mock,
    populate_dir,
)
from tests.unittests.util import MockDistro

PID_F = "/run/dhclient.pid"
LEASE_F = "/run/dhclient.lease"
DHCLIENT = "/sbin/dhclient"


@pytest.mark.parametrize(
    "server_address,lease_file_content",
    (
        pytest.param(None, None, id="no_server_addr_on_absent_lease_file"),
        pytest.param(None, "", id="no_server_addr_on_empty_lease_file"),
        pytest.param(
            None,
            "lease {\n  fixed-address: 10.1.2.3;\n}\n",
            id="no_server_addr_when_no_server_ident",
        ),
        pytest.param(
            "10.4.5.6",
            "lease {\n fixed-address: 10.1.2.3;\n"
            "  option dhcp-server-identifier 10.4.5.6;\n"
            "  option dhcp-renewal-time 1800;\n}\n",
            id="server_addr_found_when_server_ident_present",
        ),
    ),
)
class TestParseDHCPServerFromLeaseFile:
    def test_find_server_address_when_present(
        self, server_address, lease_file_content, tmp_path
    ):
        """Test that we return None in the case of no file or file contains no
        server address, otherwise return the address.
        """
        lease_file = tmp_path / "dhcp.leases"
        if server_address:
            if lease_file_content:
                lease_file.write_text(lease_file_content)
            assert (
                server_address
                == IscDhclient.parse_dhcp_server_from_lease_file(lease_file)
            )
        else:
            assert not IscDhclient.parse_dhcp_server_from_lease_file(
                lease_file
            )


class TestParseDHCPLeasesFile(CiTestCase):
    def test_parse_empty_lease_file_errors(self):
        """parse_dhcp_lease_file errors when file content is empty."""
        empty_file = self.tmp_path("leases")
        ensure_file(empty_file)
        with self.assertRaises(InvalidDHCPLeaseFileError) as context_manager:
            IscDhclient.parse_dhcp_lease_file(empty_file)
        error = context_manager.exception
        self.assertIn("Cannot parse empty dhcp lease file", str(error))

    def test_parse_malformed_lease_file_content_errors(self):
        """IscDhclient.parse_dhcp_lease_file errors when file content isn't
        dhcp leases.
        """
        non_lease_file = self.tmp_path("leases")
        write_file(non_lease_file, "hi mom.")
        with self.assertRaises(InvalidDHCPLeaseFileError) as context_manager:
            IscDhclient.parse_dhcp_lease_file(non_lease_file)
        error = context_manager.exception
        self.assertIn("Cannot parse dhcp lease file", str(error))

    def test_parse_multiple_leases(self):
        """IscDhclient.parse_dhcp_lease_file returns a list of all leases
        within.
        """
        lease_file = self.tmp_path("leases")
        content = dedent(
            """
            lease {
              interface "wlp3s0";
              fixed-address 192.168.2.74;
              filename "http://192.168.2.50/boot.php?mac=${netX}";
              option subnet-mask 255.255.255.0;
              option routers 192.168.2.1;
              renew 4 2017/07/27 18:02:30;
              expire 5 2017/07/28 07:08:15;
            }
            lease {
              interface "wlp3s0";
              fixed-address 192.168.2.74;
              filename "http://192.168.2.50/boot.php?mac=${netX}";
              option subnet-mask 255.255.255.0;
              option routers 192.168.2.1;
              renew 4 2017/07/27 18:02:30;
              expire 5 2017/07/28 07:08:15;
            }
            """
        )
        lease_file.write_text(content)
        leases = IscDhclient.parse_dhcp_lease_file(lease_file)
        assert len(leases) == 2
        assert leases[0]["interface"] == "wlp3s0"
        assert leases[0]["fixed-address"] == "192.168.2.74"
        assert leases[0]["subnet-mask"] == "255.255.255.0"
        assert leases[0]["routers"] == "192.168.2.1"
        assert leases[0]["renew"] == "4 2017/07/27 18:02:30"
        assert leases[0]["expire"] == "5 2017/07/28 07:08:15"

    @mock.patch("cloudinit.net.dhcp.is_ib_interface", return_value=True)
    @mock.patch("cloudinit.net.dhcp.get_ib_interface_hwaddr")
    @mock.patch("cloudinit.net.dhcp.subp.which", return_value="/sbin/udhcpc")
    @mock.patch("cloudinit.net.dhcp.os.remove")
    @mock.patch("cloudinit.net.dhcp.subp.subp")
    @mock.patch("cloudinit.util.load_json")
    @mock.patch("cloudinit.util.load_file")
    @mock.patch("cloudinit.util.write_file")
    def test_udhcpc_discovery_ib(
        self,
        m_write_file,
        m_load_file,
        m_loadjson,
        m_subp,
        m_remove,
        m_which,
        m_get_ib_interface_hwaddr,
        m_is_ib_interface,
    ):
        """dhcp_discovery runs udcpc and parse the dhcp leases."""
        m_subp.return_value = ("", "")
        m_loadjson.return_value = {
            "interface": "ib0",
            "fixed-address": "192.168.2.74",
            "subnet-mask": "255.255.255.0",
            "routers": "192.168.2.1",
            "static_routes": "10.240.0.1/32 0.0.0.0 0.0.0.0/0 10.240.0.1",
        }
        m_get_ib_interface_hwaddr.return_value = "00:21:28:00:01:cf:4b:01"
        self.assertEqual(
            [
                {
                    "fixed-address": "192.168.2.74",
                    "interface": "ib0",
                    "routers": "192.168.2.1",
                    "static_routes": [
                        ("10.240.0.1/32", "0.0.0.0"),
                        ("0.0.0.0/0", "10.240.0.1"),
                    ],
                    "subnet-mask": "255.255.255.0",
                }
            ],
            Udhcpc().dhcp_discovery("ib0", distro=MockDistro()),
        )
        # Interface was brought up before dhclient called
        m_subp.assert_has_calls(
            [
                mock.call(
                    ["ip", "link", "set", "dev", "ib0", "up"],
                ),
                mock.call(
                    [
                        "/sbin/udhcpc",
                        "-O",
                        "staticroutes",
                        "-i",
                        "ib0",
                        "-s",
                        "/var/tmp/cloud-init/udhcpc_script",
                        "-n",
                        "-q",
                        "-f",
                        "-v",
                        "-x",
                        "0x3d:0021280001cf4b01",
                    ],
                    update_env={
                        "LEASE_FILE": "/var/tmp/cloud-init/ib0.lease.json"
                    },
                    capture=True,
                ),
            ]
        )

