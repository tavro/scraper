def encode_36(num):
    """
    Encodes decimal integer number into base 36
    """
    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while num:
        num, i = divmod(num, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def decode_36(num_36):
    """
    Decodes base 36 number into decimal integer
    """
    return int(num_36.upper(), 36)


def decimal_to_36(num):
    """
    Formats number to fit prnt.sc url
    """
    return encode_36(num).lower()
