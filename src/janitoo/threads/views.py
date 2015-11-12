# -*- coding: utf-8 -*-
"""The Raspberry http views

A view is a list of values (hadd, uuid, index)
Will be used by UI to show a limited list of values

Examples of views :

 - a fish pond can implement a view,
 - a thermostats
 - a room / location too
 ...


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
import logging
logger = logging.getLogger( __name__ )

import os, sys
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from pkg_resources import get_distribution, DistributionNotFound
from janitoo.thread import JNTBusThread, BaseThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus
from distutils.dir_util import copy_tree
import shutil

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_WEB_CONTROLLER = 0x1030
COMMAND_WEB_RESOURCE = 0x1031

assert(COMMAND_DESC[COMMAND_WEB_CONTROLLER] == 'COMMAND_WEB_CONTROLLER')
assert(COMMAND_DESC[COMMAND_WEB_RESOURCE] == 'COMMAND_WEB_RESOURCE')
##############################################################

DEPLOY_DIRS = ['css', 'images', 'js']

def make_thread(options):
    if get_option_autostart(options, 'http') == True:
        return HttpThread(options)
    else:
        return None

def make_http_resource(**kwargs):
    return HttpResourceComponent(**kwargs)

class ThreadedHTTPHandler(SimpleHTTPRequestHandler):
    """
    """
    pass
#~ class ThreadedHTTPHandler(BaseHTTPRequestHandler):
    #~ """
    #~ """
    #~ pass
    #~ def do_GET(self):
        #~ self.send_response(200)
        #~ self.end_headers()
        #~ message =  threading.currentThread().getName()
        #~ self.wfile.write(message)
        #~ self.wfile.write('\n')
        #~ return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

class HttpServerThread(BaseThread):
    """The Rdd cache thread

    Implement a cache.

    """
    def __init__(self, section, options={}):
        """Initialise the cache thread

        Manage a cache for the rrd.

        A timer in a separated thread will pickle the cache to disk every 30 seconds.

        An other thread will update the rrd every hours

        :param options: The options used to start the worker.
        :type clientid: str
        """
        self.section = section
        BaseThread.__init__(self, options=options)
        self.config_timeout_delay = 1.5
        self.loop_sleep = 0.005
        self.host = "localhost"
        self.port = 8081
        self._server = None

    def config(self, host="localhost", port=8081):
        """
        """
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

    def pre_loop(self):
        """Launch before entering the run loop. The node manager is available.
        """
        dirname='.'
        if 'home_dir' in self.options.data and self.options.data['home_dir'] is not None:
            dirname = self.options.data['home_dir']
        dirname = os.path.join(dirname, 'public')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        #~ os.chdir(dirname)
        self._server = ThreadedHTTPServer((self.host, self.port), ThreadedHTTPHandler)

    def post_loop(self):
        """Launch after finishing the run loop. The node manager is still available.
        """
        pass

    def loop(self):
        """Launch after finishing the run loop. The node manager is still available.
        """
        self._server.serve_forever()

    def config_timeout_callback(self):
        """Called when configuration is finished.
        """
        BaseThread.config_timeout_callback(self)
        if self._server is not None:
            self._server.shutdown()
            self._server = None

    def stop(self):
        """Stop the thread
        """
        BaseThread.stop(self)
        if self._server is not None:
            self._server.shutdown()
            self._server = None

    def run(self):
        """Run the loop
        """
        self._stopevent.clear()
        #~ self.boot()
        self.trigger_reload()
        logger.debug("[%s] - Wait for the thread reload event for initial startup", self.__class__.__name__)
        while not self._reloadevent.isSet() and not self._stopevent.isSet():
            self._reloadevent.wait(0.50)
        logger.debug("[%s] - Entering the thread loop", self.__class__.__name__)
        while not self._stopevent.isSet():
            self._reloadevent.clear()
            try:
                self.pre_loop()
            except:
                logger.exception('[%s] - Exception in pre_loop', self.__class__.__name__)
                self._stopevent.set()
            while not self._reloadevent.isSet() and not self._stopevent.isSet():
                self.loop()
            try:
                self.post_loop()
            except:
                logger.exception('[%s] - Exception in post_loop', self.__class__.__name__)

