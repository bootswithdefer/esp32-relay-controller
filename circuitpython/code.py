import os
import time
import board
import digitalio

# import analogio
import ssl
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_max1704x

topic = os.getenv("MQTT_TOPIC", default="door")

relay = digitalio.DigitalInOut(board.D13)
relay.direction = digitalio.Direction.OUTPUT

# sensor1 = analogio.AnalogIn(board.A0)


# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print(f"Connected to MQTT! Listening for topic changes on {topic}")
    # Subscribe to all changes on the onoff_feed.
    client.subscribe(topic)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT!")


def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print(f"New message on topic {topic}: {message}")
    if message == "on":
        relay.value = True
    elif message == "off":
        relay.value = False
    elif message == "toggle":
        if relay.value is True:
            relay.value = False
        else:
            relay.value = True
        time.sleep(0.5)
        if relay.value is True:
            relay.value = False
        else:
            relay.value = True


print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
)
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

# Battery monitor
monitor = adafruit_max1704x.MAX17048(board.I2C())

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

mqtt_client = MQTT.MQTT(
    broker=os.getenv("MQTT_BROKER"),
    port=os.getenv("MQTT_PORT"),
    username=os.getenv("MQTT_USERNAME"),
    password=os.getenv("MQTT_PASSWORD"),
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to MQTT...")
mqtt_client.connect()

while True:
    try:
        # sensor1_voltage = (sensor1.value * 2.57) / 51000
        # mqtt_client.publish("sensor1_voltage", sensor1_voltage)
        # print(f"sensor1 value {sensor1_voltage}")
        # if sensor1_voltage > 2.85:
        #    print("unobstructed")
        # else:
        #    print("obstructed")

        mqtt_client.publish("battery_voltage", monitor.cell_voltage)
        # print(f"Battery voltage: {monitor.cell_voltage:.2f} Volts")

        mqtt_client.publish("battery_percentage", monitor.cell_percent)
        # print(f"Battery percentage: {monitor.cell_percent:.1f} %")

        # Poll the message queue
        mqtt_client.loop()
        time.sleep(1)
    except Exception:
        print("Error, reconnecting...")
        mqtt_client.reconnect()
