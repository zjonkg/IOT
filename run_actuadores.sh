#!/bin/bash

echo "Iniciando actuadores..."

source entorno-virtual/bin/activate  

cd controller/actuator || { echo "Error: No se pudo acceder a controller/actuator"; exit 1; }

python3 temperature_actuator.py &  
TEMP_PID=$!
echo "Actuador de temperatura iniciado (PID: $TEMP_PID)"

python3 humidity_actuator.py &  
HUMIDITY_PID=$!
echo "Actuador de humedad iniciado (PID: $HUMIDITY_PID)"

python3 luminosity_actuator.py &  
LUMINOSITY_PID=$!
echo "Actuador de luminosidad iniciado (PID: $LUMINOSITY_PID)"

echo "Todos los actuadores están en ejecución."
echo "Para detenerlos, usa: kill $TEMP_PID $HUMIDITY_PID $LUMINOSITY_PID"

wait
