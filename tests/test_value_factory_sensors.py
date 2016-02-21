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

class TestSensorTemperature(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_temperature'

class TestSensorAltitude(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_altitude'

class TestSensorVoltage(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_voltage'

class TestSensorCurrent(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_current'

class TestSensorPercent(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_percent'

class TestSensorFrequency(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_frequency'

class TestSensorHumidity(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_humidity'

class TestSensorPressure(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_pressure'

class TestSensorRotationSpeed(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_rotation_speed'

class TestSensorString(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_string'

class TestSensorFloat(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_float'

class TestSensorList(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_list'

class TestSensorByte(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_byte'

class TestSensorInteger(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_integer'

class TestSensorMemory(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_memory'

class TestSensorOrientation(TestFactory, BasePoll):
    """Test the value factory
    """
    entry_name='sensor_orientation'
