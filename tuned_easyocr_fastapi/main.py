# main.py
from fastapi import FastAPI, UploadFile
from ocr_utils import init_reader, run_ocr, clean_ocr_text_list

app = FastAPI()

# 커스텀 모델 로드
# GPU가 없다면 gpu=False로 변경 가능
reader = init_reader(custom_model_path="best.pth", gpu=False, langs=['ko', 'en'])

@app.post("/ocr/")
async def ocr(file: UploadFile):
    file_bytes = await file.read()
    text = run_ocr(reader, file_bytes)
    text = clean_ocr_text_list([text])
    return {"text": text}
