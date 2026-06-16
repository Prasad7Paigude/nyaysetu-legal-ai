"""Flask routes for the NyaySetu file-storage application.

Provides user registration, file upload/sharing/download, blockchain peer
endpoints, and integration with the local blockchain node.
"""

import base64
import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from dotenv import load_dotenv
from flask import (
    Flask, jsonify, redirect, render_template, request,
    send_file, session, url_for,
)
from flask_cors import CORS
from pymongo import MongoClient
from timeit import default_timer as timer
from werkzeug.utils import secure_filename

from blockchain.app import app
from blockchain.Block import Block
from blockchain.Blockchain import Blockchain as BlockchainClass
from config.settings import BLOCKCHAIN_NODE_ADDR, MONGODB_URI, SECRET_KEY
from utils.logging_setup import setup_logging

logger = setup_logging(__name__)

dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
)
load_dotenv(dotenv_path)

app.secret_key = SECRET_KEY

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "expose_headers": ["Content-Type"],
    },
})

client = MongoClient(MONGODB_URI)  # type: ignore[arg-type]
db = client["file_storage"]
users_col = db["users"]
files_col = db["files"]

blockchain = BlockchainClass(db=db)

request_tx: List[Dict[str, Any]] = []
files: Dict[str, Any] = {}
UPLOAD_FOLDER = "app/static/Uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ADDR: str = BLOCKCHAIN_NODE_ADDR


def get_tx_req() -> None:
    """Populate the global ``request_tx`` list with all transactions from the
    local blockchain, sorted most-recent-first.
    """
    global request_tx
    try:
        content: List[Dict[str, Any]] = []
        for block in blockchain.chain:
            for trans in block.transactions:
                trans_copy = trans.copy()
                trans_copy["index"] = block.index
                trans_copy["hash"] = block.prev_hash
                content.append(trans_copy)
        request_tx = sorted(content, key=lambda k: k["hash"], reverse=True)
    except Exception as exc:
        logger.error("Error in get_tx_req: %s", exc)
        request_tx = []


@app.route("/")
def index() -> str:
    """Render the home page with user files and recent transactions.

    Returns:
            Rendered HTML template.
    """
    get_tx_req()
    user_key: Optional[str] = session.get("user_key")
    username: Optional[str] = session.get("username")

    my_files: List[Dict[str, str]] = []
    if user_key:
        try:
            cursor = files_col.find({"owner": user_key})
            for f_data in cursor:
                my_files.append({
                    "filename": f_data["filename"],
                    "file_key": f_data["file_key"],
                })
        except Exception as exc:
            logger.error("Error fetching user files: %s", exc)

    return render_template(
        "index.html",
        title="FileStorage",
        subtitle="A Decentralized Network for File Storage/Sharing",
        node_address=ADDR,
        request_tx=request_tx,
        user_key=user_key,
        username=username,
        my_files=my_files,
    )


@app.route("/api/get_key/<string:username>", methods=["GET"])
def get_key(username: str) -> Tuple[Union[str, dict], int]:
    """Return the API key for a given username.

    Args:
        username: The registered username.

    Returns:
        JSON with ``user_key`` or 404 error.
    """
    try:
        user = users_col.find_one({"username": username})
        if user:
            return jsonify({"user_key": user["key"]})
    except Exception as exc:
        logger.error("Error fetching key for %s: %s", username, exc)
    return jsonify({"error": "User not found"}), 404


@app.route("/register", methods=["POST"])
def register() -> Union[str, Tuple[Union[str, dict], int]]:
    """Register a new user or retrieve the existing user's key.

    Stores the user's key and username in the Flask session.

    Returns:
        Redirect to home page on success.
    """
    username: str = request.form["username"]
    logger.debug("Registering user: %s", username)

    try:
        user = users_col.find_one({"username": username})
    except Exception as exc:
        logger.error("DB error during register: %s", exc)
        return redirect("/")

    if user:
        logger.debug("User found. Key: %s", user["key"])
        session["user_key"] = user["key"]
        session["username"] = username
    else:
        logger.debug("User NOT found. Creating new key.")
        new_key = str(uuid.uuid4())
        try:
            users_col.insert_one({"username": username, "key": new_key})
        except Exception as exc:
            logger.error("DB error creating user: %s", exc)
            return redirect("/")
        session["user_key"] = new_key
        session["username"] = username
        logger.debug("New key generated: %s", new_key)

    return redirect("/")


