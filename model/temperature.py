import random
import time
from influxdb_client import Point
from connection_component import InfluxDBConnection

def simulate_temperature():
    """Simula el envío de datos de temperatura cada 5 segundos."""
    connection = InfluxDBConnection()
    client = connection.get_client()
    write_api = connection.get_write_api(client)
    
    try:
        while True:
            temperature = round(random.uniform(20, 30), 2)  # Temperatura entre 20 y 30 grados
            temp_point = Point("thermometer").field("temperature", temperature)
            
            write_api.write(bucket=connection.bucket, org=connection.org, record=temp_point)
            print(f"Temperatura enviada: {temperature}°C")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulación de temperatura detenida.")

if __name__ == "__main__":
    simulate_temperature()
