from typing import Dict, List, Optional


def select_document(user_query: str) -> Optional[Dict[str, str]]:
    q = user_query.lower()

    RULES: List[Dict[str, str]] = [
        {
            "keywords": ["information", "details", "records", "government office"],
            "document": "RTI Application",
            "reason": "RTI is used to request information from public authorities."
        },
        {
            "keywords": ["threat", "assault", "stolen", "theft", "harassment", "crime"],
            "document": "FIR",
            "reason": "An FIR is used to report serious offences to the police."
        },
        {
            "keywords": ["arrest", "custody", "jail"],
            "document": "Bail Application",
            "reason": "Bail applications are used to seek temporary release from custody."
        },
        {
            "keywords": ["dispute", "payment", "contract", "notice"],
            "document": "Legal Notice",
            "reason": "Legal notices are used to formally communicate disputes before legal action."
        },
        {
            "keywords": ["complaint", "police not registering", "refused to file fir"],
            "document": "Complaint",
            "reason": "A complaint is used to formally bring a grievance to the attention of authorities."
        },
        {
            "keywords": ["summons", "called by court", "court notice"],
            "document": "Summons",
            "reason": "A summons is used to require a person to appear before a court or authority."
        },
        {
            "keywords": ["warrant", "arrest warrant", "search warrant"],
            "document": "Warrant",
            "reason": "A warrant authorizes specific legal actions under court authority."
        }
    ]

    for rule in RULES:
        for kw in rule["keywords"]:
            if kw in q:
                return {"document": rule["document"], "reason": rule["reason"]}

    return None
