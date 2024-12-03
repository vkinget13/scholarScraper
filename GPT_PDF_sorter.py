import openai
import pandas as pd 
import requests
from io import BytesIO
import pdfplumber

openai.api_key = "xxxx" #fill in


#Function that interacts with the GPT
def generate_gpt(prompt, content):
    response = openai.Completion.create(
        engine = "", #fill in
        prompt = f"{prompt}\n\nContent:\n{content}",
        max_tokens = XXX,
        n=1
        stop = None,
        temperature = 0.7, #what should i use here
    )
    return response.choices[0].text.strip()

#Function that extracts text from PDF
def extract_text_from_pdf(url):
    repsonse = requests.get(url)
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

#Load Excel and get URLs
excel_path = #enter path
df = pd.read_excel(excel_path)
urls = df['PDF-URL']

# the prompt
domain_prompt = """I am working on a research roadmap for a national park in belgium. All the research and articles that have taken place in the national park have been gathered and need to be categorized into research domains. You are a park expert and will categorize them into the domains. 
The research domains are as follows: 
Soil and Water
Fauna and Wildlife
Climate Adaptation & Resilience
Forests, Nature, and Landscapes
Tourism and Experience
Agriculture
Protected Nature
Health, Well-being, and Air Quality
Nature & Society
Circular Economy : 
If an upload does not fit directly into one of these domains, enter it as Not applicable. examples of this are (biographies, poems, pieces focused only on history, personal essays, etc).  
In your response, give only the name of the category and nothing more. "
"""
keywords_prompt = ("")

summary_prompt = ("")

#define the domains
domains = [
    "Soil and Water",
    "Fauna and Wildlife",
    "Climate Adaptation & Resilience",
    "Forests",
    "Nature and Landscapes",
    "Tourism and Experience",
    "Agriculture",
    "Protected Nature",
    "Health, Well-being, and Air Quality",
    "Circular Economy"
]


#Process each URL

results = []
for index, row in df.iterrows():
    url = row['PDF URL']
    try:
        pdf_text = extract_text_from_pdf(url)
       
        #get the domain
        gpt_response_domain = generate_gpt(domain_prompt, pdf_text[:4000])  # Truncate text if too long - see if we want to do this 
        #mark domain in excel
        if gpt_response in domains:
                df.at[index, gpt_response] = 1

        #get keywords
        gpt_response_keywords = generate_gpt(keywords_prompt, pdf_text[:4000])
        df.at[index, "Keywords"] = gpt_response_keywords

        #get summary or abstract
        gpt_response_summary = generate_gpt(summary_prompt, pdf_text[:4000])
        df.at[index, "Summary/Abstract"] = gpt_response_summary

        

    except Exception as e:
        df.at[index, "Keywords"] = f"Error: {str(e)}"
        df.at[index, "Summary/Abstract"] = f"Error: {str(e)}"

# Save the results to a new Excel file
output_df = pd.DataFrame(results)
output_df.to_excel("indexed_inventory.xlsx", index=False)
print("Processing completed. Results saved to indexed_inventory.xlsx")