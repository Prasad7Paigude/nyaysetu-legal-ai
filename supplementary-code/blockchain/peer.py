"""Blockchain peer node – Flask REST API for transaction and consensus operations."""

import argparse
from typing import Tuple, Union

from flask import Flask, request, jsonify

from blockchain.Block import Block
from blockchain.Blockchain import Blockchain
from utils.logging_setup import setup_logging

logger = setup_logging(__name__)

app = Flask(__name__)

blockchain = Blockchain()

peer_port: int = 8800


@app.route("/new_transaction", methods=["POST"])
def new_transaction() -> Tuple[Union[str, dict], int]:
    """Accept a new transaction and add it to the pending pool.

    Required JSON body fields:
        - user
        - v_file
        - file_data
        - file_size

    Returns:
        JSON response with status 201 on success, 400 on missing fields.
    """
    file_data = request.get_json()
    required_fields = ["user", "v_file", "file_data", "file_size"]

    for field in required_fields:
        if not file_data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    blockchain.add_pending(file_data)
    return jsonify({"message": "Transaction added to pending"}), 201


@app.route("/chain", methods=["GET"])
def get_chain() -> Tuple[Union[str, dict], int]:
    """Return the full blockchain after running consensus.

    Returns:
        JSON object with ``length`` and ``chain`` (list of block dicts).
    """
    blockchain.consensus()

    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__())

    logger.info("Chain Len: %d", len(chain))

    return jsonify({"length": len(chain), "chain": chain})


@app.route("/mine", methods=["GET"])
def mine_unconfirmed_transactions() -> Tuple[Union[str, dict], int]:
    """Mine all pending transactions and announce the new block to peers.

    Returns:
        JSON with success message and block index, or a message indicating
        there were no pending transactions.
    """
    result = blockchain.mine()

    if result:
        new_block = blockchain.chain[result]
        blockchain.announce_block(new_block)
        return jsonify({
            "message": f"Block #{result} mined successfully",
            "index": result,
            "hash": new_block.hash,
        }), 200

    return jsonify({"message": "No pending transactions to mine"}), 200


@app.route("/pending_tx")
def get_pending_tx() -> Tuple[Union[str, dict], int]:
    """Return all currently pending transactions."""
    return jsonify({
        "count": len(blockchain.pending),
        "transactions": blockchain.pending,
    })


@app.route("/add_block", methods=["POST"])
def validate_and_add_block() -> Tuple[Union[str, dict], int]:
    """Receive a block from a peer and add it to the chain if valid.

    Returns:
        201 on success, 400 if the block was rejected.
    """
    block_data = request.get_json()

    block = Block(
        block_data["index"],
        block_data["transactions"],
        block_data["prev_hash"],
    )
    block.timestamp = block_data.get("timestamp", block.timestamp)
    block.nonce = block_data["nonce"]
    hashl = block_data["hash"]

    added = blockchain.add_block(block, hashl)

    if not added:
        return jsonify({"message": "Block discarded by node"}), 400

    return jsonify({"message": "Block added to chain"}), 201


@app.route("/register_node", methods=["POST"])
def register_node() -> Tuple[Union[str, dict], int]:
    """Register a new peer and return the current chain for syncing.

    Request body should contain ``node_address`` (e.g.
    ``http://127.0.0.1:8801``).

    Returns:
        JSON with registration message, total peer count, and the chain.
    """
    node_address = request.get_json().get("node_address")

    if not node_address:
        return jsonify({"error": "Missing node_address"}), 400

    blockchain.register_peer(node_address)

    chain = [block.__dict__() for block in blockchain.chain]

    return jsonify({
        "message": "Node registered successfully",
        "total_peers": len(blockchain.peers),
        "chain": chain,
    }), 201


@app.route("/sync_chain", methods=["GET"])
def sync_chain() -> Tuple[Union[str, dict], int]:
    """Force re-synchronisation with all peers via consensus.

    Returns:
        JSON indicating whether the chain was replaced or is already up to
        date.
    """
    replaced = blockchain.consensus()

    if replaced:
        return jsonify({
            "message": "Chain replaced with longer chain from network",
            "length": len(blockchain.chain),
        }), 200

    return jsonify({
        "message": "Chain is up to date",
        "length": len(blockchain.chain),
    }), 200


@app.route("/peers", methods=["GET"])
def get_peers() -> Tuple[Union[str, dict], int]:
    """Return the set of registered peer node URLs."""
    return jsonify({
        "count": len(blockchain.peers),
        "peers": list(blockchain.peers),
    })


@app.route("/info", methods=["GET"])
def get_info() -> Tuple[Union[str, dict], int]:
    """Return summary blockchain information."""
    return jsonify({
        "port": peer_port,
        "chain_length": len(blockchain.chain),
        "pending_transactions": len(blockchain.pending),
        "difficulty": blockchain.difficulty,
        "peers": len(blockchain.peers),
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run blockchain peer node")
    parser.add_argument("--port", type=int, default=8800, help="Port to run peer on")
    args = parser.parse_args()

    peer_port = args.port

    logger.info("Starting blockchain peer on port %d", peer_port)
    logger.info("Difficulty: %d", blockchain.difficulty)
    logger.info("Genesis block hash: %s", blockchain.chain[0].hash)

    app.run(host="0.0.0.0", port=peer_port, debug=True)
