import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, request

import paho.mqtt.client as mqtt
from datetime import datetime
import ssl
from collections import OrderedDict

app = Flask(__name__)
api = Api(app)


class EMQBroker(Resource):
    def post(self):
        #print(str(request.get_json(force=True)))
        print("request.data" + str(request.data))

        obj = json.loads(request.data)

        ordered_obj_to_send = OrderedDict([
            ("device_id", obj.get("device_id")),
            ("timestamp_", obj.get("timestamp_")),
            ("car_name", obj.get("car_name")),
            ("message_type", obj.get("message_type")),
            ("track_location", obj.get("track_location")),
            ("road_piece", obj.get("road_piece")),
            ("offset", float(obj.get("offset"))),
            ("speed", obj.get("speed")),
            ("clockwise", obj.get("clockwise")),
            ("intersection_code", obj.get("intersection_code")),
            ("is_exiting", obj.get("is_exiting")),
            ("road_piece_prev", obj.get("road_piece_prev")),
            ("trackstyle", obj.get("trackstyle")),
            ("battery_level", obj.get("battery_level")),
            ("delocalized", obj.get("delocalized")),
            ("username_", obj.get("username_"))
        ])




        print("Sending: " + json.dumps(ordered_obj_to_send))
        print("On topic: " + str(publishTopic))
        client.publish(publishTopic, json.dumps(ordered_obj_to_send), qos=2)



MQTT_IP = 'emq'
MQTT_PORT = 8883

username = "anki_user"
password = "anki_nodeps"
deviceType = "ankioverdrive"

username = "simcar_user"
password = "simcar_pass"
deviceType = "simcar_type"

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
    if rc == 0:
        client.subscribe(subscribeTopic)
        # self.__send_data_loop()


def on_message(client, userdata, msg):
    print(str(datetime.now()) + " Message Received: " + str(msg.payload))

api.add_resource(EMQBroker, "/emq")


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
print("ok")
client.loop_start()
#time.sleep(2)

app.run(host='0.0.0.0' , debug=True, port=5001)







