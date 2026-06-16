from enum import Enum, auto


class QueryIntent(Enum):
    DOCUMENT_EXPLANATION = auto()
    DOCUMENT_SELECTION = auto()
    INCIDENT_ANALYSIS = auto()
    PROCEDURAL = auto()
    ADVICE = auto()
    PURE_LEGAL_INFO = auto()


DOCUMENT_KEYWORDS: set = {
    "fir",
    "rti",
    "bail",
    "anticipatory bail",
    "legal notice",
    "notice"
}

DOCUMENT_EXPLANATION_TRIGGERS: set = {
    "application",
    "document",
    "notice",
    "draft"
}

DOCUMENT_SELECTION_TRIGGERS: set = {
    "which document",
    "what document",
    "which legal document",
    "what should i file",
    "i want information",
    "i need information",
    "government office",
    "someone threatened",
    "i was threatened",
    "police arrested",
    "was arrested",
    "in custody",
    "not returning deposit",
    "money not returned",
    "payment dispute",
    "deposit issue",
    "used when",
    "required for"
}

INCIDENT_VERBS: set = {
    "hit",
    "beaten",
    "threatened",
    "threaten",
    "cheated",
    "cheat",
    "harassed",
    "harass",
    "stalked",
    "stalk",
    "abused",
    "abuse",
    "stole",
    "steal",
    "robbed",
    "rob",
    "molested",
    "assaulted",
    "assault",
    "fraud",
    "scam"
}

PROCEDURAL_TRIGGERS: set = {
    "how do i",
    "how can i",
    "how to",
    "steps",
    "procedure",
    "process",
    "what should i do",
    "tell me how",
    "what should i write"
}

ADVICE_TRIGGERS: set = {
    "can police",
    "can i",
    "will i",
    "am i",
    "is it legal",
    "will i get",
    "can they",
    "what will happen",
    "will the police",
    "can the police"
}


def normalize(text: str) -> str:
    return text.lower().strip()


def classify_intent(user_query: str) -> QueryIntent:
    query = normalize(user_query)

    for trigger in PROCEDURAL_TRIGGERS:
        if trigger in query:
            return QueryIntent.PROCEDURAL

    for trigger in ADVICE_TRIGGERS:
        if trigger in query:
            return QueryIntent.ADVICE

    for trigger in DOCUMENT_SELECTION_TRIGGERS:
        if trigger in query:
            return QueryIntent.DOCUMENT_SELECTION

    if any(doc in query for doc in DOCUMENT_KEYWORDS):
        for trigger in DOCUMENT_EXPLANATION_TRIGGERS:
            if trigger in query:
                return QueryIntent.DOCUMENT_EXPLANATION

    return QueryIntent.PURE_LEGAL_INFO
