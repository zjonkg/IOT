import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from collections import deque
from pathlib import Path

# Import InfluxDB connection module
sys.path.append(str(Path(__file__).resolve().parent.parent / "model"))

from connection_component import InfluxDBConnection

def get_all_sensor_data():
    """Fetches real-time sensor data from InfluxDB for temperature, humidity, and luminosity."""
    connection = InfluxDBConnection()
    client = connection.get_client()
    query_api = connection.get_query_api(client)

    # Define queries for each measurement
    queries = {
        "Temperature": """
            from(bucket: "jkgh")
            |> range(start: -10m)
            |> filter(fn: (r) => r._measurement == "thermometer" and r._field == "temperature")
        """,
        "Humidity": """
            from(bucket: "jkgh")
            |> range(start: -10m)
            |> filter(fn: (r) => r._measurement == "humidity_sensor" and r._field == "humidity")
        """,
        "Luminosity": """
            from(bucket: "jkgh")
            |> range(start: -10m)
            |> filter(fn: (r) => r._measurement == "luminosity_sensor" and r._field == "luminosity")
        """
    }

    data_frames = {}
    for key, query in queries.items():
        try:
            tables = query_api.query_data_frame(query)

            if isinstance(tables, list):  # Asegurar que devuelve lista de DataFrames
                tables = pd.concat(tables, ignore_index=True) if tables else pd.DataFrame()

            if tables.empty:
                print(f"[⚠️] No data found for {key}")
                data_frames[key] = pd.DataFrame()
                continue

            if "_time" in tables.columns and "_value" in tables.columns:
                df = tables[["_time", "_value"]].rename(columns={"_time": "Time", "_value": key})
                df["Time"] = pd.to_datetime(df["Time"])
                df.set_index("Time", inplace=True)
                data_frames[key] = df
            else:
                print(f"[⚠️] Missing expected columns in {key} data")
                data_frames[key] = pd.DataFrame()
        
        except Exception as e:
            print(f"[❌] Error fetching {key} data: {e}")
            data_frames[key] = pd.DataFrame()

    return data_frames

def update(frame):
    """Updates all three graphs in real time."""
    global ax1, ax2, ax3

    # Fetch data from InfluxDB
    sensor_data = get_all_sensor_data()

    # Clear previous plots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Update Temperature Plot
    if not sensor_data["Temperature"].empty:
        ax1.plot(sensor_data["Temperature"].index, sensor_data["Temperature"]["Temperature"], marker='o', linestyle='-', color='r')
        ax1.set_title("Temperature (°C)")
        ax1.grid(True)

    # Update Humidity Plot
    if not sensor_data["Humidity"].empty:
        ax2.plot(sensor_data["Humidity"].index, sensor_data["Humidity"]["Humidity"], marker='o', linestyle='-', color='b')
        ax2.set_title("Humidity (%)")
        ax2.grid(True)

    # Update Luminosity Plot
    if not sensor_data["Luminosity"].empty:
        ax3.plot(sensor_data["Luminosity"].index, sensor_data["Luminosity"]["Luminosity"], marker='o', linestyle='-', color='g')
        ax3.set_title("Luminosity (lux)")
        ax3.grid(True)

    ax3.set_xlabel("Time")  # Common X-axis label

def plot_realtime_sensors():
    """Creates real-time plots for Temperature, Humidity, and Luminosity."""
    global ax1, ax2, ax3

    # Initialize figure and subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Real-time animation (updates every 5 seconds)
    ani = FuncAnimation(fig, update, interval=5000, cache_frame_data=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_realtime_sensors()
