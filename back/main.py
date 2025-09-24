from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdftotext

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 개발서버 주소
    # 필요한 도메인 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    try:
        text = pdftotext.pdf_to_text_with_ocr(pdf_bytes)
        return {"filename": file.filename, "text": text}
    except Exception as e:
        return {"error": str(e)}