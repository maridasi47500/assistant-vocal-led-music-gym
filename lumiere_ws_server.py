import asyncio
import websockets
import flux_led
import sqlite3

led = flux_led.WifiLedBulb("192.168.1.12")



def get_etapes_from_db(style_name):
    conn = sqlite3.connect("seances.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM effets_lumineux WHERE nom = ?", (style_name,))
    row = cursor.fetchone()
    if not row:
        return []
    effet_id = row[0]
    cursor.execute("""
        SELECT action, r, g, b, brightness, pause
        FROM effet_etapes
        WHERE effet_id = ?
        ORDER BY id ASC
    """, (effet_id,))
    etapes = cursor.fetchall()
    conn.close()
    return etapes

async def effet_lumiere(style):
    etapes = get_etapes_from_db(style)
    for action, r, g, b, brightness, pause in etapes:
        if action == "turn_on":
            led.turnOn()
            if r is not None and g is not None and b is not None:
                led.setRgb(r, g, b, brightness=brightness or 100)
        elif action == "turn_off":
            led.turnOff()
        if pause:
            await asyncio.sleep(pause)


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

