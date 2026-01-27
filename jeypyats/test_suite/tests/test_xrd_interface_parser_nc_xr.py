#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_xrd_interface_parser_nc_xr.py
# This file is a part of Netalps.fr
#
# Created: 27.01.2026 18:45:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 18:42:12
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.xrd.xrd_interface_parser_nc_xr import get_interface_status_xr


class TestXRDInterfaceParserNCXr(unittest.TestCase):
    """Unit tests for XRD interface parser (NC XR)"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_xr.logger')
    def test_get_interface_status_xr_success(self, mock_logger):
        """Test successful XR interface status retrieval"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
                    <interface-xr>
                        <interface>
                            <interface-name>GigabitEthernet0/0/0/0</interface-name>
                            <state>im-state-up</state>
                        </interface>
                        <interface>
                            <interface-name>GigabitEthernet0/0/0/1</interface-name>
                            <state>im-state-down</state>
                        </interface>
                    </interface-xr>
                </interfaces>
            </data>
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_xr(self.mock_device)

        expected = [
            {"interface-name": "GigabitEthernet0/0/0/0", "state": "im-state-up"},
            {"interface-name": "GigabitEthernet0/0/0/1", "state": "im-state-down"}
        ]

        self.assertEqual(result, expected)
        self.mock_device.dispatch.assert_called_once()

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_xr.logger')
    def test_get_interface_status_xr_no_data(self, mock_logger):
        """Test XR interface status retrieval with no data"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_xr(self.mock_device)

        self.assertEqual(result, [])

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_xr.logger')
    def test_get_interface_status_xr_not_ok(self, mock_logger):
        """Test XR interface status retrieval when reply is not ok"""
        mock_reply = MagicMock()
        mock_reply.ok = False
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
                    <interface-xr>
                        <interface>
                            <interface-name>GigabitEthernet0/0/0/0</interface-name>
                            <state>im-state-up</state>
                        </interface>
                    </interface-xr>
                </interfaces>
            </data>
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_xr(self.mock_device)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
