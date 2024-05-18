from MessageHandler import BlockMessage


def test_block_parse():
    import io

    # Hypothetical block data, which you would normally need to copy from a real block
    # Here is an example only, the data is a real block converted to a string of bytes

    block_data = bytes.fromhex('')  # Copy the BlockExample here

    # Use BytesIO to simulate a file stream
    stream = io.BytesIO(block_data)

    # Calling the parse method
    block = BlockMessage.parse(stream)

    # Print the parsed block information to verify
    BlockMessage.print_blockReadable(block)


# Run the test function
test_block_parse()
