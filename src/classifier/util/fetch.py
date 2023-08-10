from requests import get

def parse(url: str, parser):
    response = get(url)
    if response.status_code == 200:
        return parser(response.text)
    return None