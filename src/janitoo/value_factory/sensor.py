# -*- coding: utf-8 -*-
"""The value

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

# Set default logging handler to avoid "No handler found" warnings.
import os
import logging
logger = logging.getLogger(__name__)

from janitoo.classes import GENRE_DESC, VALUE_DESC
from janitoo.utils import json_dumps
from janitoo.value import JNTValue
from janitoo.value_factory import JNTValueFactoryEntry

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_CONFIGURATION = 0x0070
COMMAND_SENSOR_BINARY = 0x0030
COMMAND_SENSOR_MULTILEVEL = 0x0031

assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
assert(COMMAND_DESC[COMMAND_SENSOR_BINARY] == 'COMMAND_SENSOR_BINARY')
assert(COMMAND_DESC[COMMAND_SENSOR_MULTILEVEL] == 'COMMAND_SENSOR_MULTILEVEL')
##############################################################

def make_sensor_temperature(**kwargs):
    return JNTValueSensorTemperature(**kwargs)

def make_sensor_altitude(**kwargs):
    return JNTValueSensorAltitude(**kwargs)

def make_sensor_voltage(**kwargs):
    return JNTValueSensorVoltage(**kwargs)

def make_sensor_current(**kwargs):
    return JNTValueSensorCurrent(**kwargs)

def make_sensor_percent(**kwargs):
    return JNTValueSensorPercent(**kwargs)

def make_sensor_frequency(**kwargs):
    return JNTValueSensorFrequency(**kwargs)

def make_sensor_humidity(**kwargs):
    return JNTValueSensorHumidity(**kwargs)

def make_sensor_rotation_speed(**kwargs):
    return JNTValueSensorRotationSpeed(**kwargs)

def make_sensor_integer(**kwargs):
    return JNTValueSensorInteger(**kwargs)

def make_sensor_byte(**kwargs):
    return JNTValueSensorByte(**kwargs)

def make_sensor_string(**kwargs):
    return JNTValueSensorString(**kwargs)

def make_sensor_list(**kwargs):
    return JNTValueSensorList(**kwargs)

def make_sensor_orientation(**kwargs):
    return JNTValueSensorOrientation(**kwargs)

def make_sensor_memory(**kwargs):
    return JNTValueSensorMemory(**kwargs)

def make_sensor_float(**kwargs):
    return JNTValueSensorFloat(**kwargs)

def make_sensor_pressure(**kwargs):
    return JNTValueSensorPressure(**kwargs)

class JNTValueSensorGeneric(JNTValueFactoryEntry):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        genre = kwargs.pop('genre', 0x02)
        is_readonly = kwargs.pop('is_readonly', True)
        is_writeonly = kwargs.pop('is_writeonly', False)
        JNTValueFactoryEntry.__init__(self,
            genre=genre,
            is_readonly=is_readonly, is_writeonly=is_writeonly,
            **kwargs)

    def create_poll_value(self, **kwargs):
        """
        """
        default = kwargs.pop('default', 30)
        return self._create_poll_value(default=default, **kwargs)

class JNTValueSensorFloat(JNTValueSensorGeneric):
    def __init__(self, entry_name="sensor_float", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A float sensor')
        label = kwargs.pop('label', 'Float')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, cmd_class=cmd_class, type=0x03, **kwargs)

class JNTValueSensorTemperature(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_temperature", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A temperature sensor')
        label = kwargs.pop('label', 'Temp.')
        units = kwargs.pop('units', '°C')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorPressure(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_pressure", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A pressure sensor')
        label = kwargs.pop('label', 'Pressure')
        units = kwargs.pop('units', 'Pa')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorAltitude(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_altitude", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An altitude sensor')
        label = kwargs.pop('label', 'Alt.')
        units = kwargs.pop('units', 'm')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorVoltage(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_voltage", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A voltage sensor')
        label = kwargs.pop('label', 'Voltage')
        units = kwargs.pop('units', 'V')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorCurrent(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_current", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A current sensor')
        label = kwargs.pop('label', 'Current')
        units = kwargs.pop('units', 'A')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorPercent(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_percent", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A percent sensor')
        label = kwargs.pop('label', 'Percentage')
        units = kwargs.pop('units', '%')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorRotationSpeed(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_rotation_speed", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A rotation speed sensor')
        label = kwargs.pop('label', 'Rot. speed')
        units = kwargs.pop('units', 'rpm')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorFrequency(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_frequency", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A frequency sensor')
        label = kwargs.pop('label', 'Frequency')
        units = kwargs.pop('units', 'MHz')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorHumidity(JNTValueSensorFloat):
    def __init__(self, entry_name="sensor_humidity", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An humidity sensor')
        label = kwargs.pop('label', 'humidity')
        units = kwargs.pop('units', '%')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label, units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorString(JNTValueSensorGeneric):
    def __init__(self, entry_name="sensor_string", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string sensor')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, cmd_class=cmd_class, type=0x08, **kwargs)

class JNTValueSensorList(JNTValueSensorGeneric):
    def __init__(self, entry_name="sensor_list", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A list sensor')
        label = kwargs.pop('label', 'List')
        index = kwargs.pop('index', 0)
        list_items = kwargs.pop('list_items', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, cmd_class=cmd_class, type=0x05,
            list_items=list_items,
            **kwargs)

class JNTValueSensorByte(JNTValueSensorGeneric):
    def __init__(self, entry_name="sensor_byte", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A byte sensor')
        label = kwargs.pop('label', 'Byte')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, cmd_class=cmd_class, type=0x02, **kwargs)

class JNTValueSensorInteger(JNTValueSensorGeneric):
    def __init__(self, entry_name="sensor_integer", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An integer sensor')
        label = kwargs.pop('label', 'Integer')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, cmd_class=cmd_class, type=0x04, **kwargs)

class JNTValueSensorMemory(JNTValueSensorInteger):
    def __init__(self, entry_name="sensor_memory", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An memory sensor')
        label = kwargs.pop('label', 'Memory')
        units = kwargs.pop('units', 'Bytes')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            units=units,
            index=index, cmd_class=cmd_class, **kwargs)

class JNTValueSensorOrientation(JNTValueSensorInteger):
    def __init__(self, entry_name="sensor_orientation", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An orientation sensor')
        label = kwargs.pop('label', 'Orientation')
        units = kwargs.pop('units', '°')
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_MULTILEVEL)
        JNTValueSensorGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            units=units,
            index=index, cmd_class=cmd_class, **kwargs)
