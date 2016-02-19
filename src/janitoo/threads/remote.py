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
from janitoo.utils import HADD, HADD_SEP, hadd_split
from janitoo.utils import  TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC, TOPIC_HEARTBEAT_NODE

from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus
from janitoo.dhcp import HeartbeatMessage
from janitoo.mqtt import MQTTClient, MQTTBasic

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
    return RemoteNodeComponent(**kwargs)

class RemoteNodeComponent(JNTComponent):
    """ A resource ie /rrd """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'remote.node')
        name = kwargs.pop('name', "Remote node")
        product_name = kwargs.pop('product_name', "Remote node")
        product_type = kwargs.pop('product_type', "Software")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        JNTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                product_name=product_name, product_type=product_type, product_manufacturer="Janitoo", **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)
        self.mqttc_heartbeat = None
        self.mqttc_values = None
        self.state = 'OFFLINE'
        self.remote_hadd = (None,None)
        uuid="remote_hadd"
        self.values[uuid] = self.value_factory['config_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='HADD of the remote node that we will listen to',
            label='rhadd',
            default=None,
        )
        uuid="user_read"
        self.values[uuid] = self.value_factory['rread_value'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The user values to listen to : value_uuid:index',
            label='ruser',
            default=None,
        )
        uuid="user_write"
        self.values[uuid] = self.value_factory['rwrite_value'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The user values to listen to : value_uuid:index',
            label='wuser',
            default=None,
        )
        uuid="basic_read"
        self.values[uuid] = self.value_factory['rread_value'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The basic values to listen to : value_uuid:index',
            label='rbasic',
            default=None,
        )
        uuid="basic_write"
        self.values[uuid] = self.value_factory['rwrite_value'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The basic values to listen to : value_uuid:index',
            label='wbasic',
            default=None,
        )

    def start(self, mqttc):
        """Start the component.
        """
        self.state = 'BOOT'
        JNTComponent.start(self, mqttc)
        hadd = self.values['remote_hadd'].data
        logger.debug("[%s] - Found remote HADD %s for node %s", self.__class__.__name__, hadd, self.node.uuid)
        if hadd is None:
            logger.debug("[%s] - No remote HADD. Exit ...", self.__class__.__name__)
            return False
        self.remote_hadd = hadd_split(hadd)
        if self.remote_hadd[0] is None or self.remote_hadd[1] is None:
            logger.warning("[%s] - Bad remote HADD %s", self.__class__.__name__, hadd)
            return False
        try:
            self.mqttc_heartbeat = MQTTClient(options=self.options.data)
            self.mqttc_heartbeat.connect()
            self.mqttc_heartbeat.subscribe(topic=TOPIC_HEARTBEAT_NODE%(hadd), callback=self.on_heartbeat)
            self.mqttc_heartbeat.start()
        except:
            logger.exception("[%s] - start", self.__class__.__name__)
        values_read = self.get_read_values()
        values_write = self.get_write_values()
        logger.debug("[%s] - found %s values_read", self.__class__.__name__, len(values_read))
        logger.debug("[%s] - found %s values_write", self.__class__.__name__, len(values_write))
        topics = []
        for value in values_read:
            if value[0] == 'user':
                topic=TOPIC_VALUES_USER
            else:
                topic=TOPIC_VALUES_BASIC
            topic = topic%(hadd+'/'+value[1])
            topics.append((topic, 0))
            logger.debug("[%s] - subscribe to %s", self.__class__.__name__, topic)
        if len(topics)>0:
            try:
                self.mqttc_values = MQTTClient(options=self.options.data)
                self.mqttc_values.connect()
                self.mqttc_values.subscribe(topics=topics, callback=self.on_remote_value)
                self.mqttc_values.start()
            except:
                logger.exception("[%s] - start", self.__class__.__name__)

        #~ print max_index
        #~ for index in range(max_index):
            #~ print index
        return True

    def get_read_values(self):
        """Return all the read values.
        """
        values = []
        for which in ['user_read', 'basic_read']:
            nb_instances = self.values[which].get_length()
            for i in range(nb_instances):
                vuuid, vindex = self.values[which].get_value_config(index=i)
                values.append((which.replace('_read',''), vuuid, int(vindex)))
        return values

    def get_write_values(self):
        """Return all the read values.
        """
        values = []
        for which in ['user_write', 'basic_write']:
            nb_instances = self.values[which].get_length()
            for i in range(nb_instances):
                vuuid, vindex, cmdcls, ston, stoff = self.values[which].get_value_config(index=i)
                values.append((which.replace('_write',''), vuuid, int(vindex), cmdcls, ston, stoff))
        return values

    def stop(self):
        """Stop the component.
        """
        if self.mqttc_values is not None:
            try:
                hadd = HADD%(self.remote_hadd[0], self.remote_hadd[1])
                values_read = self.get_read_values()
                topics = []
                for value in values_read:
                    if value[0] == 'user':
                        topic=TOPIC_VALUES_USER
                    else:
                        topic=TOPIC_VALUES_BASIC
                    topic = topic%(HADD%(self.remote_hadd)+'/'+value[1])
                    topics.append(topic)
                logger.debug("[%s] - Unsubscribe to %s", self.__class__.__name__, topics)
                self.mqttc_values.unsubscribe(topics)
                self.mqttc_values.stop()
                if self.mqttc_values.is_alive():
                    self.mqttc_values.join()
                self.mqttc_values = None
            except:
                logger.exception("[%s] - stop", self.__class__.__name__)
        if self.mqttc_heartbeat is not None:
            try:
                hadd = HADD%(self.remote_hadd[0], self.remote_hadd[1])
                logger.debug("[%s] - Unsubscribe to %s", self.__class__.__name__, TOPIC_HEARTBEAT_NODE%(hadd))
                self.mqttc_heartbeat.unsubscribe(topic=TOPIC_HEARTBEAT_NODE%(hadd))
                self.mqttc_heartbeat.stop()
                if self.mqttc_heartbeat.is_alive():
                    self.mqttc_heartbeat.join()
                self.mqttc_heartbeat = None
            except:
                logger.exception("[%s] - stop", self.__class__.__name__)
        JNTComponent.stop(self)
        return True

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        #~ print "it's me %s : %s" % (self.values['upsname'].data, self._ups_stats_last)
        if self.mqttc_heartbeat is not None:
            return self.state
        return False

    def on_heartbeat(self, client, userdata, message):
        """On request

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param message: The message variable is a MQTTMessage that describes all of the message parameters.
        :type message: paho.mqtt.client.MQTTMessage
        """
        hb = HeartbeatMessage(message)
        add_ctrl, add_node, state = hb.get_heartbeat()
        if add_ctrl is None or add_node is None:
            return
        if (add_ctrl == self.remote_hadd[0]) and \
           (add_node == self.remote_hadd[1] or add_node == -1) :
               self.state = state

    def on_remote_value(self, client, userdata, message):
        """On request

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param message: The message variable is a MQTTMessage that describes all of the message parameters.
        :type message: paho.mqtt.client.MQTTMessage
        """
        pass

class RemoteBus(JNTBus):
    """A pseudo-bus
    """
    def __init__(self, oid='remote', **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, oid=oid, **kwargs)

class RemoteThread(JNTBusThread):
    """The remote thread

    """
    def init_bus(self):
        """Build the bus
        """
        self.section = 'remote'
        self.bus = RemoteBus(options=self.options, product_name="Remote thread")
