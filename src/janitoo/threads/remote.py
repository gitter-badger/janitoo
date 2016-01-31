# -*- coding: utf-8 -*-
"""The remote thread

Manage

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

import logging
logger = logging.getLogger(__name__)
import os, sys
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from distutils.dir_util import copy_tree
import shutil
from pkg_resources import get_distribution, DistributionNotFound, resource_filename, Requirement

from janitoo.thread import JNTBusThread, BaseThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_WEB_CONTROLLER = 0x1030
COMMAND_WEB_RESOURCE = 0x1031
COMMAND_DOC_RESOURCE = 0x1032

assert(COMMAND_DESC[COMMAND_WEB_CONTROLLER] == 'COMMAND_WEB_CONTROLLER')
assert(COMMAND_DESC[COMMAND_WEB_RESOURCE] == 'COMMAND_WEB_RESOURCE')
assert(COMMAND_DESC[COMMAND_DOC_RESOURCE] == 'COMMAND_DOC_RESOURCE')
##############################################################


def make_thread(options):
    if get_option_autostart(options, 'remote') == True:
        return RemoteThread(options)
    else:
        return None

def make_remote_node(**kwargs):
    return RemoteComponent(**kwargs)

class RemoteComponent(JNTComponent):
    """ A resource ie /rrd """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'repote.node')
        name = kwargs.pop('name', "Remote node")
        product_name = kwargs.pop('product_name', "Remote node")
        product_type = kwargs.pop('product_type', "Software")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        JNTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                product_name=product_name, product_type=product_type, product_manufacturer="Janitoo", **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)
        self.mqttc = None

    def start(self, mqttc):
        """Start the component.

        """
        JNTComponent.start(self, mqttc)
        return True

    def stop(self):
        """Stop the component.

        """
        JNTComponent.stop(self)
        return True

class RemoteBus(JNTBus):
    """A pseudo-bus
    """
    def __init__(self, , oid='remote', **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, oid=oid, **kwargs)

        uuid="actions"
        self.values[uuid] = self.value_factory['action_list'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The action on the HTTP server',
            label='Actions',
            list_items=['start', 'stop', 'reload'],
            set_data_cb=self.set_action,
            is_writeonly = True,
            cmd_class=COMMAND_WEB_CONTROLLER,
            genre=0x01,
        )

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        #~ print "it's me %s : %s" % (self.values['upsname'].data, self._ups_stats_last)
        if self._server is not None:
            return self._server.is_alive()
        return False

    def set_action(self, node_uuid, index, data):
        """Act on the server
        """
        params = {}
        if data == "start":
            if self.mqttc is not None:
                self.start(self.mqttc)
        elif data == "stop":
            self.stop()
        elif data == "reload":
            if self._server is not None:
                self._server.trigger_reload()

    def start(self, mqttc, trigger_thread_reload_cb=None):
        JNTBus.start(self, mqttc, trigger_thread_reload_cb)
        self._server = HttpServerThread("http_server", self.options.data)
        self._server.config(host=self.values["host"].data, port=self.values["port"].data)
        self._server.start()

    def stop(self):
        if self._server is not None:
            self._server.stop()
            self._server = None
        JNTBus.stop(self)

class RemoteThread(JNTBusThread):
    """The remote thread

    """
    def init_bus(self):
        """Build the bus
        """
        self.section = 'remote'
        self.bus = RemoteBus(options=self.options, product_name="Remote thread")
