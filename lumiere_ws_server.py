import asyncio
import websockets
import flux_led

led = flux_led.WifiLedBulb("192.168.1.12")

async def effet_lumiere(style):
    if style == "bleu doux":
        led.setRgb(0, 0, 255)
    elif style == "flash intense":
        for _ in range(5):
            led.turnOn()
            led.setRgb(255, 255, 255, brightness=100)
            await asyncio.sleep(0.2)
            led.turnOff()
            await asyncio.sleep(0.2)
    elif style == "double flash":
        for _ in range(2):
            led.turnOn()
            led.setRgb(255, 255, 0)
            await asyncio.sleep(0.3)
            led.turnOff()
            await asyncio.sleep(0.3)

async def handler(websocket):
    async for message in websocket:
        print(f"💡 Reçu : {message}")
        await effet_lumiere(message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 Serveur WebSocket Lumière lancé sur le port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

