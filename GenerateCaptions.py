# ============================================================
# IMPORTS
# ============================================================

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_captions(LL_type,knowledge_base,program_name):
    llm = ChatGoogleGenerativeAI(
       model=LL_type,
       temperature=0.8,
    api_key=GEMINI_API_KEY
    )

    prompt = ChatPromptTemplate.from_template("""
You are an AI assistant creating Instagram carousel captions for an insurance company.

Your task:
- Generate captions ONLY for the specific insurance program implied by the provided examples.
- Learn the tone, structure, vocabulary, and marketing style from the examples.
- Combine and remix ideas creatively, but do NOT copy sentences verbatim.

STRICT RULES (MANDATORY):
- Language: Greek ONLY
- Domain: Insurance ONLY
- Do NOT introduce benefits, coverages, guarantees, prices, or conditions
  that are NOT clearly present or inferable from the examples.
- Do NOT exaggerate, speculate, or invent insurance features.
- Do NOT reference laws, percentages, durations, or numbers unless they exist in the examples.
- No emojis unless they are clearly used in the examples.
- Confident, professional, polite marketing tone (not aggressive, not casual).

OUTPUT REQUIREMENTS:
- Produce EXACTLY 3 captions
- Each caption must have 2–6 pages
- Use the format:
  page1:
  page2:
  ...
- Each page should be short, Instagram-friendly, and readable.
- Captions must be suitable for an Instagram carousel post.

FORMAT CONSTRAINTS:
- Return ONLY valid JSON
- No explanations
- No markdown
- No comments
- No text outside JSON

JSON STRUCTURE (EXACT):
{{
  "program": "{program_name}",
  "captions": [
    {{
      "pages": {{
        "page1": "...",
        "page2": "...",
        "page3": "..."
      }}
    }},
    {{
      "pages": {{
        "page1": "...",
        "page2": "..."
      }}
    }},
    {{
      "pages": {{
        "page1": "...",
        "page2": "...",
        "page3": "...",
        "page4": "..."
      }}
    }}
  ]
}}

Insurance Program Name: 
{program_name}
EXAMPLES (written by the client):
{examples}

    """)

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"examples": knowledge_base,"program_name":program_name})