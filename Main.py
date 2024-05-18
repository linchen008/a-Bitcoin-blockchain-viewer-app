
from Connect2Net import SimpleNode

def main():
    # Initialize node connections
    node = SimpleNode(host='seed.bitcoin.sipa.be', net='main')
    node.handshake()
    node.listen_forever()

    node.close()


if __name__ == "__main__":
    main()
