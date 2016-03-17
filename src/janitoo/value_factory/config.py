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

def make_config_string(**kwargs):
    return JNTValueConfigString(**kwargs)

def make_config_password(**kwargs):
    return JNTValueConfigPassword(**kwargs)

def make_config_integer(**kwargs):
    return JNTValueConfigInteger(**kwargs)

def make_config_byte(**kwargs):
    return JNTValueConfigByte(**kwargs)

def make_config_float(**kwargs):
    return JNTValueConfigFloat(**kwargs)

def make_config_boolean(**kwargs):
    return JNTValueConfigBoolean(**kwargs)

def make_config_array(**kwargs):
    return JNTValueConfigArray(**kwargs)

def make_config_list(**kwargs):
    return JNTValueConfigList(**kwargs)

class JNTValueConfigGeneric(JNTValueFactoryEntry):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        get_data_cb = kwargs.pop('get_data_cb', self._get_data)
        set_data_cb = kwargs.pop('set_data_cb', self._set_data)
        cmd_class = kwargs.pop('cmd_class', COMMAND_CONFIGURATION)
        genre = kwargs.pop('genre', 0x03)
        is_readonly = kwargs.pop('is_readonly', False)
        is_writeonly = kwargs.pop('is_writeonly', False)
        JNTValueFactoryEntry.__init__(self,
            get_data_cb=get_data_cb, set_data_cb=set_data_cb,
            cmd_class=COMMAND_CONFIGURATION,
            genre=genre,
            is_readonly=is_readonly, is_writeonly=is_writeonly,
            **kwargs)

    def _set_data(self, node_uuid, index, data):
        """
        """
        if index not in self.instances:
            self.instances[index] = {}
        try:
            if index not in self.instances or self.instances[index] != data:
                self.instances[index]['data'] = data
                self.options.set_option(node_uuid, '%s_%s'%(self.uuid, index), '%s'%data)
        except:
            self.instances[index]['data'] = None
            logger.exception('Exception when writing %s_%s for node %s'%(self.uuid, index, node_uuid))

    #~ def _get_data(self, node_uuid, index):
        #~ """
        #~ """
        #~ if index not in self.instances:
            #~ self.instances[index] = {}
        #~ if 'data' not in self.instances[index]:
            #~ self.instances[index]['data'] = None
        #~ if self.instances[index]['data'] is None:
            #~ try:
                #~ self.instances[index]['data'] = self.options.get_option(node_uuid, '%s_%s'%(self.uuid, index))
            #~ except:
                #~ logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        #~ return self.instances[index]['data']
    def _get_data(self, node_uuid, index):
        """
        """
        if index not in self.instances:
            self.instances[index] = {}
        if 'data' not in self.instances[index]:
            self.instances[index]['data'] = None
        if index == 0:
            i = 0
            stop = False
            while not stop:
                #~ logger.debug('index %s, instances %s'%(i, self.instances))
                if i not in self.instances or 'data' not in self.instances[i] or self.instances[i]['data'] is None:
                    try:
                        #~ print "index, node_uuid", node_uuid, index
                        #~ print "instance", i, self.instances
                        #~ print 'uuid : %s_%s'%(self.uuid, i)
                        data = self.options.get_option(node_uuid, '%s_%s'%(self.uuid, i))
                        #~ print "data2", data
                        if data is not None:
                            if i not in self.instances:
                                self.instances[i] = {}
                            self.instances[i]['data'] = data
                        else:
                            stop = True
                        #~ logger.debug('index %s, instances %s'%(i, self.instances))
                    except:
                        logger.exception('Catched exception when retrieving %s_%s for self.instances : %s'%(self.uuid, i, self.instances))
                        stop = True
                i += 1
        #~ print "last", self.instances[index]['data']
        if self.instances[index]['data'] is None:
            try:
                self.instances[index]['data'] = self.options.get_option(node_uuid, '%s_%s'%(self.uuid, index))
            except:
                logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
                self.instances[index]['data'] = self.default
        return self.instances[index]['data']

