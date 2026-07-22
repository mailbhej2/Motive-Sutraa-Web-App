from google import genai

from config import GOOGLE_API_KEY, TEXT_MODEL


class AI:

    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        """

        response = self.client.models.generate_content(
            model=TEXT_MODEL,
            contents=prompt,
        )

        return response.text.strip()