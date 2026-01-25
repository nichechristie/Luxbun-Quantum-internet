# LUXBIN Code Translation Guide

## 🌉 Cross-Language Code Translation

LUXBIN now supports translating code between programming languages using advanced AST (Abstract Syntax Tree) parsing and code generation techniques.

## Supported Languages

- **Python** ↔ **JavaScript** ↔ **C++**
- AST-based parsing for accurate syntax analysis
- Type inference and cross-language type mapping
- Support for modern C++17 features and STL containers

## Quick Start

### Python to JavaScript

```python
# Input Python code
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

result = calculate_fibonacci(10)
print(f"Fibonacci result: {result}")
```

**Translates to JavaScript:**
```javascript
function calculate_fibonacci(n) {
  if (n <= 1) {
    return n;
  }
  return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2);
}

let result = calculate_fibonacci(10);
console.log(`Fibonacci result: ${result}`);
```

### JavaScript to Python

```javascript
// Input JavaScript code
function isEven(number) {
    return number % 2 === 0;
}

function processNumbers(numbers) {
    return numbers.filter(isEven).map(n => n * 2);
}

const data = [1, 2, 3, 4, 5, 6];
const result = processNumbers(data);
console.log(result);
```

**Translates to Python:**
```python
def isEven(number):
    return number % 2 == 0

def processNumbers(numbers):
    return [n * 2 for n in numbers if isEven(n)]

data = [1, 2, 3, 4, 5, 6]
result = processNumbers(data)
print(result)
```

### Python to C++

```python
# Input Python code
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [1, 2, 3, 4, 5]
result = calculate_sum(data)
print(f"Sum: {result}")
```

**Translates to C++:**
```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

auto calculate_sum(vector<auto> numbers) {
    auto total = 0;
    for (auto num : numbers) {
        total = total + num;
    }
    return total;
}

auto data = vector<auto>{1, 2, 3, 4, 5};
auto result = calculate_sum(data);
cout << "Sum: " << result << endl;
```

## Language Differences Handled

### Operators
| Python | JavaScript | Notes |
|--------|------------|-------|
| `==` | `===` | Strict equality |
| `!=` | `!==` | Strict inequality |
| `and` | `&&` | Logical AND |
| `or` | `\|\|` | Logical OR |
| `not` | `!` | Logical NOT |

### Data Types
| Python | JavaScript | C++ | Type Category |
|--------|------------|-----|----------------|
| `int` | `number` | `int` | Primitive |
| `float` | `number` | `double` | Primitive |
| `str` | `string` | `std::string` | Primitive |
| `bool` | `boolean` | `bool` | Primitive |
| `list` | `Array` | `std::vector` | Array |
| `dict` | `Object` | `std::unordered_map` | Object |
| `tuple` | `Array` | `std::vector` | Array (immutable) |
| `set` | `Set` | `std::unordered_set` | Object |

### Control Structures

#### Conditionals
```python
# Python
if x > 0:
    result = "positive"
elif x < 0:
    result = "negative"
else:
    result = "zero"
```

```javascript
// JavaScript equivalent
if (x > 0) {
  result = "positive";
} else if (x < 0) {
  result = "negative";
} else {
  result = "zero";
}
```

#### Loops
```python
# Python
for item in items:
    process(item)
```

```javascript
// JavaScript equivalent
for (let item of items) {
  process(item);
}
```

## API Usage

### REST API

```bash
# Python to JavaScript
curl -X POST http://localhost:3000/api/v1/translate-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(name): return f\"Hello, {name}!\"",
    "source_language": "python",
    "target_language": "javascript"
  }'

# Python to C++
curl -X POST http://localhost:3000/api/v1/translate-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(name): return f\"Hello, {name}!\"",
    "source_language": "python",
    "target_language": "cpp"
  }'

# C++ to JavaScript
curl -X POST http://localhost:3000/api/v1/translate-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "auto hello(std::string name) { return \"Hello, \" + name; }",
    "source_language": "cpp",
    "target_language": "javascript"
  }'
```

