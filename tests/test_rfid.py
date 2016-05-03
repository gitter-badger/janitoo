# -*- coding: utf-8 -*-

"""Unittests for RFID.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import sys, os
import time, datetime
import unittest

from janitoo_nosetests import JNTTBase

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC
from janitoo.options import JNTOptions
from janitoo.rfid import RFIDBlock, RFIDBlock01, decode_rfid_block
from janitoo.rfid import RFIDTag, decode_rfid_tag, INVALID_BLOCK

class RFIDCommon():
    """Test RFID
    """
    current_version = 0b00000001

    block_v1 = [
            0b00000001,
            0b00000000,
            0b10000000,
            0b10000000,
            0b00000000,
            0b00000000,
            0b11111111,
            0b11111111,
            0b11111111,
            0b11111111,
            ]
    blocks = {}

    def writer(self, blockid, blockdata):
        """ A fake writer """
        self.blocks[blockid] = blockdata
        return True

    def reader(self, blockid):
        """ A fake reader """
        if blockid in self.blocks:
            return self.blocks[blockid]
        return None

    def test_001_block_current_version(self):
        block = RFIDBlock()
        self.assertEqual(block.version, self.current_version)

    def test_005_block_bad(self):
        block = decode_rfid_block(None)
        self.assertEqual(block, None)
        block = decode_rfid_block([
                0b00000001,
                0b00100000,
                0b10000000,
                0b10000000,
                0b00000000,
                0b00000000,
                0b11111111,
                0b11111111,
                0b11111111,
                0b11111111,
                ])
        self.assertEqual(block, None)
        block = decode_rfid_block(INVALID_BLOCK)
        self.assertEqual(block, None)

    def test_006_block_upgrade(self):
        #We create a v1 message
        block = decode_rfid_block([
                0b00000001,
                0b00000000,
                0b10000000,
                0b10000000,
                0b00000000,
                0b00000000,
                0b11111111,
                0b11111111,
                0b11111111,
                0b11111111,
                ])
        self.assertNotEqual(block, None)
        #We change is to v0
        block.version = 0b00000000
        #We export and upgrade version to current
        export = block.to_bytes( upgrade = True )
        #And reimport it
        block = decode_rfid_block(export)
        #And check
        self.assertNotEqual(block, None)
        self.assertEqual(block.version, self.current_version)
        self.assertEqual(block.key_type, 0b10000000)
        self.assertEqual(block.key_subtype, 0b10000000)

    def test_010_block_decode_rfid_v1(self):
        block = decode_rfid_block([
                0b00000001,
                0b00000000,
                0b10000000,
                0b10000000,
                0b00000000,
                0b00000000,
                0b11111111,
                0b11111111,
                0b11111111,
                0b11111111,
                ])
        self.assertNotEqual(block, None)
        self.assertEqual(block.version, 0b00000001)
        self.assertEqual(block.key_type, 0b10000000)
        self.assertEqual(block.key_subtype, 0b10000000)

    def test_100_tag_v1(self):
        self.blocks = { 0 : self.block_v1, 1 : self.block_v1, 2 : self.block_v1 }
        tag = decode_rfid_tag(self.reader)
        self.assertNotEqual(tag, None)
        self.assertEqual(len(tag.blocks), 3)
        self.assertEqual(tag.blocks[0].version, 0b00000001)
        self.assertEqual(tag.blocks[1].version, 0b00000001)
        self.assertEqual(tag.blocks[2].version, 0b00000001)
        #Get another tag and format it
        tag2 = decode_rfid_tag(self.reader)
        self.assertNotEqual(tag2, None)
        tag2.erase(self.writer)
        #Read it again in another tag
        tag3 = decode_rfid_tag(self.reader)
        self.assertEqual(len(tag3.blocks), 0)
        #Write first tag
        tag.to_writer(self.writer)
        #Read it again in another tag
        tag3 = decode_rfid_tag(self.reader)
        self.assertEqual(len(tag3.blocks), 3)

class TestRFID(JNTTBase, RFIDCommon):
    """Test RFID
    """
    pass
