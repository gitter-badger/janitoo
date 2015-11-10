# -*- coding: utf-8 -*-
"""The bus

A physical bus : i2c, 1-wire, ...
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
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

import threading
from utils import JanitooNotImplemented, HADD
import uuid as muuid
import ConfigParser
from pkg_resources import iter_entry_points

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+                                   # pragma: no cover
    from logging import NullHandler                   # pragma: no cover
except ImportError:                                   # pragma: no cover
    class NullHandler(logging.Handler):               # pragma: no cover
        """NullHandler logger for python 2.6"""       # pragma: no cover
        def emit(self, record):                       # pragma: no cover
            pass                                      # pragma: no cover
logger = logging.getLogger( __name__ )
from janitoo.node import JNTNode

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_CONTROLLER = 0x1050

assert(COMMAND_DESC[COMMAND_CONTROLLER] == 'COMMAND_CONTROLLER')
##############################################################

class JNTBus(object):
    def __init__(self, oid='generic', **kwargs):
        """Initialise the bus

        :param oid: The oid implemented by the bus.
        :type oid: str
        """
        self.oid = oid
        self.factory = {}
        for entry in iter_entry_points(group='janitoo.components', name=None):
            if entry.name.startswith('%s.'%self.oid):
                self.factory[entry.name] = entry.load()
        self.components = {}
        self.values = {}
        self.cmd_classes = [COMMAND_CONTROLLER]
        self._trigger_thread_reload_cb = None
        self.mqttc = None
        self.options = kwargs.get('options', None)
        """The options"""
        self.product_name = kwargs.get('product_name', 'Default product name')
        """The product name of the node"""
        self.product_type = kwargs.get('product_type', 'Default product type')
        """The product type of the node"""
        self.name = kwargs.get('name', 'Default bus name')
        """The name"""
        self.nodeman = None
        self.value_factory = {}
        for entrypoint in iter_entry_points(group = 'janitoo.values'):
            self.value_factory[entrypoint.name] = entrypoint.load()

    def start(self, mqttc, trigger_thread_reload_cb=None):
        self._trigger_thread_reload_cb = trigger_thread_reload_cb
        self.mqttc = mqttc

    def stop(self):
        for compo in self.components.keys():
            self.components[compo].stop()
        self.components = {}

    @property
    def uuid(self):
        """Return an uuid for the bus. Must be the same as the section name to retrieve the hadd of the controller

        """
        return "%s" % self.oid

    def add_component(self, oid, addr, **kwargs):
        """Return an uuid for the bus

        """
        if addr in self.components:
            return False
        if oid not in self.factory:
            logger.warning("[%s] - Can't find %s in factory", self.__class__.__name__, oid)
            return None
        compo = self.factory[oid](addr=addr, bus=self, **kwargs)
        self.components[addr] = compo
        return compo

    def create_node(self, nodeman, hadd, **kwargs):
        """Create a node associated to this bus
        """
        self.nodeman = nodeman
        name = kwargs.pop('name', "%s controller"%self.name)
        self.node = JNTNode(uuid=self.uuid, cmd_classes=self.cmd_classes, hadd=hadd, name="%s controller"%self.name, product_name=self.product_name, product_type=self.product_type, **kwargs)
        return self.node
