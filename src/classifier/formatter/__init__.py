from typing import Union
from collections import defaultdict
from classifier import Class, TypeClassifier
from classifier.util.path import conjoin
from toml import load
from classifier.util.domain import format_protocol, strip_protocol
from copy import deepcopy


class TypeFormatter:

  def __init__(
      self,
      filepath: Union[tuple, str] = ('classifier', '/toml', '/config.toml')
  ) -> None:
    if type(filepath) == tuple: filepath = conjoin(*filepath)
    self.filepath = filepath

    with open(self.filepath, 'r') as file:
      config = load(file)
    self.type = defaultdict(lambda: None, config['classifier']['type'])

  def __decide__(self, token: Class):
    if self.type[token.type] == None: return token.value
    return self.type[token.type].format(token.value)

  def decide(self, token: Class):
    if token == TypeClassifier.EMPTY: TypeFormatter.__format_empty__(token)
    elif token == TypeClassifier.IP_ADDRESS:
      TypeFormatter.__format_url__(token, 'http')
    elif token == TypeClassifier.USERNAME:
      TypeFormatter.__format_encode_prefix__(token)
    elif token == TypeClassifier.HASHTAG:
      TypeFormatter.__format_encode_prefix__(token)
    elif token == TypeClassifier.URL:
      TypeFormatter.__format_url__(token, 'https')
    elif token == TypeClassifier.NUMBER:
      TypeFormatter.__format_number__(token)
    return self.__decide__(token)

  def __format_empty__(token: Class) -> None:
    token.value = None

  def __format_url__(token: Class, protocol: str) -> None:
    token.value = format_protocol(protocol) + strip_protocol(token.value)

  def __format_encode_prefix__(token) -> None:
    token.value = '%' + hex(ord(token.value[0]))[2:] + token.value[1:]

  def __format_number__(token: Class) -> None:
    token.value = int(token.value)

  def format(self, *tokens: Class) -> list[str]:
    return [self.decide(token) for token in deepcopy(tokens)]

  def serialize(self, *tokens: Class) -> list:
    """
    serialized JSON array
    """
    return [{**vars(token), "transformed-value": self.decide(token)} for token in tokens]