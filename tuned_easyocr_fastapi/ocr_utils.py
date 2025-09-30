# ocr_utils.py
import torch
import sys
sys.path.append("C:/Users/1Class_04/Desktop/tuned_easyocr_fastapi/EasyOCR")
import easyocr
from PIL import Image
import numpy as np
from io import BytesIO
import re

def init_reader(custom_model_path, gpu=False, langs=['ko', 'en']):
    """
    최신 EasyOCR 기준으로 커스텀 모델을 로드
    custom_model_path: 커스텀 학습된 .pth 파일 경로
    gpu: GPU 사용 여부
    langs: 사용할 언어 리스트
    """
    import easyocr
    import torch

    # 기본 Reader 초기화
    reader = easyocr.Reader(
        lang_list=langs,
        gpu=gpu
    )

    # 커스텀 모델 가중치 로드 (recognizer만)
    checkpoint = torch.load(custom_model_path, map_location='cuda' if gpu else 'cpu')
    reader.recognizer.load_state_dict(checkpoint)
    reader.recognizer.eval()

    return reader



def run_ocr(reader, image_bytes):
    """
    이미지 바이트를 OCR로 텍스트 추출
    """
    try:
        img = Image.open(BytesIO(image_bytes)).convert('RGB')
        img_np = np.array(img)
        text_list = reader.readtext(img_np, detail=0)
        return "\n".join(text_list)
    except Exception as e:
        print("[OCR ERROR]", e)
        return ""


def clean_ocr_text_list(text_list):
    """
    OCR 결과 텍스트 정리
    """
    cleaned = []
    for t in text_list:
        # 한글 사이 공백 제거
        t = re.sub(r'(?<=[가-힣])\s(?=[가-힣])', '', t)
        # 연속 줄바꿈 제거
        t = re.sub(r'\n+', '\n', t)
        # 불필요한 공백 제거
        t = re.sub(r'[ ]{2,}', ' ', t)
        cleaned.append(t.strip())
    return "\n\n".join(cleaned)