class HttpBus(JNTBus):
    """A pseudo-bus to manage RRDTools
    """
    def __init__(self, **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, **kwargs)
        self._lock =  threading.Lock()
        self._server = None
        if 'home_dir' in self.options.data and self.options.data['home_dir'] is not None:
            dirname = self.options.data['home_dir']
        directory = os.path.join(dirname, 'public')
        if not os.path.exists(directory):
            os.makedirs(directory)

        uuid="host"
        self.values[uuid] = self.value_factory['config_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The host or IP to use for the server',
            label='Host',
            default='localhost',
        )

        uuid="port"
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The port',
            label='Port',
            default=8081,
        )

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

    def get_resource_path(self):
        """Return the resource path

        """
        return "%s:%s/%%s" % (self.values["host"].data, self.values["port"].data)

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

class HttpResourceComponent(JNTComponent):
    """ A resource ie /rrd """

    def __init__(self, path='generic', bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'http.resource')
        name = kwargs.pop('name', "HTTP resource")
        product_name = kwargs.pop('product_name', "HTTP resource")
        product_type = kwargs.pop('product_type', "Software")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        JNTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                product_name=product_name, product_type=product_type, product_manufacturer="Janitoo", **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)
        self.path = path
        dirname='.'
        if 'home_dir' in self.options.data and self.options.data['home_dir'] is not None:
            dirname = self.options.data['home_dir']
        dirname = os.path.join(dirname, "public")
        dirname = os.path.join(dirname, self.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        for mydir in DEPLOY_DIRS:
            directory2 = os.path.join(dirname, mydir)
            if not os.path.exists(directory2):
                os.makedirs(directory2)
        self.deploy_resource(dirname)

        uuid="resource"
        self.values[uuid] = self.value_factory['sensor_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The http resource: host:port',
            label='Resource',
            get_data_cb=self.get_resource,
            genre=0x01,
            cmd_class=COMMAND_WEB_RESOURCE,
        )
        config_value = self.values[uuid].create_config_value(help='The resource path', label='resource', type=0x08)
        self.values[config_value.uuid] = config_value
        poll_value = self.values[uuid].create_poll_value(default=1800)
        self.values[poll_value.uuid] = poll_value

    def get_resource(self, node_uuid, index):
        """
        """
        #~ print self._bus.get_resource_path() % self.path
        return self._bus.get_resource_path() % self.path

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

    def get_module_dir(self):
        """Needed to publish static files
        """
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),'public', self.path)

    def deploy_resource(self, destination):
        """
        """
        for subdir in DEPLOY_DIRS:
            try:
                copy_tree(os.path.join(self.get_module_dir(),subdir), os.path.join(destination,subdir), preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=0, dry_run=0)
            except:
                logger.exception('[%s] - Exception in deploy_resource', self.__class__.__name__)
        try:
            src_files = os.listdir(os.path.join(self.get_module_dir(),"html"))
            for file_name in src_files:
                try:
                    full_file_name = os.path.join(os.path.join(self.get_module_dir(),"html"), file_name)
                    if (os.path.isfile(full_file_name)):
                        shutil.copy(full_file_name, destination)
                except:
                    logger.exception('[%s] - Exception in deploy_resource', self.__class__.__name__)
        except:
            logger.exception('[%s] - Exception in deploy_resource', self.__class__.__name__)

    def check_heartbeat_file(self, filename):
        """Check that the component is 'available'

        """
        dirname='.'
        if 'home_dir' in self.options.data and self.options.data['home_dir'] is not None:
            dirname = self.options.data['home_dir']
        dirname = os.path.join(dirname, "public", filename)
        return os.path.exists(dirname)

class HttpThread(JNTBusThread):
    """The Http thread

    """
    def init_bus(self):
        """Build the bus
        """
        self.section = 'http'
        self.bus = HttpBus(options=self.options, oid=self.section, product_name="Http server")
