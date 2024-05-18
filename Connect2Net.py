import hashlib
import socket
import struct
from dataclasses import dataclass, field
from typing import List

from Handshake import NetworkEnvelope, PingMessage, PongMessage, VersionMessage, VerAckMessage
from MessageHandler import GetDataMessage, InvMessage, TxMessage, BlockMessage


class SimpleNode:
    def __init__(self, host: str, net: str, verbose: int = 0):
        self.net = net
        self.verbose = verbose

        # DNS resolution of the host name
        resolved_ip = socket.gethostbyname(host)
        port = {'main': 8333, 'test': 18333}[net]

        # Set up the socket connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((resolved_ip, port))
        print("Connected to Bitcoin node at {}:{}".format(resolved_ip, port))
        self.stream = self.socket.makefile('rb', None)

    def send(self, message):
        env = NetworkEnvelope(message.command, message.encode(), net=self.net)
        if self.verbose:
            print(f"sending: {env}")
        self.socket.sendall(env.encode())

    def read(self):
        env = NetworkEnvelope.decode(self.stream, net=self.net)
        # print("Received message:", env)

        return env

    def handle_inv(self, inv):
        getdata_items = [(type, hash) for type, hash in inv.items if type in [1, 2]]  # 1 for TX, 2 for Block
        if getdata_items:
            getdata = GetDataMessage(getdata_items)
            self.send(getdata)

    def listen_message(self):
        version = VersionMessage(
            timestamp=0,
            nonce=b'\x00' * 8,
            user_agent=b'/programmingbitcoin:0.1/',
        )
        self.send(version)  # Send a version message
        try:
            # Call the appropriate handler function according to the message type
            while True:
                env = NetworkEnvelope.decode(self.stream, net=self.net)  # Reading a message from the network
                command = env.command

                # respond to Version with VerAck
                if command == VersionMessage.command:
                    self.send(VerAckMessage())  # Send verack message

                    print("Connection established!")

                elif env.command == PingMessage.command:
                    self.send(PongMessage(env.payload))  # Responding to Ping Messages
                    print("Sent Pong")

                elif env.command == InvMessage.command:
                    inv = InvMessage.parse(env.stream()) # Parsing Inv messages
                    print("Received Inventory: ", inv)
                    self.handle_inv(inv)

                elif env.command == b'tx':
                    tx = TxMessage.parse(env.stream())
                    TxMessage.print_TXreadable(tx)  # Parsing Tx Messages

                elif env.command == b'block':
                    block = BlockMessage.parse(env.stream())
                    BlockMessage.print_blockReadable(block)  # Parsing Block Messages

        except Exception as e:
            print(f"Stopped listening due to error: {e}")
        finally:
            self.socket.close()
            print("Connection closed.")

    def close(self):
        self.socket.close()
