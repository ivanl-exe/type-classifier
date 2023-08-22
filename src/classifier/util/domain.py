from classifier.util.string import find_any

def strip_protocol(url: str) -> str:
    i = url.find(':')
    if i == -1: return url
    url = url[i+1:]
    if url[:2] == '//': return url[2:]
    return url

def extract_tld(domain: str) -> str:
    if '.' not in domain: return ''
    j = find_any(domain, ':/\\?#')
    return domain[domain.rfind('.')+1:j if j != -1 else None]