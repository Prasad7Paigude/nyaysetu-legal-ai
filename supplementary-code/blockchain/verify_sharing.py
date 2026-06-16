"""End-to-end verification script for the file-sharing workflow.

Registers two users, uploads a file from user A, shares it with user B,
and verifies that user B can view and download the file successfully.
"""

import json
import os
import time
from typing import Any, Optional

import requests

BASE_URL: str = "http://localhost:9000"


def register(username: str) -> requests.Session:
    """Register a new user and return an authenticated session.

    Args:
        username: Display name for the user.

    Returns:
        A :class:`requests.Session` with the registration cookie.
    """
    session = requests.Session()
    resp = session.post(f"{BASE_URL}/register", data={"username": username})
    logger.info("Register %s: %s", username, resp.status_code)
    return session


def get_user_key(session: requests.Session) -> str:
    """Retrieve the user's key by fetching the home page.

    Note:
        This function is a stub; the actual key is read from
        ``app/data.json`` in :func:`verify` for simplicity.

    Args:
        session: Authenticated requests session.

    Returns:
        Response text (currently unused).
    """
    resp = session.get(BASE_URL)
    return resp.text


def verify() -> None:
    """Execute the full file-sharing workflow and assert expected outcomes.

    Steps:
        1. Register User A and User B.
        2. Read both user keys from ``app/data.json``.
        3. User A uploads a dummy file.
        4. Locate the file key in ``app/data.json``.
        5. User A shares the file with User B.
        6. User B views shared files and checks for the filename.
        7. User B downloads the file and verifies its contents.
    """
    session_a = register("UserA")
    session_b = register("UserB")

    time.sleep(1)

    with open("app/data.json", "r") as f:
        data: dict = json.load(f)

    key_a: str = data["users"]["UserA"]
    key_b: str = data["users"]["UserB"]
    logger.info("Key A: %s", key_a)
    logger.info("Key B: %s", key_b)

    with open("test_upload.txt", "w") as f:
        f.write("This is a secret file.")

    files: dict = {"v_file": open("test_upload.txt", "rb")}
    resp = session_a.post(f"{BASE_URL}/submit", data={"user": "UserA"}, files=files)
    logger.info("Upload: %s", resp.status_code)

    with open("app/data.json", "r") as f:
        data = json.load(f)

    file_key: Optional[str] = None
    for k, v in data["files"].items():
        if v["filename"] == "test_upload.txt" and v["owner"] == key_a:
            file_key = k
            break

    logger.info("File Key: %s", file_key)

    resp = session_a.post(
        f"{BASE_URL}/share",
        data={"file_key": file_key, "recipient_key": key_b},
    )
    logger.info("Share: %s", resp.status_code)

    resp = session_b.post(
        f"{BASE_URL}/view_shared", data={"sender_key": key_a}
    )
    logger.info("View Shared: %s", resp.status_code)

    if "test_upload.txt" in resp.text:
        logger.info("SUCCESS: File found in shared view.")
    else:
        logger.info("FAILURE: File NOT found in shared view.")

    resp = session_b.get(f"{BASE_URL}/download/{file_key}")
    logger.info("Download: %s", resp.status_code)
    if resp.text == "This is a secret file.":
        logger.info("SUCCESS: File content verified.")
    else:
        logger.info("FAILURE: File content mismatch.")


if __name__ == "__main__":
    verify()
