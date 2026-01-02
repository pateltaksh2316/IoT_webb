from django.core.management.base import BaseCommand
import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from django.db import OperationalError
from core.models import MqttLog

SENSOR_TOPIC = "factory/esp32/esp32_0/Tx_model"

# 🔑 RATE LIMIT (seconds)
WRITE_INTERVAL = 60   # 1 minute

# 🔑 In-memory cache
last_written_at = {}


class Command(BaseCommand):
    help = "Run MQTT consumer with rate-limited DB writes"

    def handle(self, *args, **options):
        self.stdout.write("Starting MQTT consumer (rate-limited)...")

        client = mqtt.Client(
            client_id="django-mqtt-consumer",
            clean_session=True
        )

        client.reconnect_delay_set(min_delay=1, max_delay=30)

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
                client.subscribe(SENSOR_TOPIC)
            else:
                print("MQTT connection failed:", rc)

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode())
                now = time.time()
                topic = msg.topic

                last_time = last_written_at.get(topic, 0)

                # 🚦 RATE LIMIT CHECK
                if now - last_time < WRITE_INTERVAL:
                    return  # ❌ Skip DB write

                # ✅ Update last write time
                last_written_at[topic] = now

                # ✅ Write to DB
                MqttLog.objects.create(
                    topic=topic,
                    payload=payload
                )

                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] "
                    f"Saved to DB:", payload
                )

            except json.JSONDecodeError:
                print("Invalid JSON payload")

            except OperationalError:
                print("Database unavailable, skipping write")

            except Exception as e:
                print("Unexpected error:", e)

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("broker.emqx.io", 1883, keepalive=60)
        client.loop_forever()
