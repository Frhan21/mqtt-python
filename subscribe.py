import paho.mqtt.client as mqtt 
import json

broker = 'test.mosquitto.org'
port = 1883
topic = 'sensor/data'

def on_connect(client, userdata, flags, rc): 
    if rc == 0: 
        print('Connected to MQTT Broker!')
        client.subscribe(topic)
        print(f'Subscribe to topic : {topic}')
    else: 
        print('Failed to connect, return code %d\n', rc)
        

def on_message(client, userdata, msg): 
    try: 
        payload = json.loads(msg.payload.decode())
        # print(payload)
        temp = payload.get('temperature')
        hum = payload.get('humidity')
        timestamps = payload.get('timestamp')
        
        print(f'[{timestamps}] Temperature : {temp}, Humidity : {hum}')
    
    except json.JSONDecodeError: 
        print("Invalid JSON Received")
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_client():
    client.connect(broker, port)
    client.loop_forever()
    
if __name__ == '__main__': 
    start_client()