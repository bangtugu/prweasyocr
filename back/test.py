import pdftotext

if __name__ == "__main__":
    temppdfpath = '../data/한국고등직업교육학회.pdf'
    with open(temppdfpath, "rb") as f:
        pdf_bytes = f.read()

    extracted_text = pdftotext.pdf_to_text_with_ocr(pdf_bytes)
    print(extracted_text)