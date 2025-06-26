import gradio as gr 
from ultralytics import YOLO 
import cv2
import numpy as np 
import time 
from mqtt_publish import publish_mqtt, connect_mqtt


# Load model 
model = YOLO('model/yolo11n.pt')

def detect_from_frame(frame): 
    """
    Performs object detection on a single frame from the webcam.
    """
    if frame is None:
        # On the first run, frame can be None. Return default values.
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        return blank_image, "Waiting for webcam..."
        
    # Frame resized 
    frame_resize = cv2.resize(frame, (640, 480))
    
    # Deteksi dengan model YOLO 
    res = model.predict(source=frame_resize, conf=0.3, save=False, verbose=False)[0]
    annotated = res.plot()
    
    predictions = []
    for box in res.boxes: 
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        predictions.append({
            'label': label, 
            'confidence': conf
        })

    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": "webcam",
        "predictions": predictions
    }
    
    publish_mqtt(payload)

    # Konversi untuk gradio.Image (RGB)
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    return annotated_rgb, predictions

with gr.Blocks() as app: 
    gr.Markdown('## 📹 Realtime YOLO Detection')
    
    with gr.Row():
        # This component captures the webcam stream but is not displayed.
        # It acts as the input for the streaming event.
        webcam_input = gr.Image(streaming=True, visible=False)
        # This component displays the processed output frame.
        webcam_view = gr.Image(label="Live Detection", height=480, width=640)

    prediction_json = gr.JSON(label='Prediction JSON')
    
    # The .stream() event listener calls the function for each frame from the webcam.
    # This replaces the need for app.load with 'every'.
    webcam_input.stream(detect_from_frame, inputs=[webcam_input], outputs=[webcam_view, prediction_json])


if __name__ == '__main__': 
    connect_mqtt()
    app.launch()