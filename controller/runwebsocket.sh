#!/bin/bash

echo "Iniciando websocket..."

source entorno-virtual/bin/activate  

echo "Entorno virtual activado."

python3 WebSocketServer.py &  
WEBSOCKET_PID=$!
echo "WebSocket iniciado (PID: $WEBSOCKET_PID)"

wait  # Mantiene el proceso activo
