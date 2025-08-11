from langchain_core.prompts import PromptTemplate

phi_masking_prompt = PromptTemplate.from_template("""
You are a data privacy assistant. Your task is to identify any PII (Personally Identifiable Information) in the following text. For each PII instance found, return a JSON list object which contains the exact value and its type.

Supported PII types: ID, NAME, EMAIL, PHONE, ADDRESS, SSN, DATE_OF_BIRTH, CREDIT_CARD, IP_ADDRESS, USERNAME, PASSWORD, ORGANIZATION, GEO_LOCATION, OTHER.

For names, store both the full name and add an element for the first name.

id:
{record_id}

Text:
{narrative}

Return format:

[
  {{ 
    "value": "PII value", 
    "type": "PII type"
  }}
]

Only return the output formatted data. If no PII is found, return an empty list
""")