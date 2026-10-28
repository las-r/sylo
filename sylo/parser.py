from sylo.nodes import *

# 2: sylo parser
# by las-r

# constants
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
UNARIES = ["-", "!", "~"]

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

    def expect_kind(self, kind):
        token = self.peek()
        if token is None or token.kind != kind:
            raise SyntaxError(f"Expected token type {kind}, got {token}")
        return self.advance()

    def expect_value(self, value):
        token = self.peek()
        if token is None or token.value != value:
            raise SyntaxError(f"Expected {value!r}, got {token}")
        return self.advance()

    # parsing functions
    def parseatom(self):
        token = self.advance()
        if token is None:
            raise SyntaxError("Expected expression")

        # type casting
        if token.kind == "TYPE":
            self.expect_value(":")
            return Cast(token.value, self.parseatom())

        # unary operators
        if token.value in UNARIES:
            operand = self.parseatom()
            return UnaryOp(token.value, operand)

        # literals
        if token.kind == "STRING":
            return StringLit(token.value[1:-1])
        if token.kind == "FLOAT":
            return FloatLit(float(token.value))
        if token.kind == "INTEGER":
            return IntLit(int(token.value))
        if token.kind == "BOOL":
            return BoolLit(token.value == "true")

        # variable
        if token.kind == "IDENTIFIER":
            return Var(token.value)

        # parentheses
        if token.value == "(":
            expr = self.parseexpr()
            self.expect_value(")")
            return expr

        raise SyntaxError(f"Unexpected token: {token.value}")

    def parseexpr(self, minprec=0):
        left = self.parseatom()
        while True:
            token = self.peek()
            if token is None or token.value not in PRECEDENCES:
                break
            prec = PRECEDENCES[token.value]
            if prec < minprec:
                break
            op = self.advance().value
            right = self.parseexpr(prec + 1)
            left = BinaryOp(left, op, right)
        return left

    def parsestmt(self):
        token = self.advance()
        if token is None:
            raise SyntaxError("Expected statement")

        # inferred variables and assignment
        if token.kind == "IDENTIFIER":
            nxt = self.peek()
            if nxt is not None and nxt.value == ":=":
                self.advance()
                stmt = VarDeclare(None, token.value, self.parseexpr())
            elif nxt is not None and nxt.value == "=":
                self.advance()
                stmt = VarAssign(token.value, self.parseexpr())
            else:
                raise SyntaxError(f"Unexpected token after {token.value!r}: {nxt}")

        # typed variables
        elif token.kind == "TYPE":
            name = self.expect_kind("IDENTIFIER").value
            value = None
            if self.peek() is not None and self.peek().value == "=":
                self.advance()
                value = self.parseexpr()
            stmt = VarDeclare(token.value, name, value)

        else:
            raise SyntaxError(f"Unexpected token: {token.value}")

        self.expect_value(";")
        return stmt

    # main parse function
    def parse(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.parsestmt())
        return statements