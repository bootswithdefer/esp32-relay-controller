# ESP32 Relay Controller with Web interface

## Components
* [Adafruit ESP32-S3 Feather with STEMMA QT / Qwiic](https://www.adafruit.com/product/5323)
* [Adafruit Non-Latching Mini Relay FeatherWing](https://www.adafruit.com/product/2895)
* [CircuitPython](https://circuitpython.org/)
* [NiceGUI](https://nicegui.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Eclipse Mosquitto](https://mosquitto.org/)
* [Cloudflare Zero Trust](https://cloudflare.com)
* Docker
* Ubuntu

## Overview

This project contains the code for an ESP32 based relay controller, used by the author as Garage Door Opener.
It consists of an Adafruit feather with relay board and some Python based web services.
The feather connects to your Wifi and listens for messages on an MQTT broker.
A Linux server with Docker hosts the MQTT broker, a NiceGUI web site, and a FastAPI API service.

NOTE: The Web site and API should be secured, it is not recommended to run these apps directly on the internet as-is.
The author uses Cloudflare Zero Trust for this, but that is out of scope for this project.

The UI is a very simple button in your web browser that toggles the relay:

![image](https://github.com/bootswithdefer/garage-door-opener/assets/415790/8019b9e9-a5fd-4dce-8319-3c3c67fb88b7)

Pressing the button sends an request to the API service.
The API service publishes a message to the MQTT broker.
The feather receives the message and triggers the relay.

## Garage Door Opener notes
It is designed to interact with a garage door opener via a relay so if your garage door opener uses encryption you will have to modify one of it's controllers.
The author soldered wires onto the switch contacts on his wall-mounted opener control.
