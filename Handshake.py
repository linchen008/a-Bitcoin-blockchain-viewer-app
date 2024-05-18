"""
Classes/utils for connecting to Bitcoin nodes
Protocol Documentation: https://en.bitcoin.it/wiki/Protocol_documentation
"""
import hashlib
from dataclasses import dataclass, field

from io import BytesIO

from Utils import encode_varint

MAGICS = {
    'main': b'\xf9\xbe\xb4\xd9',
    'test': b'\x0b\x11\x09\x07',
}


@dataclass
class NetworkEnvelope:
    command: bytes
    payload: bytes
    net: str

    def __repr__(self):
        return "[NetworkEnvelope] Command: %s, Payload: %s" % \
            (self.command.decode('ascii'), self.payload.hex())

    @classmethod
    def decode(cls, s, net):
        """ Construct a NetworkEnvelope from BytesIO stream s on a given net """
        magic = s.read(4)  # validate magic bytes
        assert magic != b'', "No magic bytes; Connection was reset?"
        assert magic == MAGICS[net]
        command = s.read(12)  # decode the command
        command = command.strip(b'\x00')
        # decode and validate the payload
        payload_length = int.from_bytes(s.read(4), 'little')
        checksum = s.read(4)
        payload = s.read(payload_length)
        assert checksum == hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

        print(f"Received {command.decode()} message: {payload.hex()}")
        return cls(command, payload, net)

    def encode(self):
        """ Encode this network message as bytes """
        out = []

        out += [MAGICS[self.net]]
        # encode the command
        assert len(self.command) <= 12
        out += [self.command]
        out += [b'\x00' * (12 - len(self.command))]  # command padding
        # encode the payload
        assert len(self.payload) <= 2 ** 32  # in practice reference client nodes will reject >= 32MB...
        out += [len(self.payload).to_bytes(4, 'little')]  # payload length
        out += [hashlib.sha256(hashlib.sha256(self.payload).digest()).digest()[:4]]  # checksum
        out += [self.payload]

        return b''.join(out)

    def stream(self):
        """ Stream the payload of this envelope """
        return BytesIO(self.payload)


# -----------------------------------------------------------------------------
# Specific types of commands and their payload encoder/decords follow
# -----------------------------------------------------------------------------

@dataclass
class NetAddrStruct:
    """
    reference: https://en.bitcoin.it/wiki/Protocol_documentation#Network_address
    currently assumes IPv4 address
    """
    services: int = 0
    ip: bytes = b'\x00\x00\x00\x00'  # IPv4 address
    port: int = 8333

    def encode(self):
        out = []
        # receiver services is 8 bytes little endian
        out += [self.services.to_bytes(8, 'little')]
        # IPV4 is 10 00 bytes and 2 ff bytes then receiver ip
        assert isinstance(self.ip, bytes) and len(self.ip) == 4
        out += [b'\x00' * 10 + b'\xff\xff' + self.ip]
        # receiver port is 2 bytes, big endian
        out += [self.port.to_bytes(2, 'big')]
        return b''.join(out)


@dataclass
class VersionMessage:
    """
    reference: https://en.bitcoin.it/wiki/Protocol_documentation#version
    When a node creates an outgoing connection, it will immediately advertise
    its version. The remote node will respond with its version. No further
    communication is possible until both peers have exchanged their version.
    """

    # header information
    version: int = 70015  # specifies what messages may be communicated
    services: int = 0  # info about what capabilities are available
    timestamp: int = None  # 8 bytes Unix timestamp in little-endian
    # receiver net_addr
    receiver: NetAddrStruct = field(default_factory=NetAddrStruct)
    # sender net_addr
    sender: NetAddrStruct = field(default_factory=NetAddrStruct)
    # additional metadata
    """
    uint64_t Node random nonce, randomly generated every time a version
    packet is sent. This nonce is used to detect connections to self.
    """
    nonce: bytes = None  # 8 bytes of nonce
    user_agent: bytes = None  # var_str: User Agent
    latest_block: int = 0  # "The last block received by the emitting node"
    relay: bool = False  # Whether the remote peer should announce relayed transactions or not, see BIP 0037
    command: str = field(init=False, default=b'version')

    @classmethod
    def decode(cls, s):
        # TODO. For now return a fixed default stub
        return cls()

    def encode(self):
        out = []

        # version is 4 bytes little endian
        out += [self.version.to_bytes(4, 'little')]
        # services is 8 bytes little endian
        out += [self.services.to_bytes(8, 'little')]
        # timestamp is 8 bytes little endian
        out += [self.timestamp.to_bytes(8, 'little')]
        # receiver
        out += [self.receiver.encode()]
        # sender
        out += [self.sender.encode()]
        # nonce should be 8 bytes
        assert isinstance(self.nonce, bytes) and len(self.nonce) == 8
        out += [self.nonce]
        # useragent is a variable string, so varint first
        assert isinstance(self.user_agent, bytes)
        out += [encode_varint(len(self.user_agent))]
        out += [self.user_agent]

        # latest block is 4 bytes little endian
        out += [self.latest_block.to_bytes(4, 'little')]
        # relay is 00 if false, 01 if true
        out += [b'\x01' if self.relay else b'\x00']

        return b''.join(out)


@dataclass
class VerAckMessage:
    """
    https://en.bitcoin.it/wiki/Protocol_documentation#verack
    The verack message is sent in reply to version. This message
    consists of only a message header with the command string "verack".
    """
    command: str = field(init=False, default=b'verack')

    @classmethod
    def decode(cls, s):
        return cls()

    def encode(self):
        return b''


@dataclass
class PingMessage:
    """
    https://en.bitcoin.it/wiki/Protocol_documentation#ping
    The ping message is sent primarily to confirm that the TCP/IP
    connection is still valid. An error in transmission is presumed
    to be a closed connection and the address is removed as a current peer.
    """
    nonce: bytes
    command: str = field(init=False, default=b'ping')

    @classmethod
    def decode(cls, s):
        nonce = s.read(8)
        return cls(nonce)

    def encode(self):
        return self.nonce


@dataclass
class PongMessage:
    """
    https://en.bitcoin.it/wiki/Protocol_documentation#pong
    The pong message is sent in response to a ping message.
    In modern protocol versions, a pong response is generated
    using a nonce included in the ping.
    """
    nonce: bytes
    command: str = field(init=False, default=b'pong')

    @classmethod
    def decode(cls, s):
        nonce = s.read(8)
        return cls(nonce)

    def encode(self):
        return self.nonce