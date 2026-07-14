"""
Response Formatter
"""

from src.llm.response_schema import RAGResponse


class ResponseFormatter:

    @staticmethod
    def format(
        response: RAGResponse,
    ) -> str:

        output = []

        output.append("=" * 80)

        output.append("ANSWER")

        output.append("=" * 80)

        output.append(response.answer)

        output.append("\n")

        output.append("=" * 80)

        output.append("SUPPORTING REFERENCES")

        output.append("=" * 80)

        for index, source in enumerate(
            response.sources,
            start=1,
        ):

            output.append(

                f"""
[{index}]

Document : {source.metadata.document_name}

Page : {source.metadata.page_number}

Similarity Score : {source.score:.4f}

Evidence

{source.text}

{"-" * 80}
"""
            )

        return "\n".join(output)