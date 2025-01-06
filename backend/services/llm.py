# llm service for reasoning and generating actions

import openai
from typing import List, Dict
import os

class LLMService:
    """
        Interface for interacting with the LLM
    """
    def __init__(self):
        self.llm = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str) -> List[str]:
        """
            Generate a list of possible actions for the user to take
        """
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5, 
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content.split("\n")