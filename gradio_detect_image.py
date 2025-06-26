import gradio as gr
from ultralytics import YOLO 
import time
from mqtt_publish import publish_mqtt, connect_mqtt


# Load model 
model = YOLO('model/yolo11n.pt')

def detect_image(image):
    res = model.predict(source=image, conf=0.25, save=False)[0]
    
    predictions = []
    for box in res.boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        conf = float(box.conf[0])
        predictions.append({
            'label': label, 
            'conf' : round(conf, 3)
        })
    
    payload = {
        'timestamps': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 
        'predictions': predictions
    }
    
    publish_mqtt(payload)
    annotated_image = res.plot()
    return annotated_image, predictions


with gr.Blocks() as demo: 
    gr.Markdown('## 🎯 YOLOv11n Detection + MQTT Publisher')
    
    with gr.Row(): 
        image_input = gr.Image(type='filepath', label='Upload Image')
        image_output = gr.Image(label='Result with Bounding Box', streaming=True)
    
    json_output = gr.JSON(label='Predictions')
    
    btn = gr.Button('Run Detection')
    btn.click(fn=detect_image, inputs=image_input, outputs=[image_output, json_output])

if __name__ == "__main__":
    connect_mqtt()
    demo.launch()