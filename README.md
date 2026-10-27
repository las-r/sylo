# sylo
sylo is yet another minimal compiled programming language.

## Types
### Primitive types
- `int`: 64-bit signed integer
- `byte`: 8-bit unsigned integer
- `float`: 64-bit floating point (IEEE 754 double)
- `bool`: `true` / `false`
- `string`: Immutable, GC-managed byte string

### Composite types
- **Arrays (`T[]`)**: growable, bounds-checked, with `len()` and `append()`.
- **Structs**: named fields, no methods.
- **Maps**: built-in key/value type

### Value vs. reference semantics
- Primitives (`int`, `byte`, `float`, `bool`) are passed and copied by value.
- Structs, arrays, maps and strings are reference types.
- `nil` represents "no object" for reference types.