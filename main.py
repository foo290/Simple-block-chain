import json
from hashlib import sha256
from datetime import datetime


class Transaction:
    """
    A dummy replica of transaction to simulate blockchain concept
    """

    def __init__(self, sender, receiver, data, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.amount = amount
        self.timestamp = str(datetime.now())

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)


class Block(object):
    """
    This class represents a single block in block chain, contains all necessary details to be unique in entire
     blockchain.
    """

    def __init__(self, index, transactions: list, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = str(datetime.now())
        self.previous_hash = previous_hash
        self.nonce = nonce  # Number of tries took to get proof-of-work

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)


class Blockchain:
    """
    This class represents the blockchain and important methods for a blockchain to get going.
    """

    #  Number of zeros as prefix for proof-of-work
    DIFFICULTY = 3

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Genesis block is the origin of blockchain which has previous has of 0
        :return: None
        """
        genesis_block = Block(0, [{'transaction': 'Genesis Block'}], 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def show_chain(self):
        print(self.chain)

    @staticmethod
    def proof_of_work(block):
        """
        Calculates proof-of-work for a  block (a hash that has certain number of zeros as prefix) and assign the
         calculated hash to the block
        :param block: object of class Block
        :return: computed hash of the block according to proof-of-work
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.DIFFICULTY):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        """
        Adds a block into the main blockchain based on necessary checks
        :param block: block to be added
        :param proof: A computed hash that verifies proof-of-work standards
        :return: Bool, True if added successfully
        """
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def is_valid_proof(block, block_hash):
        """
        checks if block has valid proof-of-work hash and block hash assigned is same as computed and not altered.
        :param block: Block to be confirmed
        :param block_hash: hash of that block
        :return: Bool
        """
        return (block_hash.startswith('0' * Blockchain.DIFFICULTY) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction: Transaction):
        """
        Initially all transactions are added into unconfirmed transactions, which then mined later and added
        to the block chain
        :param transaction: object of class Transaction
        :return: None
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Main function that mines and validate transactions from unconfirmed transaction list.
        It creates new block based on transaction, calculates proof-of-work and if all checks out, then adds to
        blockchain
        :return: Index of the block added in block chain
        """
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=[json.loads(str(i)) for i in self.unconfirmed_transactions],
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.unconfirmed_transactions = []
        if self.add_block(new_block, proof):
            return new_block.index
        else:
            return False


if __name__ == '__main__':
    t1 = Transaction(
        sender="Nitin",
        receiver="somePizzaGuy",
        data="Transfer 8 bitcoins for a simple pizza xD",
        amount=8
    )
    t2 = Transaction(
        sender="SomeRandomDude",
        data="Transfer 80 bitcoins for a simple pizza xD",
        receiver="somePizzaGuy",
        amount=80
    )
    t3 = Transaction(
        sender="ThatGuy",
        data="Transfer 8 bitcoins for a simple pizza xD",
        receiver="somePizzaGuy",
        amount=8
    )
    t4 = Transaction(
        sender="AnotherSimp",
        data="Transfer 8 bitcoins for a simple pizza xD",
        receiver="somePizzaGuy",
        amount=8
    )

    blockchain = Blockchain()

    blockchain.add_new_transaction(t1)
    print(blockchain.mine())

    blockchain.add_new_transaction(t2)
    print(blockchain.mine())

    blockchain.add_new_transaction(t3)
    print(blockchain.mine())

    blockchain.add_new_transaction(t4)
    print(blockchain.mine())

    blockchain.show_chain()
