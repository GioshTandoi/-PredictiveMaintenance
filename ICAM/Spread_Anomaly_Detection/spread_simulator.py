import json

import paho.mqtt.client as mqtt
from datetime import datetime
import ssl
from collections import OrderedDict
import time

from Tkinter import *



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



#########################
#
#   CREATE THE GUI
#
#########################


root = Tk()

Label(root, text="Spread simulator").grid(row=0, column=1, pady=5)

Label(root, text="Kg").grid(row=1, column=0, pady=5)
text_id = Text(root, height=1, width=10)
text_id.grid(row=1, column=1, padx=5, pady=5)
Label(root, text="Peso in kg del vassoio prelevato (Kg)").grid(row=1, column=2, pady=5)


Label(root, text="mm_kg").grid(row=2, column=0, pady=5)
text_speed = Text(root, height=1, width=10)
text_speed.grid(row=2, column=1, padx=5, pady=5)
Label(root, text="Di quanti mm affonda per ogni kg prelevato (mm)").grid(row=2, column=2, pady=5)

Label(root, text="s").grid(row=3, column=0, pady=5)
text_speed = Text(root, height=1, width=10)
text_speed.grid(row=3, column=1, padx=5, pady=5)
Label(root, text="Coefficiente di sovraelongazione delle catene").grid(row=3, column=2, pady=5)

Label(root, text="interval").grid(row=4, column=0, pady=5)
text_speed = Text(root, height=1, width=10)
text_speed.grid(row=4, column=1, padx=5, pady=5)
Label(root, text="Intervallo di invio dati (s)").grid(row=4, column=2, pady=5)

btn_start = Button(root)
btn_start["text"] = "Start"
btn_start.grid(row=5, column=1, padx=5, pady=5)



interval_time = 1000;

def task():


    print("hello")
    root.after(interval_time, task)  # reschedule event in 2 seconds

root.after(interval_time, task)

root.mainloop()
root.destroy()


i=0
timestamp = 1234567890123
while(True):


    time.sleep(1)
    timestamp += i
    print(timestamp)

    ordered_obj_to_send = OrderedDict([
        ("spread", 3.0),
        ("timestamp_", timestamp),
        ("date", "eee")])
    client.publish(publishTopic, json.dumps(ordered_obj_to_send), qos=2)
    i+=1
#time.sleep(2)






