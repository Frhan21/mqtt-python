# Real-time YOLO Object Detection with Gradio and MQTT

This project demonstrates a real-time object detection system that leverages YOLOv8 for computer vision, integrates with a Gradio web interface for live webcam streaming, and publishes detection results via MQTT. It's designed to showcase a complete pipeline from video input to data publishing.

## Features

*   **Real-time Object Detection:** Utilizes a pre-trained YOLOv8n model to detect objects from a live webcam feed.
*   **Interactive Web Interface:** Powered by Gradio, providing a user-friendly web application to view the annotated webcam stream and raw detection data (JSON).
*   **MQTT Integration:** Publishes detected object labels, confidence scores, and timestamps to a specified MQTT topic (`sensor/data`).
*   **Modular Design:** Separates the MQTT client logic into a dedicated module (`mqtt_publish.py`) for better organization.

## Technologies Used

This project is built using the following key technologies:

*   **Python:** [!Python](https://www.python.org/)
*   **Gradio:** [!Gradio](https://gradio.app/)
*   **Ultralytics YOLO:** [!Ultralytics YOLO](https://ultralytics.com/)
*   **MQTT:** [!MQTT](https://mqtt.org/)


## Prerequisites

Before running the application, ensure you have the following installed:

*   **Python 3.x**
*   **pip** (Python package installer)
*   An **MQTT Broker** (e.g., `test.mosquitto.org` or a local instance like Mosquitto).

## Installation

1.  **Clone the repository (or create the project files):**
    Ensure all provided `.py` files and the `model/yolo11n.pt` file are in their respective locations within your project directory.

2.  **Create a Python Virtual Environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **Linux / macOS:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Required Python Libraries:**
    First, create a `requirements.txt` file in your project root (see next section for content).

    Then, install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

5.  **YOLOv8 Model:**
    The project expects the YOLOv8n model file at `model/yolo11n.pt`. This file should already be present in the `model/` subdirectory.

## Usage

1.  **Ensure your MQTT Broker is running and accessible.**
    The application is configured to connect to `test.mositto.org` on port `1883` by default. You can modify these settings in `mqtt_publish.py`.

2.  **Run the main application script:**
    ```bash
    python gradio_detect_webcam.py
    ```

3.  **Access the Web Interface:**
    Gradio will provide a local URL (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser.

4.  **Observe Real-time Detection:**
    Your webcam feed will appear with detected objects highlighted. The detection results (JSON payload) will be displayed on the interface and simultaneously published to the MQTT topic `sensor/data`.

## Project Structure

```
.
├── gradio_detect_image.py  # Main script: Gradio UI, YOLO detection, calls MQTT publishing
├── mqtt_publish.py          # MQTT client setup and functions for publishing data
├── model/                   # Directory for storing YOLO models
│   └── yolo11n.pt           # Pre-trained YOLOv8n nano model
├── venv/                    # Python virtual environment (created during setup)
└── README.md                # This file
```

## Notes

*   The `mqtt_publish.py` file was previously named `publish.py`. It contains a `publish_data` function for random sensor data which is not currently used by `gradio_detect_webcam.py`. This function can be removed or adapted if only detection data is relevant.
*   The Gradio component `gr.Webcam()` is used for webcam input, which is compatible with a wider range of Gradio versions. For very recent Gradio versions, `gr.Image(source="webcam", streaming=True)` might be an alternative, but `gr.Webcam()` is generally more robust for direct webcam access.
```

```diff
gradio
ultralytics
opencv-python
paho-mqtt
numpy
