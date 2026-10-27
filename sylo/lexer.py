from dataclasses import dataclass
import re

# 1: sylo lexer
# by las-r

@dataclass
class Token:
    kind: str
    value: str

# token pattern
TOKEN_PATTERN = re.compile(
    r'(?P<COMMENT>//[^\n]*)'
    r'|(?P<STRING>"(?:\\.|[^"\\])*")'
    r'|(?P<FLOAT>\d+\.\d+)'
    r'|(?P<INTEGER>\d+)'
    r'|(?P<BOOL>\b(?:true|false)\b)'
    r'|(?P<IDENTIFIER>[a-zA-Z_]\w*)'
    r'|(?P<OP>:=|==|!=|<=|>=|&&|\|\||<<|>>|[+\-*/%<>=!~|^&])'
    r'|(?P<PUNCT>[(){}\[\];,.:])'
    r'|(?P<SPACE>\s+)'
)

# tokenizer
def tokenize(source):
    tokens = []
    for match in TOKEN_PATTERN.finditer(source):
        kind = match.lastgroup
        value = match.group()
        if kind in ("COMMENT", "SPACE"):
            continue
        tokens.append(Token(kind, value))
    return tokens