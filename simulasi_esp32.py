"""Simulator ESP32: publish data sensor ke iot/sensor, terima perintah dari iot/kontrol.

Install : pip install "paho-mqtt>=2.0"
Jalankan: python simulasi_esp32.py
"""
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"
INTERVAL = 3  # detik

state = {"lamp": "off"}


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"✗ Gagal terhubung ke broker: {reason_code}")
        return
    print(f"✓ Terhubung ke {BROKER}:{PORT}")
    # Subscribe di sini agar otomatis aktif lagi setelah reconnect
    client.subscribe(TOPIC_KONTROL)
    print(f"✓ Subscribe topik '{TOPIC_KONTROL}'")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"! Terputus dari broker ({reason_code}), mencoba menyambung ulang...")


def on_message(client, userdata, msg):
    raw = msg.payload.decode("utf-8", errors="replace")
    try:
        cmd = json.loads(raw)
        device = cmd.get("device")
        action = cmd.get("action")
    except (json.JSONDecodeError, AttributeError):
        print(f"← Perintah (bukan JSON) di {msg.topic}: {raw}")
        return

    print(f"← Perintah diterima di {msg.topic}: {cmd}")
    if device == "lamp" and action in ("on", "off"):
        state["lamp"] = action
        label = "MENYALA" if action == "on" else "MATI"
        print(f"   💡 Lampu {label}")
    else:
        print(f"   (perintah tidak dikenali: device={device}, action={action})")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ESP32-Simulator")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
except ConnectionRefusedError:
    raise SystemExit("Broker tidak berjalan. Jalankan dulu: mosquitto -v")

client.loop_start()
print("ESP32 Simulator berjalan... Ctrl+C untuk stop")

try:
    while True:
        data = {
            "suhu": round(random.uniform(25.0, 32.0), 1),
            "kelembaban": round(random.uniform(55.0, 80.0), 1),
            "timestamp": datetime.now().isoformat(),
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"→ Publish: {data}")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\nBerhenti.")
finally:
    client.loop_stop()
    client.disconnect()
