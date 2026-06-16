from typing import Dict, Optional

GENERIC_PHRASES: set = {
    "help",
    "legal help",
    "legal issue",
    "problem",
    "need help",
    "what should i do",
    "law help"
}

LEGAL_ANCHORS: set = {
    "fir",
    "rti",
    "bail",
    "legal notice",
    "ipc",
    "crpc",
    "law",
    "section",
    "offence",
    "police",
    "court",
    "arrest",
    "arrested",
    "custody",
    "detained",
    "jail"
}


def is_vague_query(user_query: str) -> Dict[str, Optional[str]]:
    query = user_query.lower().strip()

    if len(query.split()) < 4 and not any(anchor in query for anchor in LEGAL_ANCHORS):
        return {
            "is_vague": True,
            "reason": "Query is too short and lacks legal context."
        }

    if query in GENERIC_PHRASES:
        return {
            "is_vague": True,
            "reason": "Query is too generic and lacks legal context."
        }

    if not any(anchor in query for anchor in LEGAL_ANCHORS):
        return {
            "is_vague": True,
            "reason": "Query lacks identifiable legal or document references."
        }

    return {
        "is_vague": False,
        "reason": None
    }
