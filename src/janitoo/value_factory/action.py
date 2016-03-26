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
COMMAND_SWITCH_BINARY = 0x0025
COMMAND_SWITCH_MULTILEVEL = 0x0026
COMMAND_BUTTON_BINARY = 0x3000
COMMAND_BUTTON_MULTILEVEL = 0x3001

assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
assert(COMMAND_DESC[COMMAND_SENSOR_BINARY] == 'COMMAND_SENSOR_BINARY')
assert(COMMAND_DESC[COMMAND_SENSOR_MULTILEVEL] == 'COMMAND_SENSOR_MULTILEVEL')
assert(COMMAND_DESC[COMMAND_SWITCH_BINARY] == 'COMMAND_SWITCH_BINARY')
assert(COMMAND_DESC[COMMAND_SWITCH_MULTILEVEL] == 'COMMAND_SWITCH_MULTILEVEL')
assert(COMMAND_DESC[COMMAND_BUTTON_BINARY] == 'COMMAND_BUTTON_BINARY')
assert(COMMAND_DESC[COMMAND_BUTTON_MULTILEVEL] == 'COMMAND_BUTTON_MULTILEVEL')
##############################################################

def make_action_string(**kwargs):
    return JNTValueActionString(**kwargs)

def make_action_byte(**kwargs):
    return JNTValueActionByte(**kwargs)

def make_action_integer(**kwargs):
    return JNTValueActionInteger(**kwargs)

def make_action_boolean(**kwargs):
    return JNTValueActionBoolean(**kwargs)

def make_action_list(**kwargs):
    return JNTValueActionList(**kwargs)

def make_action_switch_binary(**kwargs):
    return JNTValueActionSwitchBinary(**kwargs)

def make_action_switch_multilevel(**kwargs):
    return JNTValueActionSwitchMultilevel(**kwargs)

class JNTValueActionGeneric(JNTValueFactoryEntry):
    def __init__(self, **kwargs):
        """
        """
        genre = kwargs.pop('genre', 0x02)
        is_readonly = kwargs.pop('is_readonly', False)
        is_writeonly = kwargs.pop('is_writeonly', False)
        JNTValueFactoryEntry.__init__(self,
            genre=genre,
            is_readonly=is_readonly,
            is_writeonly=is_writeonly,
            **kwargs)

class JNTValueActionString(JNTValueActionGeneric):
    def __init__(self, entry_name="action_string", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            index=index,
            type=0x08,
            **kwargs)

class JNTValueActionByte(JNTValueActionGeneric):
    def __init__(self, entry_name="action_byte", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A byte')
        label = kwargs.pop('label', 'Byte')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            index=index,
            type=0x02,
            **kwargs)

class JNTValueActionInteger(JNTValueActionGeneric):
    def __init__(self, entry_name="action_integer", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An integer')
        label = kwargs.pop('label', 'Integer')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            index=index,
            type=0x04,
            **kwargs)

class JNTValueActionBoolean(JNTValueActionGeneric):
    def __init__(self, entry_name="action_boolean", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A boolean')
        label = kwargs.pop('label', 'Boolean')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            index=index,
            type=0x04,
            **kwargs)

class JNTValueActionList(JNTValueActionGeneric):
    def __init__(self, entry_name="action_list", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            index=index,
            type=0x05,
            **kwargs)

class JNTValueActionSwitchBinary(JNTValueActionList):
    def __init__(self, entry_name="action_switch_binary", **kwargs):
        """
        """
        label = kwargs.pop('label', 'Switch')
        index = kwargs.pop('index', 0)
        list_items = kwargs.pop('list_items', ['on', 'off'])
        help = kwargs.pop('help', 'A switch. Valid values are : %s'%list_items)
        JNTValueActionList.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            list_items=list_items,
            cmd_class=COMMAND_SWITCH_BINARY,
            index=index,
            **kwargs)

class JNTValueActionSwitchMultilevel(JNTValueActionByte):
    def __init__(self, entry_name="action_switch_multilevel", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A switch multilevel. A byte from 0 to 100')
        label = kwargs.pop('label', 'Switch')
        index = kwargs.pop('index', 0)
        JNTValueActionByte.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            cmd_class=COMMAND_SWITCH_MULTILEVEL,
            index=index,
            **kwargs)

class JNTValueActionButtonBinary(JNTValueActionList):
    def __init__(self, entry_name="action_button_binary", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A button')
        label = kwargs.pop('label', 'Button')
        index = kwargs.pop('index', 0)
        list_items = kwargs.pop('list_items', ['on', 'off'])
        JNTValueActionList.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            list_items=list_items,
            cmd_class=COMMAND_BUTTON_BINARY,
            index=index,
            **kwargs)

class JNTValueActionButtonMultiLevel(JNTValueActionByte):
    def __init__(self, entry_name="action_button_mutlilevel", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A button')
        label = kwargs.pop('label', 'Button')
        index = kwargs.pop('index', 0)
        JNTValueActionByte.__init__(self,
            entry_name=entry_name,
            help=help,
            label=label,
            cmd_class=COMMAND_BUTTON_MULTILEVEL,
            index=index,
            **kwargs)

