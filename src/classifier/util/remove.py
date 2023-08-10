def strip_protocol(url: str) -> str:
    i = url.find(':')
    if i == -1: return url
    url = url[i+1:]
    if url[:2] == '//': return url[2:]
    return url