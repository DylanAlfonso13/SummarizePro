![example workflow](https://github.com/DylanAlfonso13/SummarizePro/actions/workflows/styling.yaml/badge.svg)
![example workflow](https://github.com/eunicehassan3/Week2Project/actions/workflows/unittests.yaml/badge.svg)
# Welcome to SummarizePro
Using GPT API to summarize articles and PDFs
* Have you ever wanted to use ChatGPT to summarize an article or pdf, but you have to go through the hassle of copying / pasting the content?
* We feel you... Which is why we created this app! 
    * It simply reads in a URL for an article or a PDF
    * BOOM! Now you have the summary that ChatGPT would provide you with half the hassle!
    
## Built With
<img height="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/184117132-9e89a93b-65fb-47c3-91e7-7d0f99e7c066.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/183896128-ec99105a-ec1a-4d85-b08b-1aa1620b2046.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png">
<img height="50" src="https://user-images.githubusercontent.com/25181517/183898054-b3d693d4-dafb-4808-a509-bab54cf5de34.png">
<img height="50" src ="https://user-images.githubusercontent.com/25181517/117447155-6a868a00-af3d-11eb-9cfe-245df15c9f3f.png">

## Setup
### If you would like to use this app locally and edit it yourself, follow these steps
1. API key from https://platform.openai.com/docs/guides/gpt
2. Clone the repo
   ```sh
   git clone https://github.com/DylanAlfonso13/SummarizePro.git
   ```
3. Install required packages
   ```sh
   pip -r requirements.txt
   ```
4. Create a .env file
   ```sh
   touch .env
   ```
5. Copy the following code into your .env file
    ```sh
    FLASK_APP=app
    FLASK_ENV=development
    OPENAI_API_KEY=[INSERT API KEY HERE]
    ```

6. Run the app!
    ```sh
    python app.py
    ```

## Programmers Involved: 
* Dylan Alfonso
* Diego Santiago
* Eunice Hassan 