import os
from collections import namedtuple
from contextlib import ExitStack
from unittest.mock import patch

import pytest

from cloudinit.net.activators import (
    DEFAULT_PRIORITY,
    NAME_TO_ACTIVATOR,
    IfUpDownActivator,
    NetplanActivator,
    NetworkdActivator,
    NetworkManagerActivator,
    NoActivatorException,
    search_activator,
    select_activator,
)
from cloudinit.net.network_state import parse_net_config_data
from cloudinit.safeyaml import load

V1_CONFIG = """\
version: 1
config:
- type: physical
  name: eth0
- type: physical
  name: eth1
"""

V2_CONFIG = """\
version: 2
ethernets:
  eth0:
    dhcp4: true
  eth1:
    dhcp4: true
"""

NETPLAN_CALL_LIST: list = [
    ((["netplan", "apply"],), {}),
]


@pytest.fixture
def available_mocks():
    mocks = namedtuple("Mocks", "m_which, m_file, m_exists")
    with ExitStack() as mocks_context:
        mocks_context.enter_context(
            patch("cloudinit.distros.uses_systemd", return_value=False)
        )
        m_which = mocks_context.enter_context(
            patch("cloudinit.subp.which", return_value=True)
        )
        m_file = mocks_context.enter_context(
            patch("os.path.isfile", return_value=True)
        )
        m_exists = mocks_context.enter_context(
            patch("os.path.exists", return_value=True)
        )
        yield mocks(m_which, m_file, m_exists)


@pytest.fixture
def unavailable_mocks():
    mocks = namedtuple("Mocks", "m_which, m_file, m_exists")
    with ExitStack() as mocks_context:
        mocks_context.enter_context(
            patch("cloudinit.distros.uses_systemd", return_value=False)
        )
        m_which = mocks_context.enter_context(
            patch("cloudinit.subp.which", return_value=False)
        )
        m_file = mocks_context.enter_context(
            patch("os.path.isfile", return_value=False)
        )
        m_exists = mocks_context.enter_context(
            patch("os.path.exists", return_value=False)
        )
        yield mocks(m_which, m_file, m_exists)


class TestSearchAndSelect:
    def test_empty_list(self, available_mocks):
        resp = search_activator(priority=DEFAULT_PRIORITY, target=None)
        assert resp == [NAME_TO_ACTIVATOR[name] for name in DEFAULT_PRIORITY]

        activator = select_activator()
        assert activator == NAME_TO_ACTIVATOR[DEFAULT_PRIORITY[0]]

    def test_priority(self, available_mocks):
        new_order = ["netplan", "network-manager"]
        resp = search_activator(priority=new_order, target=None)
        assert resp == [NAME_TO_ACTIVATOR[name] for name in new_order]

        activator = select_activator(priority=new_order)
        assert activator == NAME_TO_ACTIVATOR[new_order[0]]

    def test_target(self, available_mocks):
        search_activator(priority=DEFAULT_PRIORITY, target="/tmp")
        assert "/tmp" == available_mocks.m_which.call_args[1]["target"]

        select_activator(target="/tmp")
        assert "/tmp" == available_mocks.m_which.call_args[1]["target"]

    @patch(
        "cloudinit.net.activators.IfUpDownActivator.available",
        return_value=False,
    )
    def test_first_not_available(self, m_available, available_mocks):
        resp = search_activator(priority=DEFAULT_PRIORITY, target=None)
        assert resp == [
            NAME_TO_ACTIVATOR[activator] for activator in DEFAULT_PRIORITY[1:]
        ]

        resp = select_activator()
        assert resp == NAME_TO_ACTIVATOR[DEFAULT_PRIORITY[1]]

    def test_priority_not_exist(self, available_mocks):
        with pytest.raises(ValueError):
            search_activator(priority=["spam", "eggs"], target=None)
        with pytest.raises(ValueError):
            select_activator(priority=["spam", "eggs"])

    def test_none_available(self, unavailable_mocks):
        resp = search_activator(priority=DEFAULT_PRIORITY, target=None)
        assert resp == []

        with pytest.raises(NoActivatorException):
            select_activator()


