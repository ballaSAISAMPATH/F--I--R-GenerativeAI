from langchain_core.prompts import ChatPromptTemplate

encryption_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data anonymization assistant.

TASK:
- Identify sensitive data: names, locations, dates, amounts, phone numbers, etc.
- Replace them with placeholders:
  PERSON_1, LOCATION_1, DATE_1, AMOUNT_1, etc.

OUTPUT RULES (VERY IMPORTANT):
- Return ONLY valid JSON
- No explanation, no extra text
- Always include both keys

FORMAT:
{{
  "encrypted_narration": "string",
  "mapping": {{
    "PLACEHOLDER": "original value"
  }}
}}
"""),
    
    ("human",
     """Text:
{text}

Return ONLY JSON.""")
])