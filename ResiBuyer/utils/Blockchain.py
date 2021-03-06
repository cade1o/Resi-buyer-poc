import json
import time
from hashlib import sha256


class Block:
    def __init__(self, index, data, timestamp, previous_hash):
        """
        Constructor for the `Block` class.
        :param index:         Unique ID of the block.
        :param data:          List of transactions.
        :param timestamp:     Time of generation of the block.
        :param previous_hash: Hash of the previous block in the chain which this block is part of.                                        
        """
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash # Adding the previous hash field

    def compute_hash(self):
        """
        Returns the hash of the block instance by first converting it
        into JSON string.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True) # The string equivalent also considers the previous_hash field now
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_data = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, "NULL", 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def last_tx(self):
        return self.unconfirmed_data[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash
        
        if previous_hash == proof:
            return False

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        self.unconfirmed_data = []
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_data(self, data):
        self.unconfirmed_data.append(data)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        if(block_hash.startswith('0' * Blockchain.difficulty)):
            print("Block Hash has work")
        else:
            print("Work Not Compatible")

        if(block_hash == block.compute_hash()):
            print("Hashes the Same")
        else:
            print("Hash Given: {}, Hash Produced: {}".format(block_hash, block.compute_hash()))
        
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        data to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_data:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          data=self.unconfirmed_data,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        return True

    def set_chain(self, new_chain):
        self.chain = new_chain
