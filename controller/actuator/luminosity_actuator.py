import asyncio
import websockets
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from process_logic import process_luminosity  # Importar solo la lógica de luminosidad

async def luminosity_monitor():
    uri = "ws://localhost:8765"  # Cambia la IP si es necesario

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket (Luminosidad)")

            while True:
                message = await websocket.recv()
                data = message.split(',')

                try:
                    # Convertir el valor de luminosidad a flotante y procesarlo
                    luminosity = float(data[2])
                    
                    print(f"Luminosidad recibida: {luminosity} lux")
                    
                    process_luminosity(luminosity)
                except ValueError:
                    print("Error al procesar el valor de luminosidad recibido.")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor WebSocket. Asegúrate de que esté en ejecución.")

if __name__ == "__main__":
    asyncio.run(luminosity_monitor())
