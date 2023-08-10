from typing import Union
from classifier.util.path import conjoin
from toml import load
from classifier.util.fetch import parse
from classifier.custom.parser import custom
from classifier.util.check import is_byte
from classifier.util.remove import strip_protocol

class Class:
    def __init__(self, data, type: str) -> None:
        self.data = data
        self.type = type

class TypeClassifier:
    UNKNOWN = MYSTERY = 'unknown'
    EMPTY = 'empty'
    STRING = 'string'
    NUMBER = 'number'
    CODE = 'code'
    URL = "url"
    EMAIL = 'email'
    IP_ADDRESS = 'ip-address'
    HASHTAG = 'hashtag'
    USERNAME = 'username'

    def __init__(self, filepath: Union[tuple, str] = ('classifier', '/toml', '/config.toml')) -> None:
        if type(filepath) == tuple: filepath = conjoin(*filepath)
        self.filepath = filepath

        with open(self.filepath, 'r') as file:
            config = load(file)
        url = config['tlds']['url']
        self.tlds = parse(url, parser = custom)
        self.tlds = self.tlds if self.tlds != None else []

    def tokenise(s: str) -> list[str]:
        tokens = ['']
        flag = False
        for character in s:
            if character == ' ' and not flag:
                tokens.append('')
                continue
            elif character == '`':
                flag = not flag
            tokens[-1] += character
        return tokens
    
    def decide(self, token: str) -> str:
        if TypeClassifier.__is_empty__(token): return TypeClassifier.EMPTY
        elif TypeClassifier.__is_code__(token): return TypeClassifier.CODE
        elif TypeClassifier.__is_hashtag__(token): return TypeClassifier.HASHTAG
        elif TypeClassifier.__is_username__(token): return TypeClassifier.USERNAME
        elif TypeClassifier.__is_ip_address__(token): return TypeClassifier.IP_ADDRESS
        elif TypeClassifier.__is_email__(token, self.tlds): return TypeClassifier.EMAIL
        elif TypeClassifier.__is_url__(token, self.tlds): return TypeClassifier.URL
        elif TypeClassifier.__is_number__(token): return TypeClassifier.NUMBER
        elif TypeClassifier.__is_string__(token): return TypeClassifier.STRING
        return TypeClassifier.UNKNOWN

    def __is_empty__(token: str) -> bool:
        return len(token) == 0
    
    def __is_string__(token: str) -> bool:
        return token.isalpha()
    
    def __is_number__(token: str) -> bool:
        return token.isnumeric()
    
    def __is_code__(token: str) -> bool:
        return len(token) == 0 or (token[0] == '`' and token[-1] == '`')
    
    def __is_url__(token: str, tlds: list[str]) -> bool:
        domain = strip_protocol(token)
        return domain[domain.find('.')+1:].upper() in tlds

    def __is_email__(token: str, tlds: list[str]) -> bool:
        i = token.find('@')
        return len(token[:max(i, 0)].replace(' ', '')) > 0 and TypeClassifier.__is_url__(token[i+1:], tlds)

    def __is_ip_address__(token: str) -> bool:
        octets = strip_protocol(token).split('.')
        return len(octets) == 4 and all([is_byte(octet) for octet in octets])

    def __is_hashtag__(token: str) -> bool:
        return token[0] == '#'

    def __is_username__(token: str) -> bool:
        return token[0] == '@'

    def classify(self, s: str) -> list[Class]:
        tokens = TypeClassifier.tokenise(s)
        classroom = []
        for token in tokens:
            type = self.decide(token)
            classroom.append(Class(token, type))
        return classroom