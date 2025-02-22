import random
import time
from influxdb_client import Point
from connection_component import InfluxDBConnection

def simulate_humidity():
    """Simula el envío de datos de humedad cada 5 segundos."""
    connection = InfluxDBConnection()
    client = connection.get_client()
    write_api = connection.get_write_api(client)
    
    try:
        while True:
            humidity = round(random.uniform(0, 100), 2)  # Humedad entre 0% y 100%
            humidity_point = Point("humidity_sensor").field("humidity", humidity)
            
            write_api.write(bucket=connection.bucket, org=connection.org, record=humidity_point)
            print(f"Humedad enviada: {humidity}%")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulación de humedad detenida.")

if __name__ == "__main__":
    simulate_humidity()
