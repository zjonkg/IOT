# Umbrales para la lógica de sensores
HUMIDITY_LOW = 30.0
HUMIDITY_HIGH = 70.0
LUMINOSITY_LOW = 100.0
LUMINOSITY_HIGH = 800.0
TEMPERATURE_HIGH = 28.0

def process_humidity(hum):
    """Procesa la humedad y aplica lógica de control."""
    if hum < HUMIDITY_LOW:
        print("💧 Humedad baja. Activando humidificador...")
    elif hum > HUMIDITY_HIGH:
        print("💨 Humedad alta. Activando deshumidificador...")

def process_luminosity(lum):
    """Procesa la luminosidad y aplica lógica de control."""
    if lum < LUMINOSITY_LOW:
        print("💡 Luminosidad baja. Encendiendo luces...")
    elif lum > LUMINOSITY_HIGH:
        print("🌞 Luminosidad alta. Apagando luces...")

def process_temperature(temp):
    """Procesa la temperatura y aplica lógica de control."""
    if temp > TEMPERATURE_HIGH:
        print("🔥 ¡Temperatura alta! Encendiendo aire acondicionado...")
