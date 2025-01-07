# llm service for reasoning and generating actions

from openai import OpenAI
from typing import List, Dict, Any
import json
import os

class LLMService:
    """
        Interface for interacting with the LLM
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate(self, prompt: str) -> List[str]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.split('\n')
        except Exception as e:
            print(f"Error in generate: {e}")
            return []

    async def generate_json(self, prompt: str) -> List[Dict[str, Any]]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Respond only with valid JSON array"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error in generate_json: {e}")
            return []