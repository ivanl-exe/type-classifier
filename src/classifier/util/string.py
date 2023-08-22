def find_any(s: str, args: str) -> int:
    l = [s.find(arg) for arg in args if arg in s]
    if len(l) == 0: return -1
    elif len(l) == 1: return l[0]
    return min(*l)