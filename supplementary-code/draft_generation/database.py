"""
NyaySetu Database Module - MongoDB integration for document storage and lifecycle tracking.

Provides persistence for generated documents, blockchain injection, and lifecycle management.
"""

import base64
import datetime
import logging
import os
import time
import uuid
from typing import Any, Dict, Optional

import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config.settings import BLOCKCHAIN_SERVICE_URL, MONGODB_URI

logger = logging.getLogger(__name__)


class NyaySetuDB:
    """MongoDB-backed document storage and lifecycle tracking."""

    def __init__(self, uri: Optional[str] = None) -> None:
        """Initialize the database connection.

        Args:
            uri: MongoDB URI string. Falls back to config.settings.MONGODB_URI.
        """
        self.uri: str = uri or MONGODB_URI
        self.client: Optional[MongoClient] = None
        self.db: Optional[Any] = None
        self.connect()

    def connect(self) -> None:
        """Establish connection to MongoDB."""
        if not self.uri:
            logger.warning("MONGODB_URI not set. Database features will be disabled.")
            return
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command("ismaster")
            self.db = self.client.get_database("nyaysetu_blockchain")
            logger.info("Successfully connected to MongoDB Atlas")
        except ConnectionFailure:
            logger.error("MongoDB server not available")
            self.client = None
        except Exception as exc:
            logger.error("MongoDB Connection Error: %s", exc)
            self.client = None

    def store_document(
        self,
        doc_type: str,
        user_data: Dict[str, Any],
        pdf_path: str,
        doc_hash: str,
        ref_num: Optional[str] = None,
    ) -> Optional[str]:
        """Store document metadata and content in the tracking database.

        Args:
            doc_type: Document type identifier (e.g. RTI_APPLICATION, AFFIDAVIT).
            user_data: Dictionary of user-submitted form data.
            pdf_path: Absolute or relative path to the generated PDF.
            doc_hash: SHA-256 hex digest of document content.
            ref_num: Optional human-readable reference number.

        Returns:
            Inserted document ID as string, or None on failure.
        """
        if self.db is None:
            return None

        user_key = user_data.get("userKey")
        username = user_data.get("username")

        if user_key:
            logger.debug("userKey detected, storing in blockchain as well...")
            filename = os.path.basename(pdf_path)
            self.store_in_blockchain(user_key, username, pdf_path, filename)

        try:
            with open(pdf_path, "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read()).decode("utf-8")

            document: Dict[str, Any] = {
                "type": doc_type,
                "user_name": user_data.get("name") or user_data.get("deponent_name"),
                "metadata": user_data,
                "hash": doc_hash,
                "reference_number": ref_num,
                "file_content_base64": encoded_string,
                "created_at": datetime.datetime.utcnow(),
                "status": "DRAFTED",
            }

            result = self.db.documents.insert_one(document)
            logger.info("Document stored in 'blockchain' section: %s", result.inserted_id)
            return str(result.inserted_id)
        except Exception as exc:
            logger.error("Error storing document: %s", exc)
            return None

    def store_in_blockchain(
        self,
        user_key: str,
        username: Optional[str],
        pdf_path: str,
        original_filename: str,
    ) -> Optional[str]:
        """Inject a document into the Blockchain service's file_storage database.

        Args:
            user_key: Blockchain user identifier.
            username: Display name for the transaction.
            pdf_path: Path to the PDF file on disk.
            original_filename: Original uploaded filename.

        Returns:
            Generated file_key string, or None on failure.
        """
        if self.client is None:
            return None
        try:
            bc_db = self.client.get_database("file_storage")
            files_col = bc_db["files"]

            with open(pdf_path, "rb") as pdf_file:
                file_content = pdf_file.read()
                file_size = len(file_content)
                file_base64 = base64.b64encode(file_content).decode("utf-8")

            file_key = str(uuid.uuid4())
            unique_id = str(uuid.uuid4())[:8]
            secure_name = f"{int(time.time() * 1000)}_{unique_id}_{original_filename}"

            doc: Dict[str, Any] = {
                "file_key": file_key,
                "filename": original_filename,
                "secure_name": secure_name,
                "owner": user_key,
                "shared_with": [],
                "file_content": file_base64,
                "file_size": file_size,
                "created_at": time.time(),
            }

            files_col.insert_one(doc)
            logger.info("Document injected into Blockchain 'file_storage': %s", file_key)

            if BLOCKCHAIN_SERVICE_URL:
                try:
                    tx: Dict[str, Any] = {
                        "user": username or "NyaySetu_AI",
                        "v_file": original_filename,
                        "file_key": file_key,
                        "file_data": "Binary Content Stored in DB",
                        "file_size": file_size,
                    }
                    requests.post(
                        f"{BLOCKCHAIN_SERVICE_URL}/new_transaction",
                        json=tx,
                        timeout=2,
                    )
                    logger.info("Transaction announced to Blockchain service")
                except Exception as exc:
                    logger.warning("Could not announce to blockchain service: %s", exc)

            return file_key
        except Exception as exc:
            logger.error("Error injecting into Blockchain DB: %s", exc)
            return None

    def get_lifecycles(self) -> Dict[str, Any]:
        """Retrieve all lifecycle records from the database.

        Returns:
            Dictionary mapping document hash to lifecycle document.
        """
        if self.db is None:
            return {}
        try:
            cursor = self.db.lifecycles.find({})
            return {item["hash"]: item for item in cursor}
        except Exception:
            logger.exception("Failed to retrieve lifecycles")
            return {}

    def save_lifecycle(
        self,
        doc_hash: str,
        doc_type: str,
        metadata: Dict[str, Any],
        deadlines: Dict[str, Any],
    ) -> None:
        """Persist a document lifecycle record.

        Args:
            doc_hash: Unique document hash.
            doc_type: Type of document (e.g. RTI_Application, Affidavit).
            metadata: Arbitrary metadata attached to the document.
            deadlines: Deadline dictionary computed by DocumentLifecycle.
        """
        if self.db is None:
            return
        try:
            lifecycle: Dict[str, Any] = {
                "hash": doc_hash,
                "document_type": doc_type,
                "created_date": datetime.datetime.utcnow().isoformat(),
                "current_state": "DRAFTED",
                "state_history": [
                    {
                        "state": "DRAFTED",
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "notes": "Document generated",
                    }
                ],
                "metadata": metadata,
                "deadlines": deadlines,
                "last_updated": datetime.datetime.utcnow(),
            }
            self.db.lifecycles.update_one(
                {"hash": doc_hash},
                {"$set": lifecycle},
                upsert=True,
            )
        except Exception as exc:
            logger.error("Error saving lifecycle to DB: %s", exc)

    def update_lifecycle_state(
        self,
        doc_hash: str,
        new_state: str,
        notes: str,
    ) -> bool:
        """Update the current state of a document lifecycle.

        Args:
            doc_hash: Unique document hash.
            new_state: New lifecycle state string (e.g. SUBMITTED, CLOSED).
            notes: Optional human-readable note about the transition.

        Returns:
            True if the update succeeded, False otherwise.
        """
        if self.db is None:
            return False
        try:
            self.db.lifecycles.update_one(
                {"hash": doc_hash},
                {
                    "$set": {
                        "current_state": new_state,
                        "last_updated": datetime.datetime.utcnow(),
                    },
                    "$push": {
                        "state_history": {
                            "state": new_state,
                            "timestamp": datetime.datetime.utcnow().isoformat(),
                            "notes": notes,
                        }
                    },
                },
            )
            return True
        except Exception as exc:
            logger.error("Error updating lifecycle state: %s", exc)
            return False