@app.route("/logout")
def logout() -> Union[str, Tuple[Union[str, dict], int]]:
    """Clear the Flask session and redirect to home."""
    session.clear()
    return redirect("/")


@app.route("/submit", methods=["POST"])
def submit() -> Tuple[Union[str, dict], int]:
    """Accept a file upload, persist it, and queue a blockchain transaction.

    Form fields:
        - userKey (required)
        - username (optional)
        - v_file (file, required)

    Returns:
        JSON with success status and the generated ``file_key``.
    """
    user_key = request.form.get("userKey")
    username_from_form = request.form.get("username")

    if not user_key:
        logger.warning("No userKey in form data during submit")
        return jsonify({"error": "Missing userKey"}), 400

    start = timer()
    user = username_from_form or session.get("username", "unknown")
    logger.debug("Submitting file for user: %s, Key: %s", user, user_key)

    up_file = request.files.get("v_file")

    if not up_file or up_file.filename == "":
        return jsonify({"error": "No file provided"}), 400

    try:
        file_content = up_file.read()
    except Exception as exc:
        logger.error("Error reading uploaded file: %s", exc)
        return jsonify({"error": "Failed to read file"}), 500

    file_size = len(file_content)

    timestamp = int(timer() * 1000)
    unique_id = str(uuid.uuid4())[:8]
    original_filename = up_file.filename
    secure_name = f"{timestamp}_{unique_id}_{secure_filename(original_filename)}"

    upload_path = os.path.join("app/static/Uploads/", secure_name)
    try:
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        with open(upload_path, "wb") as f:
            f.write(file_content)
    except Exception as exc:
        logger.error("Error saving file to disk: %s", exc)
        return jsonify({"error": "Failed to save file"}), 500

    file_key = str(uuid.uuid4())
    file_base64 = base64.b64encode(file_content).decode("utf-8")

    try:
        files_col.insert_one({
            "file_key": file_key,
            "filename": original_filename,
            "secure_name": secure_name,
            "owner": user_key,
            "shared_with": [],
            "file_content": file_base64,
            "file_size": file_size,
            "created_at": timer(),
        })
    except Exception as exc:
        logger.error("Error saving file metadata to DB: %s", exc)
        return jsonify({"error": "Failed to persist file metadata"}), 500

    logger.debug("File saved to MongoDB. FileKey: %s, Owner: %s", file_key, user_key)

    post_object = {
        "user": user,
        "v_file": original_filename,
        "file_key": file_key,
        "file_data": "Binary Content Stored in DB",
        "file_size": file_size,
    }

    blockchain.add_pending(post_object)
    logger.debug("Transaction added to blockchain pending transactions")

    end = timer()
    logger.debug("Upload completed in %ss", end - start)
    return jsonify({"success": True, "message": "File uploaded successfully", "file_key": file_key}), 200


@app.route("/share", methods=["POST"])
def share_file() -> Tuple[Union[str, dict], int]:
    """Share a file with another user by adding their key to the
    ``shared_with`` list in MongoDB.

    Form fields:
        - file_key (required)
        - recipient_key (required)
        - userKey (optional, falls back to session)

    Returns:
        JSON with success status.
    """
    file_key = request.form.get("file_key")
    recipient_key = request.form.get("recipient_key")
    owner_key = request.form.get("userKey") or session.get("user_key")

    if not file_key or not recipient_key or not owner_key:
        return jsonify({"error": "Missing required fields"}), 400

    logger.debug("Sharing file %s from %s to %s", file_key, owner_key, recipient_key)

    try:
        result = files_col.update_one(
            {"file_key": file_key, "owner": owner_key},
            {"$addToSet": {"shared_with": recipient_key}},
        )
    except Exception as exc:
        logger.error("DB error during share: %s", exc)
        return jsonify({"error": "Database error"}), 500

    if result.matched_count == 0:
        logger.warning("File not found or not owned by %s", owner_key)
        return jsonify({"error": "File not found or not owned by you"}), 404

    if result.modified_count > 0:
        logger.debug("File shared successfully")
        return jsonify({"success": True, "message": "File shared successfully"}), 200

    logger.debug("File already shared with this user")
    return jsonify({"success": True, "message": "File already shared with this user"}), 200


