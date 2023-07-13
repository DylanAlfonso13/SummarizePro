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

    json_data = json.dumps(extracted_data)
    json_output_path = 'path_to_output_json_file.json'

    with open(json_output_path, 'w') as json_file:
        # json_text = json_file.write(json_data)
        json_text = json_data

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the text:" +
                str(json_text)},


        ],
        temperature=1,
    )
    return response["choices"][0]["message"]["content"]
