import os
from dotenv import load_dotenv


load_dotenv()


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-2.5-flash"

    def generate_document(self, **data):
        """
        Generate a legal document using Gemini.
        If API key is missing, return a demo document.
        """

        if not self.api_key:
            return {
                "document": self._demo_document(data),
                "model": "Demo Mode",
                "demo_mode": True
            }

        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)

            prompt = self._build_prompt(data)

            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            document = response.text

            if not document:
                raise ValueError("Gemini returned an empty response.")

            return {
                "document": document,
                "model": self.model,
                "demo_mode": False
            }

        except ImportError:
            raise ValueError(
                "Google GenAI package missing. Install it using: "
                "pip install google-genai"
            )

    def _build_prompt(self, data):
        return f"""
You are a legal document drafting assistant.

Draft a clear and professional legal document based on the details below.
Use simple, formal language. Do not invent missing facts.
Include suitable headings, clauses, and signature sections.
Mention that the document should be reviewed by a qualified legal professional.

Document type: {data.get("document_type", "")}
Parties: {data.get("parties", "")}
Terms: {data.get("terms", "")}
Effective date: {data.get("effective_date", "")}
Jurisdiction: {data.get("jurisdiction", "Not specified")}
Additional instructions: {data.get("additional_instructions", "")}
"""

    def _demo_document(self, data):
        return f"""
{data.get("document_type", "LEGAL DOCUMENT").upper()}

Effective Date: {data.get("effective_date", "Not specified")}

PARTIES
{data.get("parties", "Not specified")}

TERMS AND CONDITIONS
{data.get("terms", "Not specified")}

JURISDICTION
{data.get("jurisdiction", "Not specified")}

ADDITIONAL INSTRUCTIONS
{data.get("additional_instructions", "None")}

SIGNATURES

Party 1: ______________________

Party 2: ______________________

Note: This is a demo draft, not legal advice. Please have it reviewed
by a qualified legal professional before using it.
"""