@app.route("/view_shared", methods=["POST"])
def view_shared() -> Tuple[Union[str, dict], int]:
    """Return all files that *sender_key* has shared with the current user.

    Form fields:
        - sender_key (required)
        - userKey (optional, falls back to session)

    Returns:
        JSON list of shared files or rendered HTML.
    """
    sender_key = request.form.get("sender_key")
    my_key = request.form.get("userKey") or session.get("user_key")

    if not sender_key or not my_key:
        return jsonify({"error": "Missing sender_key or userKey"}), 400

    shared_files: List[Dict[str, str]] = []

    try:
        cursor = files_col.find({"owner": sender_key, "shared_with": my_key})
        for f_val in cursor:
            shared_files.append({
                "filename": f_val["filename"],
                "file_key": f_val["file_key"],
                "secure_name": f_val["secure_name"],
            })
    except Exception as exc:
        logger.error("Error querying shared files: %s", exc)
        return jsonify({"error": "Database error"}), 500

    if request.form.get("userKey"):
        return jsonify({"files": shared_files}), 200

    return render_template("shared_files.html", files=shared_files), 200


@app.route("/download/<string:file_key>", methods=["GET"])
def download_file_key(file_key: str) -> Tuple[Union[str, Any], int]:
    """Download a file identified by its unique key.

    If the file is missing from disk it will be restored from the MongoDB
    ``file_content`` field.

    Args:
        file_key: Unique identifier of the file.

    Returns:
        File attachment or an error string.
    """
    try:
        f_data = files_col.find_one({"file_key": file_key})
    except Exception as exc:
        logger.error("DB error during file lookup: %s", exc)
        return "Database error", 500

    if not f_data:
        return "File not found or access denied", 404

    p = os.path.join(app.root_path, "static", "Uploads", f_data["secure_name"])

    if not os.path.exists(p):
        logger.debug("File %s missing from disk. Restoring from MongoDB.", p)
        if "file_content" in f_data:
            try:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                content = base64.b64decode(f_data["file_content"])
                with open(p, "wb") as f:
                    f.write(content)
            except Exception as exc:
                logger.error("Error restoring file: %s", exc)
                return "Error restoring file from cloud storage", 500
        else:
            return "File content not found in database", 404

    return send_file(p, as_attachment=True, download_name=f_data["filename"]), 200


@app.route("/submit/<string:variable>", methods=["GET"])
def download_file(variable: str) -> Any:
    """Download a file by its secured filename.

    Args:
        variable: Secured filename on disk.

    Returns:
        File attachment.
    """
    p = os.path.join(app.root_path, "static", "Uploads", secure_filename(variable))
    return send_file(p, as_attachment=True)


# ========== BLOCKCHAIN PEER ROUTES (merged from peer.py) ==========


@app.route("/new_transaction", methods=["POST"])
def new_transaction() -> Tuple[str, int]:
    """Accept a new transaction via JSON and add it to the pending pool.

    Required fields: ``user``, ``v_file``, ``file_data``, ``file_size``.
    """
    file_data = request.get_json()
    required_fields = ["user", "v_file", "file_data", "file_size"]

    for field in required_fields:
        if not file_data.get(field):
            return "Transaction does not have valid fields!", 404

    blockchain.add_pending(file_data)
    return "Success", 201


@app.route("/chain", methods=["GET"])
def get_chain() -> str:
    """Return the full blockchain as a JSON string."""
    chain = [block.__dict__() for block in blockchain.chain]
    logger.info("Chain Len: %d", len(chain))
    return json.dumps({"length": len(chain), "chain": chain})


@app.route("/mine", methods=["GET"])
def mine_unconfirmed_transactions() -> str:
    """Mine pending transactions into a new block."""
    result = blockchain.mine()
    if result:
        return f"Block #{result} mined successfully."
    return "No pending transactions to mine."


@app.route("/pending_tx")
def get_pending_tx() -> str:
    """Return the list of pending transactions as JSON."""
    return json.dumps(blockchain.pending)


@app.route("/add_block", methods=["POST"])
def validate_and_add_block() -> Tuple[str, int]:
    """Receive a block from a peer and add it to the local chain if valid."""
    block_data = request.get_json()

    block = Block(
        block_data["index"],
        block_data["transactions"],
        block_data["prev_hash"],
    )
    hashl = block_data["hash"]

    added = blockchain.add_block(block, hashl)

    if not added:
        return "The Block was discarded by the node.", 400

    return "The block was added to the chain.", 201
