"""Blockchain module managing the chain, pending transactions, and consensus."""

import random
from typing import Any, List, Optional, Set, Union

import requests
from blockchain.Block import Block

from utils.logging_setup import setup_logging

logger = setup_logging(__name__)


class Blockchain:
    """Manages the block chain, pending transaction pool, and peer consensus.

    Implements proof-of-work mining with two nonce-generation strategies
    (random and incremental) and a longest-chain consensus algorithm.
    """

    difficulty: int = 3

    def __init__(self, db: Any = None) -> None:
        """Initialise the blockchain with a genesis block, syncing from DB if available.

        Args:
            db: Optional MongoDB database instance used for persistence.
        """
        self.pending: List[Any] = []
        self.chain: List[Block] = []
        self.peers: Set[str] = set()
        self.db = db

        loaded_chain = self.load_from_db() if self.db is not None else []

        if loaded_chain:
            self.chain = loaded_chain
            logger.info("Loaded blockchain from DB: %d blocks", len(self.chain))
        else:
            genesis = Block(0, [], "0")
            genesis.hash = genesis.generate_hash()
            self.chain.append(genesis)

            if self.db is not None:
                self.save_block_to_db(genesis)
                logger.info("Created and saved genesis block to DB")

    def load_from_db(self) -> List[Block]:
        """Deserialise the full chain from MongoDB.

        Returns:
            List of :class:`Block` instances sorted by index, or an empty
            list when the database is unavailable or contains no blocks.
        """
        if self.db is None:
            return []

        blocks_col = self.db["blocks"]
        cursor = blocks_col.find().sort("index", 1)

        chain: List[Block] = []
        for b_data in cursor:
            block = Block(
                b_data["index"],
                b_data["transactions"],
                b_data["prev_hash"],
            )
            block.timestamp = b_data.get("timestamp", block.timestamp)
            block.nonce = b_data.get("nonce", 0)
            block.hash = b_data.get("hash")
            chain.append(block)

        return chain

    def save_block_to_db(self, block: Block) -> None:
        """Persist a validated block to the MongoDB blocks collection.

        Duplicate indices are silently ignored.

        Args:
            block: The block to persist.
        """
        if self.db is None:
            return

        blocks_col = self.db["blocks"]
        if blocks_col.find_one({"index": block.index}):
            return

        blocks_col.insert_one({
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "prev_hash": block.prev_hash,
            "nonce": block.nonce,
            "hash": block.hash,
        })

    def add_block(self, block: Block, hashl: str) -> bool:
        """Append a validated block to the chain and persist it.

        The block is accepted only when its ``prev_hash`` matches the hash
        of the current last block **and** the block's own hash satisfies the
        proof-of-work difficulty requirement.

        Args:
            block: The block to append.
            hashl: The block's hash (must meet difficulty target).

        Returns:
            ``True`` if the block was added, ``False`` otherwise.
        """
        if self.last_block().hash == block.prev_hash and self.is_valid(block, hashl):
            block.hash = hashl
            self.chain.append(block)
            self.save_block_to_db(block)
            return True
        return False

    def mine(self) -> Union[int, bool]:
        """Mine pending transactions into a new block using proof-of-work.

        Returns:
            Index of the newly mined block, or ``False`` when there are no
            pending transactions.
        """
        if not self.pending:
            return False

        last_block = self.last_block()
        new_block = Block(last_block.index + 1, self.pending, last_block.hash)

        hashl = self.p_o_w(new_block)

        self.add_block(new_block, hashl)
        self.pending = []

        return new_block.index

    def p_o_w(self, block: Block) -> str:
        """Proof-of-work using random nonce generation.

        Random nonces provide better security and performance at higher
        difficulty levels compared to sequential scanning.

        Args:
            block: The block to mine.

        Returns:
            A hash string that starts with ``difficulty`` zeroes.
        """
        block.nonce = 0
        get_hash = block.generate_hash()

        while not get_hash.startswith("0" * Blockchain.difficulty):
            block.nonce = random.randint(0, 99_999_999)
            get_hash = block.generate_hash()

        return get_hash

    def p_o_w_2(self, block: Block) -> str:
        """Proof-of-work using incremental (sequential) nonce.

        Args:
            block: The block to mine.

        Returns:
            A hash string that starts with ``difficulty`` zeroes.
        """
        block.nonce = 0
        get_hash = block.generate_hash()

        while not get_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            get_hash = block.generate_hash()

        return get_hash

    def add_pending(self, transaction: Any) -> None:
        """Queue a transaction for inclusion in the next mined block.

        Args:
            transaction: Arbitrary transaction data.
        """
        self.pending.append(transaction)

    def check_chain_validity(self, chain: List[Block]) -> bool:
        """Verify that every block in *chain* is properly linked and valid.

        Each block's ``prev_hash`` must match the hash of the previous block,
        and every hash must satisfy the difficulty requirement.

        Args:
            chain: List of blocks to validate.

        Returns:
            ``True`` when the entire chain is valid, ``False`` otherwise.
        """
        result = True
        prev_hash = "0"

        for block in chain:
            block_hash = block.hash

            if self.is_valid(block, block.hash) and prev_hash == block.prev_hash:
                block.hash = block_hash
                prev_hash = block_hash
            else:
                result = False
                break

        return result

    def is_valid(self, block: Block, block_hash: str) -> bool:
        """Check whether *block_hash* meets the difficulty target and matches
        the block's recomputed hash.

        Args:
            block: The block whose hash to verify.
            block_hash: The candidate hash to check.

        Returns:
            ``True`` if the hash is valid, ``False`` otherwise.
        """
        if not block_hash.startswith("0" * Blockchain.difficulty):
            return False
        return block.generate_hash() == block_hash

    def last_block(self) -> Block:
        """Return the most recently appended block in the chain.

        Returns:
            The tail of the internal chain list.
        """
        return self.chain[-1]

    # ========== CONSENSUS MECHANISM ==========

    def register_peer(self, peer_address: str) -> None:
        """Add a peer node URL to the local peer set.

        Args:
            peer_address: URL of the peer (e.g. ``http://127.0.0.1:8801``).
        """
        self.peers.add(peer_address)

    def consensus(self) -> bool:
        """Longest-chain consensus: replace local chain with the longest
        valid chain discovered among registered peers.

        Returns:
            ``True`` if the local chain was replaced, ``False`` otherwise.
        """
        longest_chain: Optional[List[Block]] = None
        current_len = len(self.chain)

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/chain", timeout=2)
                if response.status_code != 200:
                    continue

                data = response.json()
                length = data["length"]
                chain_data = data["chain"]

                chain: List[Block] = []
                for block_data in chain_data:
                    block = Block(
                        block_data["index"],
                        block_data["transactions"],
                        block_data["prev_hash"],
                    )
                    block.timestamp = block_data.get("timestamp", block.timestamp)
                    block.nonce = block_data["nonce"]
                    block.hash = block_data["hash"]
                    chain.append(block)

                if length > current_len and self.check_chain_validity(chain):
                    current_len = length
                    longest_chain = chain

            except Exception as exc:
                logger.warning("Error connecting to peer %s: %s", peer, exc)

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    def announce_block(self, block: Block) -> None:
        """Broadcast a newly mined block to every registered peer.

        Args:
            block: The block to announce.
        """
        block_data = {
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "prev_hash": block.prev_hash,
            "nonce": block.nonce,
            "hash": block.hash,
        }

        for peer in self.peers:
            try:
                requests.post(f"{peer}/add_block", json=block_data, timeout=2)
            except Exception as exc:
                logger.warning("Error announcing block to %s: %s", peer, exc)
