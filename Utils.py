
# helper functions
def decode_int(s, nbytes, encoding='little'):
    return int.from_bytes(s.read(nbytes), encoding)


def encode_int(i, nbytes, encoding='little'):
    return i.to_bytes(nbytes, encoding)


def decode_varint(s):
    i = decode_int(s, 1)
    if i == 0xfd:
        return decode_int(s, 2)
    elif i == 0xfe:
        return decode_int(s, 4)
    elif i == 0xff:
        return decode_int(s, 8)
    else:
        return i


def encode_varint(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + encode_int(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + encode_int(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + encode_int(i, 8)
    else:
        raise ValueError("integer too large: %d" % (i,))

# -----------------------------------------------------------------------------