### Response Format

```json
{
  "success": true,
  "original_code": "def hello(name): return f\"Hello, {name}!\"",
  "translated_code": "function hello(name) {\n  return `Hello, ${name}!`;\n}",
  "source_language": "python",
  "target_language": "javascript",
  "type_inference": {
    "name": {
      "name": "str",
      "category": "primitive",
      "js_equivalent": "string",
      "py_equivalent": "str"
    }
  }
}
```

### Python Library Usage

```python
from luxbin_code_translator import CodeTranslator

translator = CodeTranslator()

# Translate Python to JavaScript
python_code = """
def greet(name):
    return f"Hello, {name}!"
"""

js_code = translator.translate_python_to_javascript(python_code)
print(js_code)

# Translate Python to C++
cpp_code = translator.translate_python_to_cpp(python_code)
print(cpp_code)

# Translate JavaScript to Python
js_code = """
function greet(name) {
    return `Hello, ${name}!`;
}
"""

py_code = translator.translate_javascript_to_python(js_code)
print(py_code)

# Translate C++ to JavaScript
cpp_code_example = """
#include <iostream>
#include <string>

auto greet(std::string name) {
    return "Hello, " + name;
}
"""

js_from_cpp = translator.translate_cpp_to_javascript(cpp_code_example)
print(js_from_cpp)

# Type inference
types = translator.infer_types("x = 42\ny = 'hello'", "python")
for var_name, type_info in types.items():
    print(f"{var_name}: {type_info.name}")
```

## Advanced Features

### Type Inference

The translator can automatically detect variable types:

```python
# Input
x = 42
y = "hello"
z = [1, 2, 3]
w = {"key": "value"}

# Inferred types
x: int (primitive)
y: str (primitive)
z: list (array)
w: dict (object)
```

### Error Handling

The translator provides detailed error messages for invalid syntax:

```python
try:
    result = translator.translate_python_to_javascript("def invalid syntax(")
except ValueError as e:
    print(f"Translation error: {e}")
    # Output: Invalid Python syntax: invalid syntax (<unknown>, line 1)
```

## Limitations

### Current Limitations
- **C++ Parsing**: Currently uses mock implementation (full clang AST traversal planned)
- **Complexity**: Simple to medium complexity code works best
- **Libraries**: Standard library functions only (no external dependencies)
- **Async/Await**: Basic support for async functions
- **Classes**: Basic class translation (experimental)
- **Templates**: C++ template translation not yet supported

### Future Enhancements
- **Full C++ AST Support**: Complete clang-based parsing and traversal
- **More Language Pairs**: Java, Go, Rust, and other languages
- **Advanced Type Inference**: Generic types and template support
- **Library Translation**: Framework-specific code patterns
- **IDE Integration**: Plugin support for popular editors
- **Batch Processing**: Multi-file translation capabilities

## Testing

Run the test suite to verify functionality:

```bash
# Run Python tests
python test_code_translator.py

# Run with verbose output
python test_code_translator.py -v
```

## Contributing

To add support for new languages:

1. **Implement AST Parser**: Create language-specific AST parser
2. **Add Code Generator**: Implement code generation templates
3. **Update Type Map**: Add language-specific type mappings
4. **Add Tests**: Comprehensive test coverage
5. **Update Documentation**: API and usage documentation

## Troubleshooting

### Common Issues

**"JavaScript parsing failed"**
- Ensure Node.js and esprima are installed
- Check JavaScript syntax validity

**"Python AST parsing failed"**
- Verify Python syntax is correct
- Check for unsupported Python features

**"Type inference failed"**
- Some complex expressions may not be inferred
- This is non-critical and won't break translation

### Performance Tips

- Keep code snippets reasonably sized (< 10KB)
- Use simple, straightforward code patterns
- Avoid complex nested structures for best results

## License

This code translation feature is part of LUXBIN Light Language, licensed under MIT.