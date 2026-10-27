from sylo.nodes import *

# 2: sylo parser
# by las-r

# precedences
PRECEDENCES = {
    "||": 1,
    "&&": 2,
    "==": 3, "!=": 3,
    "<": 4, ">": 4, "<=": 4, ">=": 4,
    "|": 5,
    "^": 6,
    "&": 7,
    "<<": 8, ">>": 9,
    "+": 9, "-": 9,
    "*": 10, "/": 10, "%": 10
}

# parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # helper functions
    def peek(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def advance(self):
        token = self.peek()
        if token is not None:
            self.pos += 1
        return token

    # parsing functions
    def parseatom(self):
        token = self.advance()
        if token is None:
            raise SyntaxError("Expected expression")

        # literals
        if token.kind == "STRING":
            return StringLit(token.value[1:-1])
        if token.kind == "FLOAT":
            return FloatLit(float(token.value))
        if token.kind == "INTEGER":
            return IntLit(int(token.value))
        if token.kind == "BOOL":
            return BoolLit(token.value == "true")

        raise SyntaxError(f"Unexpected token: {token.value}")

    def parseexpr(self, minprec=0):
        pass

    def parsestmt(self):
        pass

    # main parse function
    def parse(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.parsestmt())
        return statements