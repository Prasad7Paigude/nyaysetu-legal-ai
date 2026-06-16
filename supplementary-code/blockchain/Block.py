"""Block module representing a single block in the NyaySetu blockchain."""

import time
import json
from hashlib import sha256
from typing import Any, List, Optional


class Block:
    """Represents a single block in the blockchain.

    Each block contains an index, timestamp, list of transactions,
    the previous block's hash, a nonce for proof-of-work, and its own hash.
    Multiple linked blocks form a blockchain.
    """

    def __init__(self, index: int, transactions: List[Any], prev_hash: str) -> None:
        """Initialize a new block.

        Args:
            index: Position of the block in the chain.
            transactions: List of transactions or file metadata dicts.
            prev_hash: Hash of the preceding block in the chain.
        """
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp: float = time.time()
        self.nonce: int = 0
        self.hash: Optional[str] = None

    def generate_hash(self) -> str:
        """Compute the SHA-256 hash of this block's contents.

        Serialises index, timestamp, transactions, prev_hash and nonce
        into a JSON string (sorted keys) and returns the hex digest.

        Returns:
            Hexadecimal SHA-256 hash string.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
        }, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def compute_hash(self) -> str:
        """Alias for :meth:`generate_hash` provided for compatibility.

        Returns:
            Hexadecimal SHA-256 hash string.
        """
        return self.generate_hash()

    def add_t(self, transaction: Any) -> None:
        """Append a transaction to this block's transaction list.

        Args:
            transaction: Arbitrary transaction data to add.
        """
        self.transactions.append(transaction)

    def __dict__(self) -> dict:
        """Return a JSON-serialisable dictionary representation of the block.

        Returns:
            Dict with keys index, timestamp, transactions, prev_hash,
            nonce and hash.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }
