"""
LLM Client

Wrapper around Ollama.
"""

import ollama


class LLMClient:
    """
    Ollama LLM wrapper.
    """

    def __init__(
        self,
        model_name: str = "qwen2.5:3b",
        temperature: float = 0.2,
    ):

        self.model_name = model_name

        self.temperature = temperature

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an answer from the LLM.
        """

        response = ollama.chat(

            model=self.model_name,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            options={
                "temperature": self.temperature,
            },
        )

        return response["message"]["content"]