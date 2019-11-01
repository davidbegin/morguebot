#!/usr/bin/env python

import json
import asyncio
import websockets
from optparse import OptionParser

# Other commands you can run
# ToggleMute
# SetCurrentTransition


URI = "ws://localhost:4444"


async def receive_msg():
    async with websockets.connect(URI) as websocket:
        return await websocket.recv()


def get_sources_list():
    scene = "Coding Fun Terminal"

    return json.dumps(
        {"request-type": "GetSourcesList", "scene": scene, "message-id": ""}
    )


async def send_msg(msg):
    async with websockets.connect(URI) as websocket:
        await websocket.send(msg)


def toggle_source(source, render):
    scene = "Coding Fun Terminal"
    # source = "Tests Fail - PIP"

    return json.dumps(
        {
            "request-type": "SetSourceRender",
            "scene": scene,
            "source": source,
            "render": render,
            "message-id": "",
        }
    )


if __name__ == "__main__":
    # parser = OptionParser()
    # parser.add_option("-r", "--render", action="store", type="string", dest="render")
    # (options, args) = parser.parse_args()
    # render = render.lower() == "true"

    scene = "Coding Fun Terminal"

    source = "Tests Pass - PIP"
    msg = toggle_source(source, True)
    asyncio.get_event_loop().run_until_complete(send_msg(msg))

    source = "Tests Fail - PIP"
    msg = toggle_source(source, False)
    asyncio.get_event_loop().run_until_complete(send_msg(msg))
    # msg = asyncio.get_event_loop().run_until_complete(receive_msg())
    # print(msg)
