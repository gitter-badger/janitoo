# -*- coding: utf-8 -*-

"""Unittests for Janitoo-Roomba Server.
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

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon
from janitoo_nosetests.thread import JNTTThreadRun, JNTTThreadRunCommon
from janitoo_nosetests.component import JNTTComponent, JNTTComponentCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo.threads.remote import RemoteBus
from janitoo.value_factory.other import JNTValueRRead, JNTValueRWrite

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DISCOVERY = 0x5000

assert(COMMAND_DESC[COMMAND_DISCOVERY] == 'COMMAND_DISCOVERY')
##############################################################

#~ JNTTThreadRun.skipCITest()
JNTTThreadRun.skipDockerTest()

class TestRemoteThread(JNTTThreadRun, JNTTThreadRunCommon):
    """Test the thread
    """
    thread_name = "remote"
    conf_file = "tests/data/test_remote.conf"

    #~ def test_051_nodeman_started(self):
        #~ timeout = 90
        #~ i = 0
        #~ while i< timeout*10000 and not self.thread.nodeman.is_started:
            #~ time.sleep(0.0001)
            #~ i += 1
        #~ self.assertTrue(self.thread.nodeman.is_started)


    def test_101_values_config(self):
        self.thread.start()
        try:
            timeout = 120
            i = 0
            while i< timeout and not self.thread.nodeman.is_started:
                time.sleep(1)
                i += 1
                #~ print self.thread.nodeman.state
            print self.thread.bus.nodeman.nodes
            print self.thread.bus.nodeman.find_node('node0')
            print self.thread.bus.nodeman.find_node('node1')
            print self.thread.bus.nodeman.find_node('node3')
            print self.thread.bus.nodeman.find_value('node0','user_read').instances
            print self.thread.bus.nodeman.find_value('node1','user_read').instances
            self.assertNotEqual(None, self.thread.bus.nodeman.find_node('node1'))
            self.assertNotEqual(None, self.thread.bus.nodeman.find_node('node0'))
            self.assertNotEqual(None, self.thread.bus.nodeman.find_node('node3'))
            self.assertEqual(2, self.thread.bus.nodeman.find_value('node1','user_read').get_length())
            self.assertEqual(1, self.thread.bus.nodeman.find_value('node0','user_read').get_length())
            self.assertEqual(1, self.thread.bus.nodeman.find_value('node0','user_write').get_length())
            self.assertEqual(3, self.thread.bus.nodeman.find_value('node3','user_read').get_length())
            self.assertEqual(4, len(self.thread.bus.find_components('remote.node')))
            self.assertEqual(4, len(self.thread.bus.find_values('remote.node','user_read')))

            print self.thread.bus.nodeman.find_node('node3')
            print self.thread.bus.nodeman.find_value('node3','user_read').instances
            print self.thread.bus.nodeman.find_value('node3','user_write').instances
            self.assertNotEqual(None, self.thread.bus.nodeman.find_node('node3'))
            rvalue = self.thread.bus.nodeman.find_value('node3','user_read')
            print rvalue.get_value_config()
            self.assertEqual(3, rvalue.get_length())
            self.assertEqual(['ok_syntax_hum','0'], rvalue.get_value_config())
            self.assertEqual(None, rvalue.get_value_config(index=1))
            self.assertEqual(['bad_syntax_hum','0'], rvalue.get_value_config(index=2))
            self.assertEqual(None, rvalue.get_value_config(index=3))
            wvalue = self.thread.bus.nodeman.find_value('node3','user_write')
            print wvalue.get_value_config()
            self.assertEqual(6, wvalue.get_length())
            self.assertEqual(['okswitch','0','0x0025','1','0'], wvalue.get_value_config())
            self.assertEqual(None, wvalue.get_value_config(index=1))
            self.assertEqual(None, wvalue.get_value_config(index=2))
            self.assertEqual(None, wvalue.get_value_config(index=3))
            self.assertEqual(None, wvalue.get_value_config(index=4))
            self.assertEqual(None, wvalue.get_value_config(index=5))
            self.assertEqual(None, wvalue.get_value_config(index=6))

            print self.thread.bus.nodeman.find_node('node0')
            print self.thread.bus.nodeman.find_value('node0','user_read').instances
            print self.thread.bus.nodeman.find_value('node0','user_write').instances
            self.assertNotEqual(None, self.thread.bus.nodeman.find_node('node0'))
            rvalue = self.thread.bus.nodeman.find_value('node0','user_read')
            print rvalue.get_value_config()
            self.assertEqual(1, rvalue.get_length())
            self.assertEqual(['dht_out_hum','0'], rvalue.get_value_config())
            self.assertEqual(None, rvalue.get_value_config(index=1))
            wvalue = self.thread.bus.nodeman.find_value('node0','user_write')
            print wvalue.get_value_config()
            self.assertEqual(1, wvalue.get_length())
            self.assertEqual(['switch','0','0x0025','1','0'], wvalue.get_value_config())
            self.assertEqual(None, wvalue.get_value_config(index=1))
        finally:
            self.thread.stop()
