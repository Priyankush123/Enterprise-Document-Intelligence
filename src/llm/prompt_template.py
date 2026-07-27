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
You are an Enterprise Document Intelligence Assistant.

Answer questions ONLY using the provided document context.

Instructions:

1. Use ONLY the supplied document context.
2. Never invent, infer, or assume information that is not explicitly present.
3. If the answer cannot be found in the context, reply exactly:
   "I couldn't find this information in the provided documents."
4. If the answer is found across multiple documents, combine the information into a single coherent response.
5. Quote important values (numbers, dates, names, policies) exactly as they appear.
6. Keep answers clear, concise, and well-structured.
7. At the end of the answer, list the source document names and page numbers used.
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
--------------------
{chat_history}
"""

        prompt += f"""

Document Context
----------------
{context}

User Question
-------------
{question}

Answer
------
"""

        return prompt