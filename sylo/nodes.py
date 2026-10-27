from dataclasses import dataclass
from typing import Optional

# def: sylo nodes
# by las-r

@dataclass
class Node:
    line: int = 0
    col: int = 0

# region expressions
@dataclass 
class Expr(Node): 
    type: Optional[object] = None

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

# endregion

# region statements
@dataclass
class Stmt(Node): 
    pass

@dataclass
class VarDeclare(Stmt):
    name: str
    type_name: Optional[str]
    value: Expr

@dataclass
class VarAssign(Stmt):
    name: str
    value: str

# endregion

# region top level
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

# endregion