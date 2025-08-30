# Object_-Object-Detection-Microservices
Microservices project for image object detection using FastAPI and YOLOv5. Includes UI backend for uploads and AI backend for inference; fully containerized with Docker. Outputs annotated images and JSON results, easy to deploy on any system.
## Overview

This project implements a microservice architecture for object detection, consisting of two primary backend components:

- **UI Backend Service**  
  Receives image uploads from users and forwards them to the AI backend.
- **AI Backend Service**  
  Utilizes a lightweight YOLOv5 model to perform object detection and returns detection results as structured JSON and annotated images.

The solution is designed for full portability and ease of deployment using Docker.

---

## Features

- Accepts image uploads via HTTP API.
- Detects objects using YOLOv5 (CPU compatible, no GPU required).
- Returns annotated output images (bounding boxes) and JSON with detection results.
- Easy to deploy: just run via Docker Compose.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.8 or newer (for local runs outside Docker)

---

## Installation & Usage

1. **Clone or Download the Project**

2. **Build & Run the Microservices:**
    ```
    docker-compose up --build
    ```
   This starts AI backend on port 8000 and UI backend on port 8001.

3. **Make Predictions:**
    Send a POST request with an image using curl, Postman, etc. Example with curl:
    ```
    curl -X POST "http://localhost:8001/upload/" -F "file=@sample_image.jpg"
    ```
    The response will include detection results and output file paths.

4. **View Results:**
    - Annotated images and JSON outputs will appear in the `/output` folder.
    - Check `output/output_<filename>.jpg` and `output/output_<filename>.jpg.json`.

---
---

## How it Works

- The **UI backend** receives the image and sends it to the AI backend.
- The **AI backend** predicts object locations/labels, draws bounding boxes, and saves results.
- Response is sent back to the UI/backend and user, with image and JSON persisted to disk.

---

## References

- [YOLOv5 Ultralytics](https://github.com/ultralytics/yolov5)
- [YOLOv3 (assessment reference)](https://github.com/ultralytics/yolov3)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## Sample Output

See the `/output` directory for example annotated images and JSON files from your own tests.

---

## Contributors

- Built for technical assessment. Inspired by the open-source community.

---
project-root/
├── object_detection_service.py # AI backend (detection logic)
├── ui_service.py # UI backend (upload handler)
├── requirements.txt
├── Dockerfile.ai
├── Dockerfile.ui
├── docker-compose.yml
├── output/ # Saved results (images, JSON)
└── README.md # (this file)

**For any questions or replication issues, please refer to the step-by-step instructions above or raise an issue in this repository.**


## Project Structure
