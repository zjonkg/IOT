import random
import time
from influxdb_client import Point
from connection_component import InfluxDBConnection

def simulate_luminosity():
    """Simula el envío de datos de luminosidad cada 5 segundos."""
    connection = InfluxDBConnection()
    client = connection.get_client()
    write_api = connection.get_write_api(client)
    
    try:
        while True:
            luminosity = round(random.uniform(0, 1000), 2)  # Luminosidad entre 0 y 1000 lux
            luminosity_point = Point("luminosity_sensor").field("luminosity", luminosity)
            
            write_api.write(bucket=connection.bucket, org=connection.org, record=luminosity_point)
            print(f"Nivel de luminosidad enviado: {luminosity} lux")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulación de luminosidad detenida.")

if __name__ == "__main__":
    simulate_luminosity()
