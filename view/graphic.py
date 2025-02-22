import asyncio
import websockets
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque

data_buffer = deque(maxlen=100)  # Almacena los últimos 100 datos

def plot_live():
    plt.ion()
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)  # Tres gráficos en una columna
    ax1, ax2, ax3 = axes  # Desempaquetamos los ejes

    while True:
        if data_buffer:
            df = pd.DataFrame(data_buffer, columns=["Time", "Temperature", "Humidity", "Luminosity"])
            df.set_index("Time", inplace=True)

            # Limpiar gráficos
            ax1.clear()
            ax2.clear()
            ax3.clear()

            # Gráfico de Temperatura
            ax1.set_title("Temperatura")
            ax1.set_ylabel("°C")
            ax1.plot(df.index, df["Temperature"], color='tab:red', label="Temperatura")
            ax1.legend(loc="upper left")

            # Gráfico de Humedad
            ax2.set_title("Humedad")
            ax2.set_ylabel("%")
            ax2.plot(df.index, df["Humidity"], color='tab:blue', label="Humedad")
            ax2.legend(loc="upper left")

            # Gráfico de Luminosidad
            ax3.set_title("Luminosidad")
            ax3.set_ylabel("lux")
            ax3.set_xlabel("Tiempo")
            ax3.plot(df.index, df["Luminosity"], color='tab:green', label="Luminosidad")
            ax3.legend(loc="upper left")

            plt.tight_layout()
            plt.pause(1)

def process_message(message):
    """ Procesa los datos recibidos y los almacena en el buffer """
    try:
        temp, hum, lum = map(float, message.split(","))
        data_buffer.append([pd.Timestamp.now(), temp, hum, lum])
    except ValueError:
        print("Error al procesar el mensaje recibido")

async def receive_data():
    uri = "ws://0.0.0.0:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            process_message(message)

async def main():
    await asyncio.gather(receive_data(), asyncio.to_thread(plot_live))

if __name__ == "__main__":
    asyncio.run(main())
