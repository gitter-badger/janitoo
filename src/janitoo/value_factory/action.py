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
try:  # Python 2.7+                                   # pragma: no cover
    from logging import NullHandler                   # pragma: no cover
except ImportError:                                   # pragma: no cover
    class NullHandler(logging.Handler):               # pragma: no cover
        """NullHandler logger for python 2.6"""       # pragma: no cover
        def emit(self, record):                       # pragma: no cover
            pass                                      # pragma: no cover
logger = logging.getLogger( __name__ )

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

def make_action_string(**kwargs):
    return JNTValueActionString(**kwargs)

def make_action_byte(**kwargs):
    return JNTValueActionByte(**kwargs)

def make_action_integer(**kwargs):
    return JNTValueActionIntger(**kwargs)

def make_action_list(**kwargs):
    return JNTValueActionList(**kwargs)

class JNTValueActionGeneric(JNTValueFactoryEntry):
    def __init__(self, **kwargs):
        """
        """
        genre = kwargs.pop('genre', 0x02)
        is_readonly = kwargs.pop('is_readonly', False)
        is_writeonly = kwargs.pop('is_writeonly', False)
        JNTValueFactoryEntry.__init__(self,
            genre=genre,
            is_readonly=is_readonly, is_writeonly=is_writeonly,
            **kwargs)

class JNTValueActionString(JNTValueActionGeneric):
    def __init__(self, entry_name="action_string", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x08, **kwargs)

class JNTValueActionByte(JNTValueActionGeneric):
    def __init__(self, entry_name="action_byte", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A byte')
        label = kwargs.pop('label', 'Byte')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x02, **kwargs)

class JNTValueActionIntger(JNTValueActionGeneric):
    def __init__(self, entry_name="action_integer", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An integer')
        label = kwargs.pop('label', 'Integer')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x04, **kwargs)

class JNTValueActionList(JNTValueActionGeneric):
    def __init__(self, entry_name="action_list", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        JNTValueActionGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x05, **kwargs)

