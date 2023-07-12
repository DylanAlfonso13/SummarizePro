import PyPDF2
import json
import openai


def pdf_summary(pdf_file):
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
        # json_text = json_file.write(json_data)
        json_text = json_data


    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Can you summarize this json file: " + str(json_text),
        temperature=1,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
)
    return response["choices"][0]["text"]


# if __name__ == '__main__':
#     texts = pdf_summary("/Users/eunicehassan/Desktop/Letter for Financial Support (Corrected).pdf")
#     print(texts)