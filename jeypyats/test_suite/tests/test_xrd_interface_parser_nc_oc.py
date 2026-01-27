#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_xrd_interface_parser_nc_oc.py
# This file is a part of Netalps.fr
#
# Created: 27.01.2026 18:45:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 18:41:57
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.xrd.xrd_interface_parser_nc_oc import get_interface_status_oc


class TestXRDInterfaceParserNCOc(unittest.TestCase):
    """Unit tests for XRD interface parser (NC OC)"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_oc.logger')
    def test_get_interface_status_oc_success(self, mock_logger):
        """Test successful OC interface status retrieval"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                    <interface>
                        <state>
                            <name>GigabitEthernet0/0/0/0</name>
                            <oper-status>UP</oper-status>
                        </state>
                    </interface>
                    <interface>
                        <state>
                            <name>GigabitEthernet0/0/0/1</name>
                            <oper-status>DOWN</oper-status>
                        </state>
                    </interface>
                </interfaces>
            </data>
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_oc(self.mock_device)

        expected = [
            {"name": "GigabitEthernet0/0/0/0", "oper-status": "UP"},
            {"name": "GigabitEthernet0/0/0/1", "oper-status": "DOWN"}
        ]

        self.assertEqual(result, expected)
        self.mock_device.dispatch.assert_called_once()

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_oc.logger')
    def test_get_interface_status_oc_no_data(self, mock_logger):
        """Test OC interface status retrieval with no data"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_oc(self.mock_device)

        self.assertEqual(result, [])

    @patch('jeypyats.parsers.xrd.xrd_interface_parser_nc_oc.logger')
    def test_get_interface_status_oc_not_ok(self, mock_logger):
        """Test OC interface status retrieval when reply is not ok"""
        mock_reply = MagicMock()
        mock_reply.ok = False
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                    <interface>
                        <state>
                            <name>GigabitEthernet0/0/0/0</name>
                            <oper-status>UP</oper-status>
                        </state>
                    </interface>
                </interfaces>
            </data>
        </rpc-reply>"""

        self.mock_device.dispatch.return_value = mock_reply

        result = get_interface_status_oc(self.mock_device)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
