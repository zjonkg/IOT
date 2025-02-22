import asyncio
import websockets
import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "model"))

from connection_component import InfluxDBConnection
from concurrent.futures import ThreadPoolExecutor

async def send_temperature_data(websocket):
    """Envía datos de temperatura en tiempo real a los clientes conectados."""
    connection = InfluxDBConnection()
    client = connection.get_client()
    query_api = connection.get_query_api(client)

    last_timestamp = None

    # Creamos el ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=3)  # Puedes ajustar el número de hilos

    def query_data(query):
        """Ejecutar la consulta de InfluxDB en un hilo separado."""
        return query_api.query_data_frame(query)

    try:
        while True:
            # Definir las consultas
            query_temperature = """
            from(bucket: "jkgh")
                |> range(start: -10s)
                |> filter(fn: (r) => r._measurement == "thermometer" and r._field == "temperature")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            query_humidity = """
            from(bucket: "jkgh")
                |> range(start: -10s)
                |> filter(fn: (r) => r._measurement == "humidity_sensor" and r._field == "humidity")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """
            query_luminosity = """
            from(bucket: "jkgh")
                    |> range(start: -10s)
                    |> filter(fn: (r) => r._measurement == "luminosity_sensor" and r._field == "luminosity")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """

            # Ejecutar las tres consultas en paralelo usando el ThreadPoolExecutor
            table_temperature = await asyncio.to_thread(query_data, query_temperature)
            table_humidity = await asyncio.to_thread(query_data, query_humidity)
            table_luminosity = await asyncio.to_thread(query_data, query_luminosity)

            # Procesar nuevos datos
            if not (table_temperature.empty or table_humidity.empty or table_luminosity.empty):
                df = table_temperature[["_time", "temperature"]].rename(
                    columns={"_time": "Time", "temperature": "Temperature"}
                )
                df2 = table_humidity[["humidity"]].rename(columns={"humidity": "Humidity"})
                df3 = table_luminosity[["luminosity"]].rename(
                    columns={"luminosity": "Luminosity"}
                )
                df["Time"] = pd.to_datetime(df["Time"])
                # Combinar los tres dataframes en uno solo basado en el índice 'Time'
                merged_data = pd.concat(
                    [
                        df.set_index("Time"),
                        df2.set_index(df["Time"]),
                        df3.set_index(df["Time"]),
                    ],
                    axis=1,
                )

                new_data = merged_data[
                    merged_data.index > (last_timestamp or merged_data.index.min())
                ]

                if not new_data.empty:
                    last_timestamp = new_data.index.max()
                    # Enviar datos nuevos a través del WebSocket
                    for _, row in new_data.iterrows():
                        message = (
                            f"{row['Temperature']},{row['Humidity']},{row['Luminosity']}"
                        )
                        await websocket.send(message)

            await asyncio.sleep(5)  # Pausa entre consultas

    except websockets.exceptions.ConnectionClosed:
        print("Conexión cerrada con el cliente.")

# Configurar el servidor WebSocket
async def main():
    server = await websockets.serve(send_temperature_data, "0.0.0.0", 8765)
    print("Servidor WebSocket iniciado en ws://0.0.0.0:8765")
    await server.wait_closed()

    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        print("\nServidor WebSocket detenido correctamente.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente.")
