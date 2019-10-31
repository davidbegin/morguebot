#!/usr/bin/env python

import time
import json
import asyncio
import websockets


# ToggleMute
# SetCurrentTransition

async def have_fun():
    uri = "ws://localhost:4444"
    async with websockets.connect(uri) as websocket:
        # scene = "Jobs 3 Comps"
        scene = "Coding Fun Terminal"

        source = "Tests Fail - PIP"

        msg = json.dumps({"request-type":"SetSourceRender","scene": scene, "source": source, "render": True, "message-id":"1"})
        # msg = json.dumps({"request-type":"SetSourceRender", "source": source, "render": True, "message-id":"1"})

        await websocket.send(msg)
        time.sleep(0.2)

        # source = "Tests Pass - PIP"
        # msg = json.dumps({"request-type":"SetSourceRender","scene": scene, "source": source, "render": False, "message-id":"2"})
        # await websocket.send(msg)

        # scene = "PiP"
        # msg = json.dumps({"request-type":"SetCurrentScene","scene-name":f"{scene}","message-id":""})
        # await websocket.send(msg)

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(have_fun())
