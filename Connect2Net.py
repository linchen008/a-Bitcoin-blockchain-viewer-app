import hashlib
import socket
from dataclasses import dataclass
from typing import List

from Handshake import NetworkEnvelope, VersionMessage, VerAckMessage, PongMessage, PingMessage
from Utils import encode_varint, decode_varint


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
        self.stream = self.socket.makefile('rb', None)

    def send(self, message):
        env = NetworkEnvelope(message.command, message.encode(), net=self.net)
        if self.verbose:
            print(f"sending: {env}")
        self.socket.sendall(env.encode())

    def read(self):
        env = NetworkEnvelope.decode(self.stream, net=self.net)
        if self.verbose:
            print(f"receiving: {env}")
        return env
    
    def process_message(self, env):
            # Decode and print the message
            if self.verbose:
                print(f"Processing message: {env}")
            # further decoding

    def listen_forever(self):
        try:
            while True:
                message = self.read()
                # Optionally process and print the message based on its type
                self.process_message(message)
        except Exception as e:
            print(f"Stopped listening due to error: {e}")
        finally:
            self.socket.close()
            print("Connection closed.")

    def wait_for(self, *message_classes):
        command = None
        command_to_class = {m.command: m for m in message_classes}

        # loop until one of the desired commands is encountered
        while command not in command_to_class:
            env = self.read()
            command = env.command

            # respond to Version with VerAck
            if command == VersionMessage.command:
                self.send(VerAckMessage())

            # respond to Ping with Pong
            elif command == PingMessage.command:
                self.send(PongMessage(env.payload))

        # return the parsed message
        print(command_to_class[command].decode(env.stream()))
        return command_to_class[command].decode(env.stream())

    def handshake(self):
        version = VersionMessage(
            timestamp=0,
            nonce=b'\x00' * 8,
            user_agent=b'/programmingbitcoin:0.1/',
        )
        print(version)
        self.send(version)
        self.wait_for(VersionMessage)
        self.wait_for(VerAckMessage)
        self.send(VerAckMessage())
        print("Connection established")
        self.listen_forever()

    def close(self):
        self.socket.close()

