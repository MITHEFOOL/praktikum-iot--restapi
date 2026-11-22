nama:muhammad ilmi
npm: 241010413
mata kuliah : iot

# REST API Node-RED untuk Sistem IoT

Sistem monitoring dan kontrol IoT: simulator ESP32 (Python) -> Mosquitto (MQTT) -> Node-RED (REST API + WebSocket) -> dashboard web.

## File
- simulasi_esp32.py : simulator sensor (paho-mqtt v2)
- flow_nodered.json : flow Node-RED (import lewat menu Import)
- dashboard.html : dashboard (Chart.js, WebSocket)

## Cara menjalankan
1. Pastikan Mosquitto berjalan (port 1883)
2. node-red, lalu import flow_nodered.json dan Deploy
3. python simulasi_esp32.py
4. Buka dashboard.html

## Catatan
Di settings.js Node-RED, aktifkan httpNodeCors dengan methods "GET,PUT,POST,DELETE,OPTIONS" dan allowedHeaders "Content-Type,X-API-Key".
