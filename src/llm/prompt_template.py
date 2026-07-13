"""
Prompt Template

Builds prompts for Retrieval-Augmented Generation.
"""

from typing import Optional


class PromptTemplate:
    """
    Prompt builder for the RAG pipeline.
    """

    SYSTEM_PROMPT = """
You are an intelligent Enterprise Document Assistant.

Your job is to answer questions ONLY using the supplied document context.

Rules:

1. Never invent information.

2. If the answer cannot be found in the context,
   reply:

   "I couldn't find this information in the provided documents."

3. Keep answers concise.

4. Quote important values exactly.

5. Mention the source document and page number whenever possible.
"""

    @classmethod
    def build(
        cls,
        question: str,
        context: str,
        chat_history: Optional[str] = None,
    ) -> str:

        prompt = cls.SYSTEM_PROMPT.strip()

        if chat_history:

            prompt += f"""

Conversation History

{chat_history}
"""

        prompt += f"""

Document Context

{context}

User Question

{question}

Answer
"""

        return prompt