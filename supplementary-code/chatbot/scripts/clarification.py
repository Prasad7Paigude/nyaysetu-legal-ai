def get_clarification_question(reason: str) -> str:
    if reason == "Query is too short and lacks legal context.":
        question = (
            "Could you please clarify whether your question is about a "
            "legal document (such as FIR or RTI), or about understanding a law or legal term?"
        )

    elif reason == "Query is too generic and lacks legal context.":
        question = (
            "Are you trying to understand a legal document, "
            "or are you looking for general legal information?"
        )

    elif reason == "Query lacks identifiable legal or document references.":
        question = (
            "Could you please clarify which legal issue, document, or situation you are referring to?"
        )

    else:
        question = (
            "Could you please provide a bit more detail so I can understand your legal question better?"
        )

    return f"""
Clarification Needed

{question}

Note:
This system provides general legal information only.
""".strip()
