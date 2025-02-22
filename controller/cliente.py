import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:8765"  # Cambia la IP al servidor WebSocket

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket")
            try:
                while True:
                    message = await websocket.recv()  # Recibe los datos
                    print(f"Datos recibidos: {message}")

                    # Dividir los datos por la coma
                    try:
                        temperature, humidity, luminosity = message.split(',')

                        # Convertir a los tipos correctos si es necesario
                        temperature = float(temperature)
                        humidity = float(humidity)
                        luminosity = float(luminosity)

                        # Mostrar los datos
                        print(f"Temperatura: {temperature}°C, Humedad: {humidity}%, Luminosidad: {luminosity} lux")

                    except ValueError:
                        print("Error al procesar los datos recibidos. Asegúrate de que los valores estén en el formato correcto.")

            except websockets.exceptions.ConnectionClosed:
                print("Conexión cerrada por el servidor.")
    except ConnectionRefusedError:
        print(f"No se pudo conectar al servidor en {uri}. Asegúrate de que el servidor esté en ejecución.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(receive_data())
