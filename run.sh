#!/bin/bash

echo "Iniciando sensores..."


source entorno-virtual/bin/activate  

cd model || { echo "Error: No se pudo acceder a model"; exit 1; }


echo "Entorno virtual activado."

python3 temperature.py &  
TEMP_PID=$!
echo "Sensor de temperatura iniciado (PID: $TEMP_PID)"

python3 humidity.py &  
HUMIDITY_PID=$!
echo "Sensor de humedad iniciado (PID: $HUMIDITY_PID)"

python3 luminosity.py &  
LUMINOSITY_PID=$!
echo "Sensor de luminosidad iniciado (PID: $LUMINOSITY_PID)"

echo "Todos los sensores están en ejecución."
echo "Para detenerlos, usa: kill $TEMP_PID $HUMIDITY_PID $LUMINOSITY_PID"

wait
