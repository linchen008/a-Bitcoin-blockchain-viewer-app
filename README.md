# a-Bitcoin-blockchain-viewer-application
This project demonstrates basic interactions with a Bitcoin node using Python. It provides a simplified framework for connecting to Bitcoin nodes, sending and receiving messages, and parsing blockchain data.
## Overvie
The script connects to a Bitcoin node, sends a handshake, listens for messages, and interacts with blockchain data. It includes functionality to decode transaction and block information from the node's responses.
## Dependencies
- Python 3.12+
- `socket` for network connections
## Installation
To run this project, clone the repo and install the required Python packages:
## Usage
Execute the main script to start interacting with a Bitcoin node:
`python main.py`
## Architecture Overview
The codebase is split into multiple modules:
`main.py`: Initializes the connection with Bitcoin node Domain.
`Connect2Net.py`: Handles network connections and message handling logic.
`Handshake.py`: Handshake with Bitcoin Node, Contains utility classes for encoding/decoding network messages.
`MessageHandler.py`: Encodes and decodes specific blockchain data structures.
## Test
# Run the test function
`test_block_parse()`
```TestBlock
   Merkle Root: 01e5f8ef45651a8f28aac2691c0bf2159138400437274c02dd4b8b1ac2ef1564
   Timestamp: 1970-01-01 00:08:07
   Bits: 4294770688 (Difficulty: 0.0)
   Nonce: 2936209407
   Number of Transactions: 170
   Transaction Information:
   Version: 7
   Locktime: 420741142
   Number of Inputs: 0
   Number of Outputs: 0
   Transaction Inputs:
   Transaction Outputs:
   Transaction Information:
   Version: 2839568471
   Locktime: 0
   Number of Inputs: 235
   Number of Outputs: 0
   Transaction Inputs:
   Input 1:
   Previous Output Hash: 7601191df616bb9748bacd92b721a07b020000000000160014035a32e3e1d73f
   Output Index: 3973306363
   ScriptSig: c3a4a532a16fe4d70000000000fdffffff0200000000000000000a6a5d0714baa···
   Input 9:
   Previous Output Hash: 01f10b000000000000160014cdccb1311df1a421611dec5ac9ebc0a2ba219ac7
   Output Index: 0
============================== 1 passed in 0.10s ===============================
```
## Output Example
When running the script, you might see output similar to the following, indicating the interaction with the node:
```Main.py
Connected to Bitcoin node at 5.255.97.254:8333
Received version message: 80110100090400000000000000000000000000000···
Received verack message:
Connection established!
Received sendcmpct message: 000200000000000000
Received ping message: 91a6033e2dcc3a89
Sent Pong
Received feefilter message: e803000000000000
Received Inventory:  InvMessage(items=[(1, b'\xa7\xe2JQ\x1d\xbdn\xf2\x82\xf1\xb0\xf9\xb3\x00\xa9\xe2\x96\x82i!\xc9i\xdd\xbc\xe0.\x80\x03`\x84 \r'), (1, b'\xcf\xcf\xf0\xde\x98y1\xeb\xe0K\x15\xa6]\xb0@\xa5\xbe\xae6\xe0b\xbc@\xc9\x80\x1d\x87\xc8\x0c\x14\xdf\x8a'), (1, b'\x81[\xcb\n\x94\xa4\x85\xddG6\xdd\xben\x07\x0cT\x028\xf6q\xb5:\xdf8\x13\x15K\xf31C\x01\xec'), (1, b'#\x08\xd9\xc47\x85\xd0\xb2#~>\xe13\xea\xfdu\x91\xde\xef\x1cD\xf4\xfdd\xfc0\xad\xe7F!\x99\xcf'), (1, b'<)OM\t\xd8\x8b\xc5yu\xd4\x9a\xa7cQ#[\xe8{1\xb6\xd2\xb7\xe3\xeb\xde\xe93k\x1b\xbc\xbe'), (1, b'-6\xb6\x13\x9e\x91u\xc2\xd1@M\x83+\x98!+\x1a\xec@\x93j\x08GU@#{\xc1\xff{I\x9d'), (1, b'GN\xd2;J`\x19i:\xa6\xe2\xce\xc3\x96\xb4\xe6:BP\x9d|\xa0o\x83\x90\xba\xb0\xee\x8b\xb6\x92g'), (1, b'\xe9\xaa\xe9-\xb0\xa085\xdch\xbc"\x14\xfbn\xe8\xc9q\x1bU`\xd3\nCl]\x00\x15e\x94\x8e|'), (1, b'\xf8\xb0\xe7#\xad6\xe3\xd1\x1dD/\x86 h\x9b\xd1\xc6\x9f\xa0\x8et9,\x10O\xb6\x15Q\xb1\x98\xd7\xe0'), (1, b'\xea&\xcb{F\xea:%\x04\x12w\x87\xd8\xe3]\xd8\xec\xcf\x0c\xb0\xe5\xf7\xa3\xd9\x9b\x00 qVr\xa2}'), (1, b'\xedD}\xa0;\xdc\xc1"6\x94\x0f\xf3\x04\xdc\xdf\xf8\xaa1\xfeE\xb4\xbd\x80\x95\xf7\xd0\xac{\xdc\xff\x1f\xe4'), (1, b"\xc1K\xa3\x9d\x04\x06'21\x82\xe5)\xee\xbdN\xcb3\x04\x1d@\xb8\x06\xc8\x04:vl1RC\xda\xd8"), (1, b'\x93\x18"Q8U&8k\xc2FL&\x05\xbfg\xb8\x8f\x92\x93\xd0\xcf\x07\xa7G\xb3\x9a\xfa\xdf\xdd\x12\xc8'), (1, b'\x8e~\xad4\x85\x84\xb33\xbdKma\xcbb\xec$\xb9|\xf2p\x99\xd6\xc9A\xb8\xbf[n\\8\xa8\xa5'), (1, b"W\xcc(\x97q\x99[.\xb0\xf7\xbfO)\xfel\xcc\xa0/'\xf5z$\xdd{\xcaT\xd0\xbb\x93(/8"), (1, b'1\xd6\x1eW\xc9H\xc4J\xd7=\xcd\xba\xea\xbe\x9f\xa2\xf1h\tdR-\x14T\xaf;K\x85r\x8d\x15\x85'), (1, b'\x1b[O`\x878\x1c\x7f\x0cU\xcc\x980\xd0\xf4\xa0\xe7zPi\xc7\x18\xef\xae,\xd5k\r\xc7Zq\xe4'), (1, b'\xb1\xc8\xa0?Q\x18a\xc3\xc7\xbe\x03\x9d\x87\x0cg\x14\x96AoL\xf88\n\x0f\x85k\xea\x7f\x15\xc5l\xe8'), (1, b'p.A\xa3@,\x08\xd2\xe8|#\x03\x1c\xb7\xf8\xf6\x1c\xa1!\x13\nPw\x08\xa0\x06\x97T\xbc\xc2f\xf7'), (1, b'Ab$^b\xd4\xbc\x0b\xd4\xd5\xebG\x9f\xc6D\xb82\\=\xe8\xea\x987\x9e;u\x05[\x8f^(z'), (1, b'\xd8W\\\xfeX=\xc0\xaa\xe8I\xf5|\x17&\\\x16\xe9\xe1\xd7\xb7\xa6\xa84\xe4\xd7\xc9J\xb9\x98S&R'), (1, b'r\x0f;E\xca\xd1Sr\x92\x19~\xe7}\xbf\xef\xb9\xb7Vcv\x97\x89\x1f\xd1\xd6\xf3-\xfb\x87>\xca('), (1, b'$Na]\xff\xf2\xd9\xa2s\xe6\xbe\xae\xb0\xad\xb8W\xb40\xaf\x17@\x03\xd1\x81\x00E*\xf1\xa98h\x9e'), (1, b'\x13G\x84\x82\xe0+\xefl\x1e\x8a\x14\xa1%\x1e\xa8l\xf0CY\xd7~\xd4P\x14\x9c\xa0\xa1\xbf\x83{\xf2\xf3'), (1, b'R\xb5\t\xd2\xa997\x00\xff\xce]`O\x03C\x0e\xbcWNd\x04\xf8i\xfe\x03\x06\x8c\x8a6\x05\x14\xda'), (1, b'\xeai\xdd\x85\x7f\xc0\xa0\xaaA\xaeT\xa2\xd6[\xc1\x83\xf4`\xeb\xae\xc2\x1cQ,}\xb0\x04\xabZ\xe3\r\xd2'), (1, b'\t\xd3N\xee&A\x81k\xc6\xff\xff`E\xcb\xff\xff}\xe0\x9b\xc8+\x9b\xb4\xa2\xd7\xc3\xe5\x82|\x8a\xdf\xe5'), (1, b'\xd3u\x85\xa7\x1f\r\x19U\xa7^\x93z(a\x14\xe3ET\xa4e\xc0\\\x08+By\xe8\xear\xe5\xed\x9b'), (1, b'U\\\x92N\xc5CY\xc7\xa8;i\xaf\x02\x1d\x86&\x16\x9bg\xb8\x9b\xabn\xea\t\x80WU\x81C\x94/'), (1, b'\xecS\xa8\xa5\xa5\xd4\xd9\xdb\x9e\x9a\x89N\x8f\xd7\xd5\x12\x0e\xf0\xf0Tp\xd5\x93\xa55h&6\x98B\x1b~')], command=b'inv')
Received tx message: [0100000001a7a81d4d8c0644ac1fb127a807d8ed97e35adb93f389dc377eb11d17f50ea5f3bf0000···]
Transaction Information:
   Version: 1
  Locktime: 0
  Number of Inputs: 1
  Number of Outputs: 1
  Transaction Inputs:
    Input 1:
      Previous Output Hash: a7a81d4d8c0644ac1fb127a807d8ed97e35adb93f389dc377eb11d17f50ea5f3
      Output Index: 191
      ScriptSig: 483045022100d62d4c53deea9ca4466d7a853518f478d06688ecc46d62···
  Transaction Outputs:
    Output 1:
      Value: 14947 Satoshis
      ScriptPubKey: 00146d0f77fc5d049b51a5de3fd47b1c1abda711e3ae
    Output 2:
      Value: 60659 Satoshis
      ScriptPubKey: 00142042e9b4bf795baea1feed294d98b34c709c9bba
 [Block ~~~]
```
## Troubleshooting
 - Common issues include:
   - Connection issues: Need to connect more nodes, form peergroup, so as to be able to capture more Transaction and Block information faster, the network connection can also be more stable.
   - Added a test case: Utilizes a real block data example for parsing and validating the block information.
## Platform Compatibility
The code has been tested on the following platforms:
- macOS
- Linux
