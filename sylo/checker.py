from sylo.nodes import *

# 3: sylo checker
# by las-r

# constants
NUMERIC = {"int", "float", "byte"}
INTEGRAL = {"int", "byte"}
CASTS = {
    ("int", "float"), ("float", "int"),
    ("int", "byte"), ("byte", "int"),
    ("int", "string"), ("float", "string"), ("bool", "string"),
    ("string", "int"), ("string", "float"),
}

# checker error
class CheckError(Exception):
    pass

# checker
class Checker:
    def __init__(self):
        self.vars = {}

    def check(self, stmts):
        for s in stmts:
            self.stmt(s)

    # statements
    def stmt(self, s):
        # var declarations
        if isinstance(s, VarDeclare):
            if s.name in self.vars:
                raise CheckError(f"{s.name} already declared")
            if s.value is None:
                self.vars[s.name] = s.type_name
                return
            vt = self.expr(s.value)
            if s.type_name is None:
                s.type_name = vt
            elif s.type_name != vt:
                raise CheckError(f"{s.name} is {s.type_name}, got {vt}")
            self.vars[s.name] = s.type_name

        # vqr assignments
        elif isinstance(s, VarAssign):
            if s.name not in self.vars:
                raise CheckError(f"{s.name} not declared")
            vt = self.expr(s.value)
            if self.vars[s.name] != vt:
                raise CheckError(f"{s.name} is {self.vars[s.name]}, got {vt}")

    # expression type checker
    def expr(self, e):
        e.type = self._expr(e)
        return e.type

    # expression type helper
    def _expr(self, e):
        # literals
        if isinstance(e, IntLit):    return "int"
        if isinstance(e, FloatLit):  return "float"
        if isinstance(e, BoolLit):   return "bool"
        if isinstance(e, StringLit): return "string"

        # variables
        if isinstance(e, Var):
            if e.name not in self.vars:
                raise CheckError(f"{e.name} not declared")
            return self.vars[e.name]

        # operations
        if isinstance(e, UnaryOp):
            t = self.expr(e.value)
            if e.op == "!" and t == "bool": return "bool"
            if e.op == "-" and t in NUMERIC: return t
            if e.op == "~" and t in INTEGRAL: return t
            raise CheckError(f"can't apply {e.op} to {t}")
        if isinstance(e, BinaryOp):
            l, r = self.expr(e.left), self.expr(e.right)
            if l != r:
                raise CheckError(f"{l} {e.op} {r}: types must match")
            if e.op in ("&&", "||"):
                if l != "bool": raise CheckError(f"{e.op} needs bool")
                return "bool"
            if e.op in ("==", "!="):
                return "bool"
            if e.op in ("<", ">", "<=", ">="):
                if l not in NUMERIC: raise CheckError(f"can't compare {l}")
                return "bool"
            if e.op in ("&", "|", "^", "<<", ">>"):
                if l not in INTEGRAL: raise CheckError(f"{e.op} needs int/byte")
                return l
            if e.op in ("+", "-", "*", "/", "%"):
                if l not in NUMERIC: raise CheckError(f"can't use {e.op} on {l}")
                return l

        # type casts
        if isinstance(e, Cast):
            src = self.expr(e.value)
            if src != e.target and (src, e.target) not in CASTS:
                raise CheckError(f"can't cast {src} to {e.target}")
            return e.target

        raise CheckError(f"unknown node {e}")