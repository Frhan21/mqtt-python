import paho.mqtt.client as mqtt 
import time 
import random 
import json

broker = 'test.mosquitto.org'
port = 1883
topic = 'sensor/data'

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def connect_mqtt(): 
    client.connect(broker, port)
    print(f'Connected to MQTT broker {broker}:{port}')

def publish_data():
    while True: 
        temp = round(random.uniform(20,35), 2)
        hum = round(random.uniform(40,80), 2)
        
        payload = {
            "temperature": temp,
            "humidity": hum,
            "unit": {
                "temperature": "°C",
                "humidity": "%"
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        json_payload = json.dumps(payload)
        client.publish(topic, json_payload)
        print(f'Published: {json_payload}')
        time.sleep(2)

if __name__ == '__main__': 
    connect_mqtt()
    publish_data()