import asyncio
import websockets
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from process_logic import process_humidity # Importar solo la lógica de humidity

async def humidity_monitor():
    uri = "ws://localhost:8765"  # Cambia la IP si es necesario
    umbral_bajo = 30.0  # Humedad mínima
    umbral_alto = 70.0  # Humedad máxima

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket (Humedad)")

            while True:
                message = await websocket.recv()
                data = message.split(',')

                try:
                    humidity = float(data[1])  # Segunda posición es la humedad
                    print(f"Humedad recibida: {humidity}%")

                    
                    process_humidity(humidity)

                except ValueError:
                    print("Error al procesar la humedad recibida.")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor WebSocket. Asegúrate de que esté en ejecución.")

if __name__ == "__main__":
    asyncio.run(humidity_monitor())
