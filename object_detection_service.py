from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import json
import io
from PIL import Image
import torch
from pathlib import Path

app = FastAPI()

# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, trust_repo=True)

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_np = np.array(img)

        # Run inference
        results = model(img_np)

        detections = []
        for *box, conf, cls in results.xyxy[0].tolist():
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]
            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

        # Draw detections
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img_cv, f'{det["label"]} {det["confidence"]:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Output paths
        output_path = Path("output")
        output_path.mkdir(parents=True, exist_ok=True)

        safe_filename = Path(file.filename).name
        if not safe_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            safe_filename += ".jpg"

        output_img_file = output_path / f"output_{safe_filename}"
        stem = Path(safe_filename).stem
        output_json_file = output_path / f"output_{stem}.json"

        # Save image
        if not cv2.imwrite(str(output_img_file), img_cv):
            raise HTTPException(status_code=500, detail="Failed to save output image.")

        # Save detections
        with open(output_json_file, "w") as f:
            json.dump(detections, f, indent=4)

        return JSONResponse({
            "detections": detections,
            "output_image_path": str(output_img_file),
            "output_json_path": str(output_json_file)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
