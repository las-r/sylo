from dataclasses import dataclass, field
from typing import Optional

# def: sylo nodes
# by las-r

@dataclass
class Node:
    pass

# expressions
@dataclass 
class Expr(Node): 
    type: Optional[object] = field(default=None, kw_only=True)

@dataclass
class IntLit(Expr): 
    value: int

@dataclass
class ByteLit(Expr): 
    value: int

@dataclass
class FloatLit(Expr): 
    value: float

@dataclass
class BoolLit(Expr): 
    value: bool

@dataclass
class StringLit(Expr): 
    value: str

@dataclass
class UnaryOp(Expr):
    op: str
    value: Expr

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class Var(Expr):
    name: str

@dataclass
class Cast(Expr):
    target: str
    value: Expr

# statements
@dataclass
class Stmt(Node): 
    pass

@dataclass
class VarDeclare(Stmt):
    type_name: Optional[str]
    name: str
    value: Optional[Expr]

@dataclass
class VarAssign(Stmt):
    name: str
    value: Expr

# top level
@dataclass
class Param(Node):
    name: str
    type_name: str

@dataclass
class Func(Node):
    name: str
    params: list[Param]
    ret_type_name: Optional[str]
    body: list[Stmt]

@dataclass
class Program(Node):
    funcs: list[Func]