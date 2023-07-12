from pdfminer.high_level import extract_text

def pdf_to_text():
    text = extract_text("/Users/eunicehassan/Library/Mobile Documents/com~apple~CloudDocs/Discrete Math/Problem Sets/2250 Discrete Problem Set 2 S23.pdf")
    print(text)