class JNTValueConfigString(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_string", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        index = kwargs.pop('index', 0)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x08, **kwargs)

class JNTValueConfigList(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_list", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A string')
        label = kwargs.pop('label', 'String')
        list_items = kwargs.pop('list_items', ['value1', 'value2'])
        index = kwargs.pop('index', 0)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x05, list_items=list_items, **kwargs)

class JNTValueConfigPassword(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_password", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A password')
        label = kwargs.pop('label', 'Password')
        index = kwargs.pop('index', 0)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            index=index, type=0x14, **kwargs)

class JNTValueConfigBoolean(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_boolean", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A boolean')
        label = kwargs.pop('label', 'Bool')
        index = kwargs.pop('index', 0)
        get_data_cb = kwargs.pop('get_data_cb', self._get_data_bool)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb,
            index=index, type=0x01, **kwargs)

    def _get_data_bool(self, node_uuid, index):
        """
        """
        try:
            data = self._get_data(node_uuid, index)
            if data is not None:
                self.instances[index]['data'] = bool(data)
            else:
                self.instances[index]['data'] = None
        except:
            logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        return self.instances[index]['data']

class JNTValueConfigInteger(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_integer", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An integer')
        label = kwargs.pop('label', 'Int')
        index = kwargs.pop('index', 0)
        get_data_cb = kwargs.pop('get_data_cb', self._get_data_integer)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb,
            index=index, type=0x04, **kwargs)

    def _get_data_integer(self, node_uuid, index):
        """
        """
        try:
            data = self._get_data(node_uuid, index)
            if data is not None:
                self.instances[index]['data'] = int(data)
            else:
                self.instances[index]['data'] = None
        except:
            logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        return self.instances[index]['data']

class JNTValueConfigByte(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_byte", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A byte')
        label = kwargs.pop('label', 'Byte')
        index = kwargs.pop('index', 0)
        get_data_cb = kwargs.pop('get_data_cb', self._get_data_byte)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb,
            index=index, type=0x02, **kwargs)

    def _get_data_byte(self, node_uuid, index):
        """
        """
        try:
            data = self._get_data(node_uuid, index)
            if data is not None:
                self.instances[index]['data'] = int(data)
            else:
                self.instances[index]['data'] = None
        except:
            logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        return self.instances[index]['data']

class JNTValueConfigFloat(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_float", **kwargs):
        """
        """
        help = kwargs.pop('help', 'A float')
        label = kwargs.pop('label', 'Float')
        index = kwargs.pop('index', 0)
        get_data_cb = kwargs.pop('get_data_cb', self._get_data_float)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb,
            index=index, type=0x04, **kwargs)

    def _get_data_float(self, node_uuid, index):
        """
        """
        try:
            data = self._get_data(node_uuid, index)
            if data is not None:
                self.instances[index]['data'] = float(data)
            else:
                self.instances[index]['data'] = None
        except:
            logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        return self.instances[index]['data']

class JNTValueConfigArray(JNTValueConfigGeneric):
    def __init__(self, entry_name="config_array", **kwargs):
        """
        """
        help = kwargs.pop('help', 'An array of strings separated by |')
        label = kwargs.pop('label', 'Array')
        index = kwargs.pop('index', 0)
        get_data_cb = kwargs.pop('get_data_cb', self._get_data_list)
        JNTValueConfigGeneric.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb,
            index=index, type=0x16, **kwargs)

    def _get_data_list(self, node_uuid, index):
        """
        """
        try:
            data = self._get_data(node_uuid, index)
            if data is not None:
                self.instances[index]['data'] = data.split('|')
            else:
                self.instances[index]['data'] = None
        except:
            logger.exception('Exception when retrieving %s_%s for node %s'%(self.uuid, index, node_uuid))
        return self.instances[index]['data']
