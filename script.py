from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

# ✅ Enable CORS for all origins (required for GitHub Pages or external tests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Perform OCR
        text = pytesseract.image_to_string(image)

        # Debug: Print the extracted text
        print("OCR Result:", text)

        # Use regex to extract multiplication of two 8-digit numbers
        match = re.search(r"(\d{8})\s*[\*x×]\s*(\d{8})", text)
        if not match:
            return JSONResponse(
                {"error": "Could not find a valid multiplication expression."},
                status_code=400
            )

        num1 = int(match.group(1))
        num2 = int(match.group(2))
        answer = num1 * num2

        return {
            "answer": answer,
            "email": "22f3001117@ds.study.iitm.ac.in"
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
