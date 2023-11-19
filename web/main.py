from nicegui import ui
import requests
import json


def toggle_garage_door(url):
    response = requests.post(
        "https://gdo-api.dotd.com/toggle",
        headers=json.loads("headers.json")
    )
    print(response.status_code)
    print(response.text)


button = ui.button("Door Opener", on_click=toggle_garage_door)

ui.run()
