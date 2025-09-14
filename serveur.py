import asyncio
import websockets
import json
from signals import SIGNALS
from urubugu import Urubugu, MoveException

sockets = {}
abakinyi:list[Urubugu] = []
amazina = []
mode = SIGNALS.KWINJIRA
uwushikiriwe = 0

async def bwira_abandi(id, signal, data):
    for umukinyi in abakinyi.values():
        if umukinyi.websocket.id != id:
            await umukinyi.websocket.send(json.dumps({"signal": signal, "data": data}))

async def kwinjira(websocket, data):
    if mode != SIGNALS.KWINJIRA:
        await websocket.send(json.dumps({"signal": SIGNALS.IKOSA, "insiguro": "urukino ruraremvye"}))
        return
    urubugu = Urubugu(websocket=websocket, abansi=abakinyi, **data.get("urubugu"))
    if urubugu.izina in amazina:
        for umukinyi in abakinyi:
            if umukinyi.izina == data['izina']:
                umukinyi.websocket = websocket
        return
    else:
        await websocket.send(json.dumps({"signal": SIGNALS.KAZE, "abakinyi": abakinyi}))
        abakinyi[urubugu.websocket.id] = urubugu
        amazina.append(urubugu.izina)
        bwira_abandi(SIGNALS.KWINJIRA, str(urubugu))

async def tangura(websocket, data):
    umukinyi = abakinyi[uwushikiriwe]
    if umukinyi.websocket.id != websocket.id:
        await websocket.send(json.dumps({"signal": SIGNALS.IKOSA, "insiguro": "Ntabwo ari urukino rwawe"}))
        return
    else:
        position = data.get("position")
        umukinyi.tangura(position)
        uwushikiriwe = (uwushikiriwe + 1) % len(abakinyi)
        umukinyi = abakinyi[uwushikiriwe]
        umukinyi.websocket.send(json.dumps({"signal": SIGNALS.URASHIKIRIWE}))

CASES = {
    SIGNALS.GUTANGURA: tangura,
    SIGNALS.KWINJIRA: kwinjira,
    SIGNALS.KWUNGURUZA: kwunguruza
}
        
async def handler(websocket):
    try:
        async for message in websocket:
            if websocket.id not in abakinyi:
                kwinjira(websocket, message)
            

    except websockets.exceptions.ConnectionClosedOK:
        print("Connexion fermée proprement", locals())
    except Exception as e:
        print(f"Erreur : {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serveur WebSocket démarré sur ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
