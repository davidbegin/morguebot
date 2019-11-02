#!/usr/bin/env python

import json
import asyncio
import websockets


async def have_fun():
    uri = "ws://localhost:4444"
    async with websockets.connect(uri) as websocket:

        # Other commands you can run
        # ToggleMute
        # SetCurrentTransition

        scene = "Coding Fun Terminal"

        source = "Tests Fail - PIP"
        msg = json.dumps(
            {
                "request-type": "SetSourceRender",
                "scene": scene,
                "source": source,
                "render": False,
                "message-id": "",
            }
        )
        await websocket.send(msg)

        source = "Tests Pass - PIP"
        msg = json.dumps(
            {
                "request-type": "SetSourceRender",
                "scene": scene,
                "source": source,
                "render": False,
                "message-id": "",
            }
        )
        await websocket.send(msg)

        source = "Deploy Done"
        msg = json.dumps(
            {
                "request-type": "SetSourceRender",
                "scene": scene,
                "source": source,
                "render": False,
                "message-id": "",
            }
        )
        await websocket.send(msg)

        # scene = "PiP"
        # msg = json.dumps({"request-type":"SetCurrentScene","scene-name":f"{scene}","message-id":""})
        # await websocket.send(msg)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(have_fun())
