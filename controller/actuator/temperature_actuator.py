import asyncio
import websockets
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from process_logic import process_temperature  # Importar solo la lógica de temperature

async def temperature_monitor():
    uri = "ws://localhost:8765"  # Cambia la IP si es necesario

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket (Temperatura)")

            while True:
                message = await websocket.recv()  # Recibe los datos
                data = message.split(',')

                try:
                    temperature = float(data[0])  # Primera posición es la temperatura
                    print(f"Temperatura recibida: {temperature}°C")

                    process_temperature(temperature)

                except ValueError:
                    print("Error al procesar la temperatura recibida.")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor WebSocket. Asegúrate de que esté en ejecución.")

if __name__ == "__main__":
    asyncio.run(temperature_monitor())
