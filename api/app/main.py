import os
from fastapi import FastAPI
import paho.mqtt.client as mqtt

app = FastAPI(title="GDO API")

MQTT_BROKER_ADDRESS = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT", default=1883)
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", default="door")


def toggle_door():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT, 5)
    client.publish(MQTT_TOPIC, "toggle")
    client.disconnect()


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/toggle")
def post_toggle():
    toggle_door()
    return {"state": "toggled"}
