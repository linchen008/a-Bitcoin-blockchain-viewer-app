import time
from dataclasses import dataclass, field
from typing import List

from Utils import decode_varint, encode_int, encode_varint


@dataclass
class GetDataMessage:
    items: List[tuple]  # Same structure as InvMessage
    command: bytes = field(init=False, default=b'getdata')  # Add the default command attribute

    def encode(self):
        out = [encode_varint(len(self.items))]
        for item_type, item_hash in self.items:
            out += [encode_int(item_type, 4)]
            out += [item_hash]
        return b''.join(out)


@dataclass
class InvMessage:
    items: List[tuple]  # List of (type, hash) tuples indicating the inventory
    command: bytes = field(init=False, default=b'inv')

    @classmethod
    # Decode inv messages from byte streams
    def parse(cls, s):
        count = decode_varint(s)  # Read inventory item count
        items = []
        for _ in range(count):
            inv_type = int.from_bytes(s.read(4), 'little')  # Retrieve inventory item type
            inv_hash = s.read(32)  # Read inventory item hash
            items.append((inv_type, inv_hash))
        return cls(items)

    def encode(self):  # Encoding inv messages into byte streams
        out = [encode_varint(len(self.items))]
        for inv_type, inv_hash in self.items:
            out += [encode_int(inv_type, 4)]
            out += [inv_hash]
        return b''.join(out)


def decode_script(s):
    length = decode_varint(s)
    return s.read(length)


@dataclass
class Input:
    prevout_hash: bytes
    prevout_index: int
    script_sig: bytes
    sequence: int

    @classmethod
    def decode(cls, s):
        prevout_hash = s.read(32)  # Transaction hash, 32 bytes
        prevout_index = int.from_bytes(s.read(4), 'little')  # Output index, 4 bytes
        script_sig = decode_script(s)  # Unlocking Scripts
        sequence = int.from_bytes(s.read(4), 'little')  # product key
        return cls(prevout_hash, prevout_index, script_sig, sequence)


@dataclass
class Output:
    value: int  # Value in satoshis
    script_pubkey: bytes

    @classmethod
    def decode(cls, s):
        value = int.from_bytes(s.read(8), 'little')  # Amount, 8 bytes
        script_pubkey = decode_script(s)  # Lock Script
        return cls(value, script_pubkey)

    def btc_value(self):
        """ Convert satoshi to BTC """
        return self.value / 100_000_000


@dataclass
class TxMessage:
    version: int
    inputs: List[Input]
    outputs: List[Output]
    locktime: int

    @classmethod
    def parse(cls, s):
        version = int.from_bytes(s.read(4), 'little')
        num_inputs = decode_varint(s)
        inputs = [Input.decode(s) for _ in range(num_inputs)]
        num_outputs = decode_varint(s)
        outputs = [Output.decode(s) for _ in range(num_outputs)]
        locktime = int.from_bytes(s.read(4), 'little')
        return cls(version, inputs, outputs, locktime)

    def print_TXreadable(self):
        version, inputs, outputs, lock_time = self.version, self.inputs, self.outputs, self.locktime
        total_value = sum(output.value for output in outputs)
        print("Transaction Information:")
        print(f"  Version: {version}")
        print(f"  Locktime: {lock_time}")
        print(f"  Number of Inputs: {len(inputs)}")
        print(f"  Number of Outputs: {len(outputs)}")
        print(f"  Total Output Value: {total_value / 100_000_000:.8f} BTC")
        print("  Transaction Inputs:")
        for i, input in enumerate(inputs):
            print(f"    Input {i + 1}:")
            print(f"      Previous Output Hash: {input.prevout_hash.hex()}")
            print(f"      Output Index: {input.prevout_index}")
            print(f"      ScriptSig: {input.script_sig.hex()}")
        print("  Transaction Outputs:")
        for i, output in enumerate(outputs):
            print(f"    Output {i + 1}:")
            print(f"      Value: {output.value} Satoshis ({output.btc_value()} BTC)")
            print(f"      ScriptPubKey: {output.script_pubkey.hex()}")


@dataclass
class BlockMessage:
    version: int
    prev_block: bytes
    merkle_root: bytes
    timestamp: int
    bits: int
    nonce: int
    transactions: List[TxMessage]

    @classmethod
    def parse(cls, s):
        version = int.from_bytes(s.read(4), 'little')
        prev_block = s.read(32)
        merkle_root = s.read(32)
        timestamp = int.from_bytes(s.read(4), 'little')
        bits = int.from_bytes(s.read(4), 'little')
        nonce = int.from_bytes(s.read(4), 'little')
        count = decode_varint(s)
        transactions = [TxMessage.parse(s) for _ in range(count)]
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce, transactions)

    def print_blockReadable(self):
        print("Block Information:")
        print(f"  Version: {self.version}")
        print(f"  Previous Block Hash: {self.prev_block[::-1].hex()}")
        print(f"  Merkle Root: {self.merkle_root.hex()}")
        print(f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.timestamp))}")
        print(f"  Bits: {self.bits} (Difficulty: {self.calculate_difficulty()})")
        print(f"  Nonce: {self.nonce}")
        print(f"  Number of Transactions: {len(self.transactions)}")
        for tx in self.transactions:
            tx.print_TXreadable()

    def calculate_difficulty(self):
        # This method converts 'bits' into a full target and then calculates the difficulty
        exponent = (self.bits >> 24)
        mantissa = self.bits & 0x007fffff

        # Calculate the full target based on the mantissa and exponent
        if exponent <= 3:
            target = mantissa >> (8 * (3 - exponent))
        else:
            target = mantissa << (8 * (exponent - 3))

        # Genesis block target based on '0x1d00ffff'
        genesis_block_target = 0x00000000FFFF * (2 ** (8 * (0x1d - 3)))

        # Calculate difficulty as a ratio of genesis target to current target
        if target == 0:
            return float('inf')  # To avoid division by zero, though it should never happen
        return genesis_block_target / target
