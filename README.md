# sylo
sylo is yet another minimal compiled programming language.
Statically typed, garbage collected, no pointers, no manual memory control.

## Lexical
- Source is UTF-8. Whitespace separates tokens; newlines are not significant.
- Comments: `// to end of line`.
- Statements end with `;`.
- Identifiers: `[A-Za-z_][A-Za-z0-9_]*`.
- Keywords: `def struct if else while for in break continue return true false nil map void`.
- Literals: decimal ints (`42`), floats (`3.14`, digits required on both sides of the dot), strings (`"..."` with escapes `\n \t \\ \" \0`), `true`, `false`, `nil`.

## Types
### Primitive types
- `int`: 64-bit signed, wraps on overflow.
- `float`: 64-bit IEEE 754 double.
- `bool`: `true` / `false`.
- `byte`: 8-bit unsigned, wraps on overflow.
- `string`: immutable byte string. Never `nil`; the empty string is `""`.

### Composite types
- Array `T[]`: growable, bounds-checked. `T` is any type, including other arrays.
- Map `map[K]V`: `K` must be `int`, `string`, `bool` or `byte`. `V` is any type.
- Struct: declared at top level as `struct Name { T a; T b; }`. Named fields, no methods.

### Reference semantics
- `int`, `float`, `bool`, `byte` are copied by value.
- `string`, arrays, maps, structs are references. Assignment and argument passing share the object.
- `nil` is a value of struct types only. Arrays, maps and strings are never `nil`.

### Conversions
No implicit conversions anywhere. Explicit conversions are `int(x)`, `float(x)`, `byte(x)` and `str(x)`.
- `int(float)` truncates toward zero.
- `int(byte)` and `byte(int)` (the latter keeps the low 8 bits) are allowed.
- `str(x)` accepts `int`, `float`, `bool`, `byte`.

## Declarations
Top level contains only `struct` and `def` declarations, in any order. There are no global variables, nested functions, closures, overloading or imports.

```
struct Point { int x; int y; }

def int add(int a, int b) { return a + b; }
def void greet(string name) { println("hi " + name); }
```

- Return type is a type or `void`.
- Parameters are passed by value (references share their object).
- Falling off the end of a non-`void` function is a runtime error.
- Every program has exactly one `def int main() { ... }`; its return value is the process exit code.

## Statements
- `T V = X;` declares with an explicit type. `V := X;` declares with the type of `X`.
- Every variable must be initialised at declaration. Redeclaring a name in the same scope is an error; shadowing an outer scope is allowed. Scopes are blocks.
- `V = X;` assigns. Targets can also be `a[i] = X;`, `s.f = X;`, `m[k] = X;`.
- `if C { } else if C { } else { }`: braces always required, no parentheses around `C`.
- `while C { }`
- `for V in A..B { }`: `V` is a fresh `int` running from `A` up to `B - 1`. `A` and `B` are evaluated once, and `V` is read-only inside the body.
- `break;` `continue;` `return X;` `return;`
- An expression statement is allowed only for function calls.

## Expressions
### Literals and construction
- Array: `int[]{1, 2, 3}`, empty `int[]{}`.
- Map: `map[string]int{}` (always empty; fill with assignment).
- Struct: `Point{x: 1, y: 2}`. Every field is required, in any order.

### Access
- `a[i]` (array index, bounds-checked), `s[i]` (string index, yields `byte`), `m[k]` (missing key is a runtime error), `p.x` (field).
- `nil` field access is a runtime error.

### Operators
Precedence, lowest to highest (all binary operators are left-associative):

| Level | Operators | Operand types |
|---|---|---|
| 1 | `\|\|` | bool |
| 2 | `&&` | bool |
| 3 | `==` `!=` | any matching type |
| 4 | `<` `>` `<=` `>=` | int, float, byte |
| 5 | `\|` | int, byte |
| 6 | `^` | int, byte |
| 7 | `&` | int, byte |
| 8 | `<<` `>>` | int (shift count masked to 0..63; `>>` is arithmetic) |
| 9 | `+` `-` | int, float, byte; `+` also string |
| 10 | `*` `/` `%` | int, float, byte; `%` int/byte only |
| 11 (unary) | `-` `!` `~` | `-`: int/float, `!`: bool, `~`: int/byte |

Rules:
- Both operands of a binary operator must have exactly the same type.
- `&&` and `||` short-circuit.
- `/` and `%` on ints truncate toward zero. Division by zero is a runtime error.
- `==` and `!=`: primitives compare by value, strings by content, and structs, arrays and maps by identity. Only structs may be compared with `nil`.

## Built-in functions
These are compiler built-ins, not library code.
- `print(x)`, `println(x)`: `x` is any of `int`, `float`, `bool`, `byte`, `string`.
- `read_line()`: returns `string` (empty at end of input).
- `len(x)`: `string`, array or map.
- `append(a, x)`: appends `x` to array `a`. Returns nothing.
- `has(m, k)`: `bool`.
- `keys(m)`: `K[]` in unspecified order.
- Conversions: `int`, `float`, `byte`, `str`.

## Runtime errors
Out-of-bounds index, missing map key, `nil` access, division by zero and falling off a function all print a message and exit with code 1.

## Memory
Memory is automatic and invisible. An implementation may reclaim unreachable objects or never reclaim anything.