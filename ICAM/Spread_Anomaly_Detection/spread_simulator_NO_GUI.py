import json
import paho.mqtt.client as mqtt
from datetime import datetime
import ssl
from collections import OrderedDict
import time
import numpy as np
import datetime

MQTT_IP = 'emq'
MQTT_PORT = 8883

username = "spread_ICAM"
password = "spread_ICAM"
deviceType = "spread_ICAM"
version = "v1"

def on_connect(client, userdata, flags, rc):
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
   # if rc == 0:
    #    client.subscribe(subscribeTopic)
        # self.__send_data_loop()


def on_message(client, userdata, msg):
    print(str(datetime.now()) + " Message Received: " + str(msg.payload))


publishTopic = "%s_%s/%s/events" % (deviceType, version, username)
subscribeTopic = "%s_%s/%s/operations" % (deviceType, version, username)
# se non imposto il client_id non riesce a connettersi!!!!!
client = mqtt.Client(client_id="TentativoRaffo")
client.tls_set(ca_certs="digitalfuture_ca_public.pem", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_SSLv23, ciphers=None)
client.tls_insecure_set(False)
client.username_pw_set(username, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_IP, MQTT_PORT, 60, bind_address="")
client.loop_start()

#Peso in kg del vassoio prelevato (Kg)
kg = 2
#Di quanti mm affonda per ogni kg prelevato (mm)
mm_kg = 1
#Coefficiente di sovraelongazione delle catene
s = 1

interval_time = 60;
i = 0
timestamp = int(time.time())

while(i<100):
    time.sleep(1)
    timestamp += 60  #add a second
    date = datetime.datetime.fromtimestamp(timestamp).isoformat()
    s += 0.01
    spread = np.random.normal(loc=0.708727, scale=0.192176)
    spread = spread*s
    print(timestamp)
    ordered_obj_to_send = OrderedDict([
        ("spread", spread),
        ("timestamp_", timestamp),
        ("date", date)])
    client.publish(publishTopic, json.dumps(ordered_obj_to_send), qos=2)
    i+=1