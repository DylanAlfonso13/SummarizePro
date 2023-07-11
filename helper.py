from pdfminer.high_level import extract_text

def pdf_to_text(file):
    text = extract_text(file)
    print(text)