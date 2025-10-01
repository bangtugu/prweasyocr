from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import pdftotext  # OCR 처리 모듈

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 개발서버 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract/")
async def upload_files(files: List[UploadFile] = File(...)):
    results = {}
    for file in files:
        pdf_bytes = await file.read()
        try:
            text = pdftotext.pdf_to_text_with_ocr(pdf_bytes)
            results[file.filename] = text
        except Exception as e:
            results[file.filename] = f"ERROR: {str(e)}"
    return results

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # main.py 안에 있는 app 객체
        host="0.0.0.0",      # 외부 접속 허용 (로컬만 할거면 127.0.0.1)
        port=8001,           # 원하는 포트 번호
        reload=True          # 코드 변경 시 자동 리로드 (개발용)
    )