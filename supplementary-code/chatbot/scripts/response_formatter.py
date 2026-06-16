from typing import Optional


def format_response(
    title: str,
    explanation: str,
    note: Optional[str] = None
) -> str:
    response = f"""{title}

Explanation:
{explanation}
""".strip()

    if note:
        response += f"""

Note:
{note}
""".rstrip()

    return response
