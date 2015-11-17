# -*- coding: utf-8 -*-
"""The mqtt client

Largely inspired from http://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/tree/examples/sub-class.py

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

    Original copyright :
    Copyright (c) 2013 Roger Light <roger@atchoo.org>

    All rights reserved. This program and the accompanying materials
    are made available under the terms of the Eclipse Distribution License v1.0
    which accompanies this distribution.

    The Eclipse Distribution License is available at
    http://www.eclipse.org/org/documents/edl-v10.php.

    Contributors:
     - Roger Light - initial implementation

    This example shows how you can use the MQTT client in a class.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger('janitoo.mqtt')
import threading
import paho.mqtt.client as mqtt
import uuid as muuid

from janitoo.utils import JanitooNotImplemented, HADD, json_dumps

class MQTTClient(threading.Thread):
    def __init__(self, clientid=None, options={}):
        """Initialise the client

        :param clientid: use a specific client id which must be unique on the broker. Use None to let the client generate a random id for you.
        :type clientid: str
        """
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.options = options
        self._mqttc = mqtt.Client(clientid)
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe

    def mqtt_on_connect(self, client, userdata, flags, rc):
        """Called when the broker responds to our connection request.


        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param flags: flags is a dict that contains response flags from the broker:
                      flags['session present'] - this flag is useful for clients that are
                      using clean session set to 0 only. If a client with clean
                      session=0, that reconnects to a broker that it has previously
                      connected to, this flag indicates whether the broker still has the
                      session information for the client. If 1, the session still exists.
        :type flags: dict
        :param rc: the value of rc determines success or not:
                       0: Connection successful
                       1: Connection refused - incorrect protocol version
                       2: Connection refused - invalid client identifier
                       3: Connection refused - server unavailable
                       4: Connection refused - bad username or password
                       5: Connection refused - not authorised
                       6-255: Currently unused.
        :type rc: in
        """
        logger.debug("Connected to broker")
        #print("rc: "+str(rc))
        #raise JanitooNotImplemented('mqtt_on_connect not implemnted')

    def mqtt_on_message(self, client, userdata, message):
        """Called when a message has been received on a
        topic that the client subscribes to.

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param message: The message variable is a MQTTMessage that describes all of the message parameters.
        :type message: paho.mqtt.client.MQTTMessage

        """
        logger.debug("mqtt_on_message topic : %s, qos : %s, payload: %s", message.topic, message.qos, message.payload)
        #print(message.topic+" "+str(message.qos)+" "+str(message.payload))
        #raise JanitooNotImplemented('mqtt_on_message not implemnted')

    def mqtt_on_publish(self, client, userdata, mid):
        """called when a message that was to be sent using the
        publish() call has completed transmission to the broker.

        For messages with QoS levels 1 and 2, this means that the appropriate handshakes have
        completed. For QoS 0, this simply means that the message has left the
        client.
        This callback is important because even if the publish() call returns
        success, it does not always mean that the message has been sent.

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param mid: (Not used) The mid variable matches the mid variable returned from the
                    corresponding publish() call, to allow outgoing messages to be tracked.
        :type mid: unknow

        """
        #print("mid: "+str(mid))
        logger.debug("The message have been published")

    def mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        """called when the broker responds to a subscribe request.

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param mid: (Not used) The mid variable matches the mid variable returned from the
                    corresponding publish() call, to allow outgoing messages to be tracked.
        :type mid: unknow
        :param granted_qos: The granted_qos variable is a list of integers that give the QoS level the broker has granted for each
                            of the different subscription requests..
        :type granted_qos: list()

        """
        #print("Subscribed: "+str(mid)+" "+str(granted_qos))
        logger.debug("The subscription is done")

    def mqtt_on_log(self, client, userdata, level, buff):
        """called when the client has log information. Define to allow debugging.

        :param client: the Client instance that is calling the callback.
        :type client: paho.mqtt.client.Client
        :param userdata: user data of any type and can be set when creating a new client instance or with user_data_set(userdata).
        :type userdata: all
        :param level: The level variable gives the severity of the message
                      and will be one of MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
                      MQTT_LOG_ERR, and MQTT_LOG_DEBUG.
        :type level: int
        :param buff: The message itself.
        :type buff: str

        """
        if level == mqtt.MQTT_LOG_DEBUG:
            logger.debug(buff)
        elif level == mqtt.MQTT_LOG_ERR:
            logger.error(buff)
        elif level == mqtt.MQTT_LOG_WARNING:
            logger.warning(buff)
        elif level == mqtt.MQTT_LOG_NOTICE or level == mqtt.MQTT_LOG_INFO:
            logger.info(buff)

    def remove_topic(self, topic=None):
        """Remove a message callback previously registered with message_callback_add().

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str
        """
        self._mqttc.message_callback_remove(topic)

    def add_topic(self, topic=None, callback=None):
        """Register a message callback for a specific topic.

        Messages that match 'topic' will be passed to 'callback'. Any
        non-matching messages will be passed to the default on_message
        callback.

        Call multiple times with different 'sub' to define multiple topic
        specific callbacks.

        Topic specific callbacks may be removed with message_callback_remove().

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str
        :param callback: the function called when a message arrived.
        :type callback: func
        """
        #mqttc.message_callback_add("$SYS/broker/messages/#", on_message_msgs)
        #mqttc.message_callback_add("$SYS/broker/bytes/#", on_message_bytes)
        self._mqttc.message_callback_add(topic, callback)

    def _username_pw_set(self, username, password=None):
        """Set a username and optionally a password for broker authentication.

        Must be called before connect() to have any effect.
        Requires a broker that supports MQTT v3.1.

        username: The username to authenticate with. Need have no relationship to the client id.
        password: The password to authenticate with. Optional, set to None if not required.
        """
        self._mqttc.username_pw_set(username, password)

    def _connect(self, server='127.0.0.1', port=1883, keepalive=60):
        """Connect to the broker

        :param server: the hostname or IP address of the remote broker.
        :type server: str
        :param port: the network port of the server host to connect to. Defaults to 1883.
                     Note that the default port for MQTT over SSL/TLS is 8883 so if you are using tls_set() the port may need providing manually.
        :type port: int
        :param keepalive: maximum period in seconds allowed between communications with the broker.
                          If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker.
        :type keepalive: int
        """
        logger.info("Connect to %s:%s", server, port)
        self._mqttc.connect(server, port, keepalive)

    def subscribe(self, topic=None, qos=0, callback=None):
        """Subscribe to a topic

        This function may be called in three different ways:

        Simple string and integer
        -------------------------
        e.g. subscribe("my/topic", 2)

        topic: A string specifying the subscription topic to subscribe to.
        qos: The desired quality of service level for the subscription.
             Defaults to 0.

        String and integer tuple
        ------------------------
        e.g. subscribe(("my/topic", 1))

        topic: A tuple of (topic, qos). Both topic and qos must be present in
               the tuple.
        qos: Not used.

        List of string and integer tuples
        ------------------------
        e.g. subscribe([("my/topic", 0), ("another/topic", 2)])

        This allows multiple topic subscriptions in a single SUBSCRIPTION
        command, which is more efficient than using multiple calls to
        subscribe().

        topic: A list of tuple of format (topic, qos). Both topic and qos must
               be present in all of the tuples.
        qos: Not used.

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str
        :param qos: the desired quality of service level for the subscription. Defaults to 0.
        :type qos: int
        :param callback: the function called when a message arrived.
        :type callback: func
        """
        #self._mqttc.subscribe("$SYS/#", 0)
        self._mqttc.on_message = callback
        self._mqttc.subscribe(topic, qos)
        logger.debug("Subscribe to %s", topic)

    def unsubscribe(self, topic):
        """Unsubscribe the client from one or more topics.

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str

        Raises a ValueError if topic is None or has zero string length, or is not a string or list.
        """
        self._mqttc.unsubscribe(topic)

    def subscribe_reply(self, uuid=None, qos=0, callback=None):
        """Subscribe to the reply mechanisme

        :param uuid: An uuid.
        :type uuid: str
        :param qos: the desired quality of service level for the subscription. Defaults to 0.
        :type qos: int
        :param callback: the function called when a message arrived.
        :type callback: func
        """
        if uuid is None:
            uuid = str(muuid.uuid1())
        self.subscribe(topic='/reply/'+uuid, callback=callback)
        return uuid

    def unsubscribe_reply(self, uuid):
        """Unsubscribe the client from one or more topics.

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str

        Raises a ValueError if topic is None or has zero string length, or is not a string or list.
        """
        self.remove_topic(topic='/reply/'+uuid)

    def publish_reply(self, uuid, payload=None, qos=0, retain=False):
        """Publish an uuid reply to clients.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        self.publish(topic="/reply/"+uuid, payload=payload, qos=qos, retain=retain)

    def publish(self, topic, payload=None, qos=0, retain=False):
        """Publish a message on a topic.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param topic: The topic that the message should be published on.
        :type topic: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        self._mqttc.publish(topic, payload, qos, retain)

    def publish_heartbeat(self, add_ctrl, add_node, state='online', qos=0, retain=False):
        """Publish an heartbeat for the node add_ctrl, add_node.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        self.publish(topic="/dhcp/heartbeat/"+HADD%(add_ctrl, add_node), payload=state, qos=qos, retain=retain)

    def publish_heartbeat_controller(self, add_ctrl, state='online', qos=0, retain=False):
        """Publish an heartbeat for the controller add_ctrl and all its nodes.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        msg = {'add_ctrl':add_ctrl, 'add_node':-1}
        self.publish(topic="/dhcp/heartbeat/", payload=json_dumps(msg), qos=qos, retain=retain)

    def publish_heartbeat_msg(self, msg, qos=0, retain=False):
        """Publish an heartbeat message.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        self.publish(topic="/dhcp/heartbeat/", payload=json_dumps(msg), qos=qos, retain=retain)

    def publish_heartbeat_resolv_msg(self, msg, qos=0, retain=False):
        """Publish an heartbeat message.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        self.publish(topic="/resolv/dhcp/heartbeat/", payload=json_dumps(msg), qos=qos, retain=retain)

    def publish_value(self, hadd, value, genre='user', qos=0, retain=False):
        """Publish a value.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        :param uuid: The uuid sent in the request.
        :type uuid: str
        :param payload: The actual message to send. If not given, or set to None a
                        zero length message will be used. Passing an int or float will result
                        in the payload being converted to a string representing that number. If
                        you wish to send a true int/float, use struct.pack() to create the
                        payload you require.
        :type payload: message
        :param qos: The quality of service level to use.
        :type qos: int
        :param retain: If set to true, the message will be set as the "last known good"/retained message for the topic.
        :type retain: bool
        """
        #~ print "publish_value : ", hadd, value, genre
        if genre in ["user", "basic", "config"]:
            #For user values with indexes send all instance
            res = value.to_json_with_indexes()
        else:
            res = value.to_json()
        logger.debug('Publish new value to /value/%s : %s', hadd, res)
        self.publish(topic="/values/%s/%s/%s" % (genre, hadd, value.uuid), payload=res, qos=qos, retain=retain)

    def run(self):
        """Run the loop
        """
        #print "Start run"
        #~ rc = 0
        #~ while rc == 0 and not self._stopevent.isSet():
            #~ #print "Ok"
            #~ rc = self._mqttc.loop_forever()
        while not self._stopevent.isSet():
            self._mqttc.loop(timeout=0.25)
        return 0

    def stop(self):
        """Stop the mqtt thread
        """
        logger.debug("Stop the client")
        self._stopevent.set( )
        self._mqttc.disconnect()

    def connect(self):
        """Connect to the mqtt broker
        """
        logger.info("Start the client")
        if "broker_user" in self.options:
            password = None
            if "broker_password" in self.options:
                password = self.options['broker_password']
            self._username_pw_set(self.options['broker_user'], password)
        server = '127.0.0.1'
        if "broker_ip" in self.options:
            server = self.options['broker_ip']
        #print server
        port = 1883
        if "broker_port" in self.options:
            port = self.options['broker_port']
        keepalive = 60
        if "broker_keepalive" in self.options:
            keepalive = int(self.options['broker_keepalive'])
        self._connect(server=server, port=port, keepalive=keepalive)
