#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_l2vpn_parser.py
# This file is a part of Netalps.fr
#
# Created: 27.01.2026 18:45:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 18:42:19
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock
from jeypyats.parsers.iosxe import ParsersMixin


class TestIOSXEL2VPNParser(unittest.TestCase):
    """Unit tests for IOS-XE L2VPN parser"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    def test_get_l2vpn_bridge_domain_brief_success(self):
        """Test successful L2VPN bridge domain brief retrieval"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
                    <nodes>
                        <node>
                            <node-id>0/RP0/CPU0</node-id>
                            <bridge-domains>
                                <bridge-domain>
                                    <bridge-domain-group-name>BG_IB_MGMT</bridge-domain-group-name>
                                    <bridge-domain-name>BD_IB_MGMT_0001</bridge-domain-name>
                                    <bridge-domain-info>
                                        <bridge-state>bridge-up</bridge-state>
                                    </bridge-domain-info>
                                </bridge-domain>
                                <bridge-domain>
                                    <bridge-domain-group-name>BG_IB_MGMT</bridge-domain-group-name>
                                    <bridge-domain-name>BD_IB_MGMT_0002</bridge-domain-name>
                                    <bridge-domain-info>
                                        <bridge-state>bridge-down</bridge-state>
                                    </bridge-domain-info>
                                </bridge-domain>
                            </bridge-domains>
                        </node>
                    </nodes>
                </l2vpnv2>
            </data>
        </rpc-reply>"""

        self.mock_device.request.return_value = mock_reply

        result = ParsersMixin.get_l2vpn_bridge_domain_brief(self.mock_device)

        expected = {
            "BD_IB_MGMT_0001": {"state": "bridge-up"},
            "BD_IB_MGMT_0002": {"state": "bridge-down"}
        }

        self.assertEqual(result, expected)
        self.mock_device.request.assert_called_once()

    def test_get_l2vpn_bridge_domain_brief_no_reply(self):
        """Test L2VPN bridge domain brief with failed reply"""
        mock_reply = MagicMock()
        mock_reply.ok = False

        self.mock_device.request.return_value = mock_reply

        result = ParsersMixin.get_l2vpn_bridge_domain_brief(self.mock_device)

        self.assertEqual(result, {})
        self.mock_device.request.assert_called_once()

    def test_get_l2vpn_bridge_domain_brief_empty_data(self):
        """Test L2VPN bridge domain brief with empty data"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
            </data>
        </rpc-reply>"""

        self.mock_device.request.return_value = mock_reply

        result = ParsersMixin.get_l2vpn_bridge_domain_brief(self.mock_device)

        self.assertEqual(result, {})
        self.mock_device.request.assert_called_once()

    def test_get_l2vpn_bridge_domain_brief_no_bridge_domains(self):
        """Test L2VPN bridge domain brief with no bridge domains"""
        mock_reply = MagicMock()
        mock_reply.ok = True
        mock_reply.xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
                    <nodes>
                        <node>
                            <node-id>0/RP0/CPU0</node-id>
                            <bridge-domains>
                            </bridge-domains>
                        </node>
                    </nodes>
                </l2vpnv2>
            </data>
        </rpc-reply>"""

        self.mock_device.request.return_value = mock_reply

        result = ParsersMixin.get_l2vpn_bridge_domain_brief(self.mock_device)

        self.assertEqual(result, {})
        self.mock_device.request.assert_called_once()


if __name__ == '__main__':
    unittest.main()
