from typing import Dict, Any


FIR_TEMPLATE: Dict[str, Any] = {
    "title": "First Information Report (FIR)",

    "what_it_is": (
        "A First Information Report (FIR) is the first official written record of information "
        "given to the police about the commission of a serious crime. "
        "It is recorded by the police when the information relates to a cognizable offence, "
        "meaning an offence for which the police can take action without prior court approval."
    ),

    "why_it_exists": (
        "The FIR exists to formally bring a serious offence to the notice of the police "
        "and to ensure that the information is officially documented. "
        "It creates a starting point for the criminal justice process and helps maintain "
        "a transparent record of allegations made."
    ),

    "when_it_is_used": (
        "An FIR is generally used when a person wants to report a serious crime such as "
        "theft, assault, harassment, domestic violence, or other cognizable offences. "
        "It may be filed by the victim, a witness, or any person with knowledge of the incident."
    ),

    "what_it_does_not_do": (
        "An FIR does not decide whether an offence has actually occurred. "
        "It does not determine guilt or innocence, and it does not guarantee arrest or punishment. "
        "It only records information for the purpose of investigation."
    )
}


RTI_TEMPLATE: Dict[str, Any] = {
    "title": "Right to Information (RTI) Application",

    "what_it_is": (
        "An RTI application is a formal request made by a citizen to seek information "
        "from a public authority under the Right to Information Act, 2005. "
        "It allows citizens to ask for records, documents, or data held by government bodies."
    ),

    "why_it_exists": (
        "The RTI mechanism exists to promote transparency and accountability in government functioning. "
        "It empowers citizens to understand how public authorities make decisions and use public resources."
    ),

    "when_it_is_used": (
        "RTI applications are commonly used when a person wants information about "
        "government decisions, official records, public spending, policies, or administrative actions."
    ),

    "what_it_does_not_do": (
        "An RTI application does not resolve disputes, justify decisions, or provide explanations. "
        "It only gives access to information that already exists with the public authority."
    )
}


BAIL_TEMPLATE: Dict[str, Any] = {
    "title": "Bail Application",

    "what_it_is": (
        "A bail application is a formal request made to a court seeking the temporary release "
        "of an accused person from custody while the legal proceedings are ongoing. "
        "It relates to personal liberty during the period before or during trial."
    ),

    "why_it_exists": (
        "The concept of bail exists to protect individual freedom and to ensure that a person "
        "is not unnecessarily kept in custody before a court determines guilt or innocence."
    ),

    "when_it_is_used": (
        "A bail application is generally used after a person has been arrested, "
        "or when there is a reasonable fear of arrest in certain serious cases."
    ),

    "what_it_does_not_do": (
        "Grant of bail does not end the criminal case and does not declare the person innocent. "
        "It only allows temporary release subject to conditions imposed by the court."
    )
}


LEGAL_NOTICE_TEMPLATE: Dict[str, Any] = {
    "title": "Legal Notice",

    "what_it_is": (
        "A legal notice is a formal written communication sent to a person or organization "
        "to inform them about a legal grievance or claim. "
        "It serves as an official intimation of a legal issue."
    ),

    "why_it_exists": (
        "A legal notice exists to formally communicate a concern and give the recipient "
        "an opportunity to respond or address the issue before formal legal proceedings begin."
    ),

    "when_it_is_used": (
        "Legal notices are commonly used in civil disputes, contractual matters, "
        "property issues, employment disputes, or consumer-related grievances."
    ),

    "what_it_does_not_do": (
        "A legal notice does not itself start a court case, "
        "and it does not decide liability, guilt, or punishment."
    )
}


COMPLAINT_TEMPLATE: Dict[str, Any] = {
    "title": "Complaint",

    "what_it_is": (
        "A complaint is a formal statement made to a legal authority describing an offence, "
        "grievance, or unlawful act. "
        "It may be submitted to the police or directly to a court, depending on the situation."
    ),

    "why_it_exists": (
        "A complaint exists to formally bring a matter to the attention of authorities "
        "when a person believes a legal wrong has occurred."
    ),

    "when_it_is_used": (
        "Complaints are commonly used when an FIR is not registered, "
        "or when the matter involves offences that require court intervention."
    ),

    "what_it_does_not_do": (
        "A complaint does not automatically lead to arrest or punishment. "
        "It does not by itself establish that an offence has been committed."
    )
}


CHARGE_SHEET_TEMPLATE: Dict[str, Any] = {
    "title": "Charge Sheet",

    "what_it_is": (
        "A charge sheet is a formal document prepared by the police after completing an investigation. "
        "It lists the allegations, evidence collected, and the sections of law applied."
    ),

    "why_it_exists": (
        "The charge sheet exists to inform the court about the outcome of the police investigation "
        "and to formally place the case before the judicial system."
    ),

    "when_it_is_used": (
        "A charge sheet is used after the police finish investigating a case "
        "and are ready to present their findings to the court."
    ),

    "what_it_does_not_do": (
        "A charge sheet does not decide guilt or innocence. "
        "It only presents the police version of the case for judicial consideration."
    )
}


AFFIDAVIT_TEMPLATE: Dict[str, Any] = {
    "title": "Affidavit",

    "what_it_is": (
        "An affidavit is a written statement of facts sworn to be true by a person "
        "and signed before an authorized authority. "
        "It is used as a formal declaration in legal and official matters."
    ),

    "why_it_exists": (
        "Affidavits exist to allow individuals to formally declare facts "
        "and take responsibility for the truthfulness of their statements."
    ),

    "when_it_is_used": (
        "Affidavits are commonly used in courts, government procedures, "
        "and administrative processes where verified statements are required."
    ),

    "what_it_does_not_do": (
        "An affidavit does not prove the facts stated in it by itself. "
        "It only records a sworn statement made by the person."
    )
}


SUMMONS_TEMPLATE: Dict[str, Any] = {
    "title": "Summons",

    "what_it_is": (
        "A summons is an official legal document issued by a court or authority "
        "requiring a person to appear before it at a specified time and place."
    ),

    "why_it_exists": (
        "Summons exist to formally inform a person that their presence is required "
        "in connection with a legal matter."
    ),

    "when_it_is_used": (
        "Summons are commonly used to call witnesses, accused persons, "
        "or parties to a case before a court."
    ),

    "what_it_does_not_do": (
        "A summons does not imply guilt and does not authorize arrest by itself."
    )
}


WARRANT_TEMPLATE: Dict[str, Any] = {
    "title": "Warrant",

    "what_it_is": (
        "A warrant is a formal written order issued by a court authorizing a specific legal action, "
        "such as arrest or search, under the authority of law."
    ),

    "why_it_exists": (
        "Warrants exist to ensure that certain actions affecting personal liberty or property "
        "are carried out only with judicial approval."
    ),

    "when_it_is_used": (
        "Warrants are generally used when a court believes compulsory legal action is necessary "
        "to ensure compliance with the law."
    ),

    "what_it_does_not_do": (
        "A warrant does not determine guilt or innocence. "
        "It only authorizes a specific legal action as permitted by law."
    )
}


DOCUMENT_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "fir": FIR_TEMPLATE,
    "rti": RTI_TEMPLATE,
    "bail": BAIL_TEMPLATE,
    "legal_notice": LEGAL_NOTICE_TEMPLATE,
    "complaint": COMPLAINT_TEMPLATE,
    "charge_sheet": CHARGE_SHEET_TEMPLATE,
    "affidavit": AFFIDAVIT_TEMPLATE,
    "summons": SUMMONS_TEMPLATE,
    "warrant": WARRANT_TEMPLATE
}
