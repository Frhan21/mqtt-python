import paho.mqtt.client as mqtt 
import json

broker = 'test.mosquitto.org'
port = 1883
topic = 'model/prediction'

client = mqtt.Client()

def connect_mqtt():
    try: 
        client.connect(broker, port)
        print(f'✅ MQTT connected to {broker}:{port}') 
    except Exception as e: 
        print(f'❌ Failed to connect: {e}')

def publish_mqtt(payload: dict):
    """
    Fungsi untuk mengirimkan payload prediksi dalam format JSON ke broker MQTT.
    """
    if not client.is_connected(): 
        connect_mqtt()
    
    try: 
        msg = json.dumps(payload)
        client.publish(topic, msg)
        print(f'✅ Published: {msg}')
        
    except Exception as e:
        print(f'❌ Failed to publish: {e}')