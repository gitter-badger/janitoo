# -*- coding: utf-8 -*-

"""Unittests for Janitoo-common.
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time
import unittest
import threading
import logging
from pkg_resources import iter_entry_points
import mock
import ConfigParser
from ConfigParser import RawConfigParser

sys.path.insert(0,os.path.dirname(__name__))

from janitoo_nosetests import JNTTBase

from janitoo.runner import Runner, jnt_parse_args
from janitoo.server import JNTServer
from janitoo.options import JNTOptions

from test_value_factory import TestFactory, BasePoll

class TestConfigString(TestFactory):
    """Test the value factory
    """
    entry_name='config_string'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 'A string')

class TestConfigPassword(TestFactory):
    """Test the value factory
    """
    entry_name='config_password'

class TestConfigInteger(TestFactory):
    """Test the value factory
    """
    entry_name='config_integer'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 10)

class TestConfigByte(TestFactory):
    """Test the value factory
    """
    entry_name='config_byte'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 10)

class TestConfigList(TestFactory):
    """Test the value factory
    """
    entry_name='config_list'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 'A string')

class TestConfigArray(TestFactory):
    """Test the value factory
    """
    entry_name='config_array'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 'A string|Another string')

class TestConfigBoolean(TestFactory):
    """Test the value factory
    """
    entry_name='config_boolean'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = True)
        self.assertSetgetConfig(node_uuid=node_uuid, data = False)

class TestConfigFloat(TestFactory):
    """Test the value factory
    """
    entry_name='config_float'

    def test_101_setget_data_config(self):
        node_uuid='test_node'
        self.assertSetgetConfig(node_uuid=node_uuid, data = 18.28)
