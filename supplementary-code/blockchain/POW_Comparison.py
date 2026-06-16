"""Compare two proof-of-work algorithms (random vs incremental nonce).

Runs both algorithms at difficulty levels 2 through 5 and prints timing
results for each.
"""

import random
import string
import threading
from timeit import default_timer as timer
from typing import List, Optional

from blockchain.Block import Block
from blockchain.Blockchain import Blockchain
from utils.logging_setup import setup_logging

logger = setup_logging(__name__)

pow_run: List[Optional[float]] = []
pow2_run: List[Optional[float]] = []


def random_char(y: int) -> str:
    """Generate a random alphabetic string of length *y*.

    Args:
        y: Desired string length.

    Returns:
        Random string of lowercase ASCII letters.
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(y))


def add_transaction(block: Block) -> None:
    """Populate *block* with random transactions approximating real-world load.

    Uses the module-level ``transactions_length`` and ``transactions`` globals
    (set in the loop below). There is roughly a 10 % chance per iteration that
    a new transaction is generated and appended to the block.

    Args:
        block: The block to receive transactions.
    """
    global transactions_length
    global transactions

    for _ in range(transactions_length):
        if random.random() > 0.9:
            name = random_char(random.randint(0, 20))
            file_name = random_char(random.randint(0, 20))
            file_data = random_char(random.randint(0, 200))

            t = {
                "user": name,
                "v_file": file_name,
                "file_data": file_data,
                "file_size": random.randint(0, 1000),
            }

            block.add_t(t)


for j in range(2, 6):
    block_index = random.randint(0, 2000)
    transactions_length = random.randint(10, 20)
    transactions: List[dict] = []

    b = Block(block_index, transactions, "0")
    chain = Blockchain()
    Blockchain.difficulty = j

    new_thread = threading.Thread(target=add_transaction, args=(b,))
    new_thread.start()

    start = timer()
    logger.info(chain.p_o_w(b))
    end = timer()
    elapsed = end - start
    logger.info("POW elapsed: %s", elapsed)
    pow_run.insert(j, elapsed)

    start = timer()
    logger.info(chain.p_o_w_2(b))
    end = timer()
    elapsed = end - start
    logger.info("POW2 elapsed: %s", elapsed)
    pow2_run.insert(j, elapsed)

logger.info("------------Proof of Work with Random Nonce ------------")
for a in pow_run:
    if a is not None:
        logger.info("Difficulty %d  Time : %s", pow_run.index(a) + 2, round(a, 5))

logger.info("------------Proof of Work with Iterative Nonce ------------")
for a in pow2_run:
    if a is not None:
        logger.info("Difficulty %d  Time : %s", pow2_run.index(a) + 2, round(a, 5))

logger.info("------------Proof of Work with Random Nonce ------------")
for a in pow_run:
    if a is not None:
        logger.info(round(a, 5))

logger.info("------------Proof of Work with Iterative Nonce ------------")
for a in pow2_run:
    if a is not None:
        logger.info(round(a, 5))