IF_UP_DOWN_AVAI
# ... [truncated] ...
, "eth0"],), {}),
    ((["ip", "link", "set", "down", "eth1"],), {}),
]


@pytest.mark.parametrize(
    "activator, expected_call_list",
    [
        (IfUpDownActivator, IF_UP_DOWN_BRING_DOWN_CALL_LIST),
        (NetplanActivator, NETPLAN_CALL_LIST),
        (NetworkManagerActivator, NETWORK_MANAGER_BRING_DOWN_CALL_LIST),
        (NetworkdActivator, NETWORKD_BRING_DOWN_CALL_LIST),
    ],
)
class TestActivatorsBringDown:
    @patch("cloudinit.subp.subp", return_value=("", ""))
    def test_bring_down_interface(
        self, m_subp, activator, expected_call_list, available_mocks
    ):
        activator.bring_down_interface("eth0")
        assert len(m_subp.call_args_list) == 1
        assert m_subp.call_args_list[0] == expected_call_list[0]


class TestNetworkManagerActivatorBringUp:
    def fake_isfile_no_nmconn(filename):
        return False if filename.endswith(".nmconnection") else True

    @patch("cloudinit.subp.subp", return_value=("", ""))
    @patch(
        "cloudinit.net.network_manager.available_nm_ifcfg_rh",
        return_value=True,
    )
    @patch.object(os.path, "isfile", side_effect=fake_isfile_no_nmconn)
    @patch("os.path.exists", return_value=True)
    def test_bring_up_interface_no_nm_conn(
        self, m_exists, m_isfile, m_plugin, m_subp
    ):
        """
        There is no network manager connection file but ifcfg-rh plugin is
        present and ifcfg interface config files are also present. In this
        case, we should use ifcfg files.
        """
        expected_call_list = [
            (
                (
                    [
                        "nmcli",
                        "connection",
                        "load",
                        "".join(
                            [
                                "/etc/sysconfig/network-scripts/ifcfg-eth0",
                            ]
                        ),
                    ],
                ),
                {},
            ),
            (
                (
                    [
                        "nmcli",
                        "connection",
                        "up",
                        "filename",
                        "".join(
                            [
                                "/etc/sysconfig/network-scripts/ifcfg-eth0",
                            ]
                        ),
                    ],
                ),
                {},
            ),
        ]
        index = 0
        assert NetworkManagerActivator.bring_up_interface("eth0")
        for call in m_subp.call_args_list:
            assert call == expected_call_list[index]
            index += 1

    @patch("cloudinit.subp.subp", return_value=("", ""))
    @patch(
        "cloudinit.net.network_manager.available_nm_ifcfg_rh",
        return_value=False,
    )
    @patch.object(os.path, "isfile", side_effect=fake_isfile_no_nmconn)
    @patch("os.path.exists", return_value=True)
    def test_bring_up_interface_no_plugin_no_nm_conn(
        self, m_exists, m_isfile, m_plugin, m_subp
    ):
        """
        The ifcfg-rh plugin is absent and nmconnection file is also
        not present. In this case, we can't use ifcfg file and the
        interface bring up should fail.
        """
        assert not NetworkManagerActivator.bring_up_interface("eth0")

    @patch("cloudinit.subp.subp", return_value=("", ""))
    @patch(
        "cloudinit.net.network_manager.available_nm_ifcfg_rh",
        return_value=True,
    )
    @patch("os.path.isfile", return_value=False)
    @patch("os.path.exists", return_value=True)
    def test_bring_up_interface_no_conn_file(
        self, m_exists, m_isfile, m_plugin, m_subp
    ):
        """
        Neither network manager connection files are present nor
        ifcfg files are present. Even if ifcfg-rh plugin is present,
        we can not bring up the interface. So bring_up_interface()
        should fail.
        """
        assert not NetworkManagerActivator.bring_up_interface("eth0")

