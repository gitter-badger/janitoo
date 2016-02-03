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
from janitoo.value_factory.config import JNTValueConfigString

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_CONFIGURATION = 0x0070
COMMAND_SENSOR_BINARY = 0x0030
COMMAND_SENSOR_MULTILEVEL = 0x0031
COMMAND_BASIC = 0x0020

assert(COMMAND_DESC[COMMAND_BASIC] == 'COMMAND_BASIC')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
assert(COMMAND_DESC[COMMAND_SENSOR_BINARY] == 'COMMAND_SENSOR_BINARY')
assert(COMMAND_DESC[COMMAND_SENSOR_MULTILEVEL] == 'COMMAND_SENSOR_MULTILEVEL')
##############################################################

def make_ip_ping(**kwargs):
    return JNTValueIpPing(**kwargs)

def make_value_rread(**kwargs):
    return JNTValueRRead(**kwargs)

def make_value_rwrite(**kwargs):
    return JNTValueRWrite(**kwargs)

class JNTValueIpPing(JNTValueFactoryEntry):
    """
    """
    def __init__(self, entry_name="ip_ping", **kwargs):
        help = kwargs.pop('help', 'Ping an IP address')
        label = kwargs.pop('label', 'Ping')
        get_data_cb = kwargs.pop('get_data_cb', self.ping_ip)
        index = kwargs.pop('index', 0)
        cmd_class = kwargs.pop('cmd_class', COMMAND_SENSOR_BINARY)
        JNTValueFactoryEntry.__init__(self, entry_name=entry_name, help=help, label=label,
            get_data_cb=get_data_cb, set_data_cb=None,
            index=index, cmd_class=cmd_class, genre=0x02, type=0x01, is_writeonly=False, is_readonly=True, **kwargs)

    def create_config_value(self, **kwargs):
        """
        """
        help = kwargs.pop('help', 'The IP to ping')
        return self._create_config_value(type=0x21, help=help)

    def create_poll_value(self, **kwargs):
        """
        """
        default = kwargs.pop('default', 30)
        return self._create_poll_value(default=default, **kwargs)

    def ping_ip(self, node_uuid=None, index=None):
        """
        """
        try:
            if node_uuid is None:
                node_uuid = self.node_uuid
            if index is None:
                index = self.index
            if index not in self.instances or self.instances[index]['config'] is None:
                logger.warning('[%s] - Pinging an unknown instance %s on node %s', self.__class__.__name__, index, node_uuid)
                return False
            if os.system('ping -c 2 -w 2 ' + self.instances[index]['config'] + '> /dev/null 2>&1'):
                self.instances[index]['data'] = False
                return False
            self.instances[index]['data'] = True
            return True
        except :
            logger.exception('[%s] - Exception when pinging (%s)', self.__class__.__name__, self.instances[index]['config'])
            return False

class JNTValueRRead(JNTValueConfigString):
    """Should be extend to a SensorString + config (as value_factory) to avoid use of get cache, ...
    """
    def __init__(self, entry_name="rread_value", **kwargs):
        help = kwargs.pop('help', 'A read value located on a remote node')
        label = kwargs.pop('label', 'Remote')
        #We will update
        JNTValueConfigString.__init__(self, entry_name=entry_name, help=help, label=label, **kwargs)
        self._cache = {}

    def get_cache(self, node_uuid=None, index=None):
        """
        """
        if index is None:
            index = self.index
        if index in self._cache:
            return self._cache[index]
        return None

    def set_cache(self, node_uuid=None, index=None, data = None):
        """
        """
        if index is None:
            index = self.index
        self._cache[index] = data

    def get_value_config(self, node_uuid=None, index=None):
        """
        conf = switch|0
        """
        try:
            if node_uuid is None:
                node_uuid = self.node_uuid
            if index is None:
                index = self.index
            data = self._get_data(node_uuid, index)
            #~ print data
            if data is None:
                return None
            data = data.split('|')
            #~ print ' length', len(data)
            if len(data) == 1:
                return [ data[0], '0' ]
            if len(data) > 2:
                return None
            return data
        except :
            logger.exception('[%s] - Exception when reading (%s)', self.__class__.__name__, self.instances[index]['data'])
            return None

class JNTValueRWrite(JNTValueConfigString):
    """Should be extend to a SensorString + config (as value_factory) to avoid use of get cache, ...
    """
    def __init__(self, entry_name="rwrite_value", **kwargs):
        help = kwargs.pop('help', 'A write value located on a remote node')
        label = kwargs.pop('label', 'Rwrite')
        #We will update
        JNTValueConfigString.__init__(self, entry_name=entry_name, help=help, label=label, **kwargs)
        self._cache = {}

    def get_cache(self, node_uuid=None, index=None):
        """
        """
        if index is None:
            index = self.index
        if index in self._cache:
            return self._cache[index]
        return None

    def set_cache(self, node_uuid=None, index=None, data = None):
        """
        """
        if index is None:
            index = self.index
        self._cache[index] = data

    def get_value_config(self, node_uuid=None, index=None):
        """
        conf = switch|0|0x0025|1|0
        """
        try:
            if node_uuid is None:
                node_uuid = self.node_uuid
            #~ print "node_uuid ", node_uuid
            if index is None:
                index = self.index
            #~ print "index ", index
            data = self._get_data(node_uuid, index)
            #~ print "data ", data
            if data is None:
                return None
            data = data.split('|')
            #~ print ' length', len(data)
            if len(data) != 5:
                return None
            return data
        except :
            logger.exception('[%s] - Exception when reading (%s)', self.__class__.__name__, self.instances[index]['data'])
            return None
