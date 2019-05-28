'''
 * Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 * WSO2 Inc. licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
'''

import base64
import json
import threading
import paho.mqtt.client as mqtt
import urllib.request
import ssl
from uuid import uuid4
from datetime import datetime
import time

MQTT_IP = 'emq'
MQTT_PORT = 8883

class Sniffer():
    def __init__(self):
        client = mqtt.Client(client_id=str(uuid4()))
        client.tls_set(ca_certs="digitalfuture_ca_public.pem", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23, ciphers=None)
        client.tls_insecure_set(False)
        client.username_pw_set("kafka", password="56WzM3wW5rA9uZHB")
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        client.connect(MQTT_IP, MQTT_PORT, 60, bind_address="")
        self.client=client
    def __on_connect(self,client, userdata, flags, rc):
        """0: Connection successful 
        1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 
        3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 
        5: Connection refused - not authorised 
        6-255: Currently unused."""
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # If connection successful start publishing data
        if rc == 0:
            self.rc=rc
            client.subscribe("#")
            client.publish("test", json.dumps({"connectivity-test":"ok"}))
    def __on_message(self,client, userdata, msg):
        print("%s message on topic %s: %s" % (str(datetime.now()),str(msg.topic),str(msg.payload)))
    def loop_forever(self):
        self.client.loop_forever()

Sniffer().loop_forever()