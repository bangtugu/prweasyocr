import fitz  # pymupdf
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO
import io

'''
def clean_ocr_text(raw_text):
    import re
    # 한글 사이 띄어쓰기 없애기 (예: '묘 구 사 항' → '묘구사항')
    raw_text = re.sub(r'(?<=[가-힣])\s(?=[가-힣])', '', raw_text)
    # 반복된 줄바꿈 및 공백 정리
    raw_text = re.sub(r'\n+', '\n', raw_text)
    raw_text = re.sub(r'[ ]{2,}', ' ', raw_text)
    return raw_text.strip()
'''


reader = easyocr.Reader(['ko', 'en'], gpu=False)  # GPU 있으면 gpu=True 가능


def run_ocr(image_bytes):
    # image_bytes는 바이트형 이미지 데이터라고 가정
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img_np = np.array(img)

    # easyocr는 numpy array (RGB) 입력 필요
    result = reader.readtext(img_np, detail=0)
    # print("OCR 결과:", result)
    return "\n".join(result)


def clean_ocr_text(raw_text):
    import re
    # 한글 사이 띄어쓰기 없애기 (예: '묘 구 사 항' → '묘구사항')
    raw_text = re.sub(r'(?<=[가-힣])\s(?=[가-힣])', '', raw_text)
    # 반복된 줄바꿈 및 공백 정리
    raw_text = re.sub(r'\n+', '\n', raw_text)
    raw_text = re.sub(r'[ ]{2,}', ' ', raw_text)
    return raw_text.strip()


def get_image_at_block(page, block=[]):
    # bbox = (x0, y0, x1, y1)
    # 해당 영역을 pixmap으로 크롭해서 bytes 반환
    # fitz.Rect 쓰면 좌표 정리 편함
    dpi_set = 300
    if not block:
        pix = page.get_pixmap(dpi=dpi_set)
    else:
        bbox = block[:4]
        rect = fitz.Rect(bbox)
        pix = page.get_pixmap(clip=rect, dpi=dpi_set)  # dpi 높이면 해상도 증가
    
    img_bytes = pix.tobytes(output="png")
    return img_bytes


def pdf_to_text_with_ocr(pdf_bytes, lang='eng+kor'):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)
        # print(images)
        blocks = page.get_text("blocks")
        # print(blocks)
        
        if not blocks:
            img_bytes = get_image_at_block(page)
            text = run_ocr(img_bytes)
            full_text.append(text)

        else:
            for b in blocks:
                if b[6] == 0:
                    full_text.append(b[4])
                else:
                    img_bytes = get_image_at_block(page, b)
                    text = run_ocr(img_bytes)
                    full_text.append(text)

    doc.close()

    for i in range(len(full_text)):
        full_text[i] = clean_ocr_text(full_text[i])

    return "\n\n".join(full_text)