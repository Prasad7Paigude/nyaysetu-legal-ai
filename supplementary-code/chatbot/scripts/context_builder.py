from typing import Any, List


def build_context(docs: List[Any]) -> str:
    if not docs:
        return ""

    context_blocks = []

    for idx, doc in enumerate(docs, start=1):
        block = f"""
[Source {idx}]
{doc.page_content}
"""
        context_blocks.append(block.strip())

    return "\n\n".join(context_blocks)
