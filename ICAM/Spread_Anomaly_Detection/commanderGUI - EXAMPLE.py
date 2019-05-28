from Tkinter import *
import json
import paho.mqtt.client as mqtt
import requests
import time

#Broker = "127.0.0.1"
Broker = "10.0.4.201"

pres_topic = "mqtt/car/presentation"

api_url = "http://"+Broker+":5000/car/"


cars = []
cars_buttons = []

r = 2


def on_connect(client, userdata, flags, rc):
    client.subscribe(pres_topic)
    print("GUI. Connected to " + pres_topic + " with result code " + str(rc))


def show_car_on_screen(car, r):
    c = 0

    car_widgets = {}
    car_widgets["lbl_id"] = Label(text=car["car_id"], justify=LEFT)
    car_widgets["lbl_id"].grid(row=r, column=c)

    c += 1
    car_widgets["lbl_speed"] = Label(text="Speed: " + str(car["cur_speed"]))
    car_widgets["lbl_speed"].grid(row=r, column=c)

    c += 1
    car_widgets["lbl_pos"] = Label(text="Pos: " + str(car["cur_pos"]))
    car_widgets["lbl_pos"].grid(row=r, column=c)

    c += 1
    car_widgets["lbl_lap"] = Label(text="Lap: " + str(car["cur_lap"]))
    car_widgets["lbl_lap"].grid(row=r, column=c)

    c += 1
    car_widgets["lbl_batt"] = Label(text="Batt%: " + str(car["battery_level"]))
    car_widgets["lbl_batt"].grid(row=r, column=c)


cars_labels = {}
cars_widgets = {}


def show_car_on_screen_new(car, r):
    c = 0
    car_id = car["car_id"]

    if not (car_id in cars_widgets):
        cars_labels[car_id] = {}
        cars_labels[car_id]["id"] = StringVar()
        cars_labels[car_id]["speed"] = StringVar()
        cars_labels[car_id]["pos"] = StringVar()
        cars_labels[car_id]["lap"] = StringVar()
        cars_labels[car_id]["batt"] = StringVar()

        cars_widgets[car_id] = {}
        cars_widgets[car_id]["lbl_id"] = Label(textvariable=cars_labels[car_id]["id"], justify=LEFT)
        cars_widgets[car_id]["lbl_id"].grid(row=r, column=c)
        c += 1
        cars_widgets[car_id]["lbl_speed"] = Label(textvariable=cars_labels[car_id]["speed"], justify=LEFT)
        cars_widgets[car_id]["lbl_speed"].grid(row=r, column=c)
        c += 1
        cars_widgets[car_id]["lbl_pos"] = Label(textvariable=cars_labels[car_id]["pos"])
        cars_widgets[car_id]["lbl_pos"].grid(row=r, column=c)
        c += 1
        cars_widgets[car_id]["lbl_lap"] = Label(textvariable=cars_labels[car_id]["lap"])
        cars_widgets[car_id]["lbl_lap"].grid(row=r, column=c)
        c += 1
        cars_widgets[car_id]["lbl_batt"] = Label(textvariable=cars_labels[car_id]["batt"])
        cars_widgets[car_id]["lbl_batt"].grid(row=r, column=c)

    cars_labels[car_id]["id"].set(car_id)
    cars_labels[car_id]["speed"].set("Speed: " + str(car["cur_speed"]))
    cars_labels[car_id]["pos"].set("Pos: " + str(car["cur_pos"]))
    cars_labels[car_id]["lap"].set("Lap: " + str(car["cur_lap"]))
    cars_labels[car_id]["batt"].set("Batt%: " + str(car["battery_level"]))


def on_message(client, userdata, msg):
    global r
    print("Received: " + msg.payload)
    if msg.topic == pres_topic:
        r += 1
        car = json.loads(msg.payload)
        cars.insert(0, car)  # insert on top (just for visualization).

        show_car_on_screen_new(car, r)


def change_speed():
    car_id = text_id.get("1.0", 'end-1c')
    cur_speed = text_speed.get("1.0", 'end-1c')
    print("GUI. Changing speed.. ID: " + car_id + "; cur_speed: " + cur_speed)
    requests.post(api_url + car_id, data={"cur_speed": cur_speed})


def find_cars():
    global r
    r = 2
    requests.get(api_url + str(0))
    print("finding executed..")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

#########################
#
#   CREATE THE GUI
#
#########################


root = Tk()

Label(root, text="Change speeds").grid(row=0, column=1, pady=5)

Label(root, text="ID").grid(row=1, column=0, pady=5)
Label(root, text="Speed").grid(row=1, column=1, pady=5)

text_id = Text(root, height=1, width=10)
text_id.grid(row=2, column=0, padx=5, pady=5)

text_speed = Text(root, height=1, width=10)
text_speed.grid(row=2, column=1, padx=5, pady=5)

btn_speed = Button(root)
btn_speed["text"] = "Change"
btn_speed["command"] = change_speed
btn_speed.grid(row=2, column=2, padx=5, pady=5)

#########################################################
#
#   Not efficent: "simple" way to refresh the screen
#
#########################################################

import thread


def refresh():
    while True:
        time.sleep(0.5)
        find_cars()


thread.start_new_thread(refresh, ())

#########################################################
#########################################################


mainloop()
root.destroy()
