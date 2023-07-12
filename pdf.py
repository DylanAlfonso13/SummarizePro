import PyPDF2
import json


def pdf_to_json(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        num_pages = len(pdf_reader.pages)
        extracted_data = []

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            extracted_data.append(page.extract_text())

        # Convert extracted data to JSON
        json_data = json.dumps(extracted_data)

        # Define the output file path
        json_output_path = 'path_to_output_json_file.json'

        # Write JSON data to the output file
        with open(json_output_path, 'w') as json_file:
            # json_file.write(json_data)
            return json_data
    except Exception as e:
        print("The Following Error occurred" + str(e))




# if __name__ == '__main__':
#     texts = pdf_to_json("/Users/eunicehassan/Desktop/Letter for Financial Support (Corrected).pdf")
#     print(texts)