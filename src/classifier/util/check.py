def is_byte(octet: str) -> bool:
    return octet.isnumeric() and (int(octet) >= 0 and int(octet) < 2 ** 8)