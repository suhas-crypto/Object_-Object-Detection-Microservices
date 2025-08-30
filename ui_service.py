from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

app = FastAPI()

AI_BACKEND_URL = "http://ai-backend:8000/detect/"  # docker network service

# --- Upload Form (GET /) ---
@app.get("/", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <body>
            <h2>Upload Image for Detection</h2>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                <input type="file" name="file" accept="image/*">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

# --- Handle Image Upload (POST /upload/) ---
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Prepare file for forwarding
        files = {"file": (file.filename, await file.read(), file.content_type)}

        # Send to AI backend
        async with httpx.AsyncClient() as client:
            response = await client.post(AI_BACKEND_URL, files=files)

        # Pass AI backend response back
        return JSONResponse(content=response.json())

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
async def root():
    return {"message": "UI Backend is running. Use POST /upload/ to send an image."}
