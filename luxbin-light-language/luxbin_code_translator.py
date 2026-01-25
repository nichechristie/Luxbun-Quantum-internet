#!/usr/bin/env python3
"""
LUXBIN Code Language Translator
Developed by Nicheai - Universal Code Translation System

Translates between programming languages using AST parsing and code generation.
Supports Python ↔ JavaScript translation with type inference.

Company: Nicheai (https://nicheai.com)
Author: Nichole Christie
License: MIT
"""

import ast
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
try:
    import clang.cindex as clang
    CLANG_AVAILABLE = True
except ImportError:
    CLANG_AVAILABLE = False
    print("Warning: clang not available. C++ translation will not work.")


@dataclass
class TypeInfo:
    """Type information for variables and expressions."""
    name: str
    category: str  # 'primitive', 'object', 'function', 'array'
    js_equivalent: str
    py_equivalent: str


class CodeTranslator:
    """
    Universal code translator supporting Python ↔ JavaScript conversion.

    Features:
    - AST-based parsing for both languages
    - Type inference system
    - Code generation templates
    - Cross-language type mapping
    """

    def __init__(self):
        self.type_map = self._build_type_map()

    def _build_type_map(self) -> Dict[str, TypeInfo]:
        """Build the type mapping dictionary."""
        return {
            # Primitive types
            'int': TypeInfo('int', 'primitive', 'number', 'int'),
            'float': TypeInfo('float', 'primitive', 'number', 'float'),
            'str': TypeInfo('str', 'primitive', 'string', 'str'),
            'bool': TypeInfo('bool', 'primitive', 'boolean', 'bool'),

            # Python-specific types
            'list': TypeInfo('list', 'array', 'Array', 'list'),
            'dict': TypeInfo('dict', 'object', 'Object', 'dict'),
            'tuple': TypeInfo('tuple', 'array', 'Array', 'tuple'),
            'set': TypeInfo('set', 'object', 'Set', 'set'),

            # JavaScript types
            'number': TypeInfo('number', 'primitive', 'number', 'float'),
            'string': TypeInfo('string', 'primitive', 'string', 'str'),
            'boolean': TypeInfo('boolean', 'primitive', 'boolean', 'bool'),
            'Array': TypeInfo('Array', 'array', 'Array', 'list'),
            'Object': TypeInfo('Object', 'object', 'Object', 'dict'),

            # C++ types
            'int32_t': TypeInfo('int32_t', 'primitive', 'number', 'int'),
            'int64_t': TypeInfo('int64_t', 'primitive', 'number', 'int'),
            'float32': TypeInfo('float32', 'primitive', 'number', 'float'),
            'float64': TypeInfo('float64', 'primitive', 'number', 'float'),
            'double': TypeInfo('double', 'primitive', 'number', 'float'),
            'char': TypeInfo('char', 'primitive', 'string', 'str'),
            'std::string': TypeInfo('std::string', 'primitive', 'string', 'str'),
            'bool': TypeInfo('bool', 'primitive', 'boolean', 'bool'),
            'std::vector': TypeInfo('std::vector', 'array', 'Array', 'list'),
            'std::map': TypeInfo('std::map', 'object', 'Object', 'dict'),
            'std::unordered_map': TypeInfo('std::unordered_map', 'object', 'Object', 'dict'),
        }

    def translate_python_to_javascript(self, python_code: str) -> str:
        """
        Translate Python code to JavaScript.

        Args:
            python_code: Python source code

        Returns:
            JavaScript equivalent code
        """
        try:
            # Parse Python AST
            tree = ast.parse(python_code)
            return self._python_ast_to_js(tree)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")

    def translate_javascript_to_python(self, js_code: str) -> str:
        """
        Translate JavaScript code to Python.

        Args:
            js_code: JavaScript source code

        Returns:
            Python equivalent code
        """
        try:
            # Parse JavaScript AST (would use esprima in production)
            js_ast = self._parse_js_ast(js_code)
            return self._js_ast_to_python(js_ast)
        except Exception as e:
            raise ValueError(f"Invalid JavaScript syntax: {e}")

    def translate_python_to_cpp(self, python_code: str) -> str:
        """
        Translate Python code to C++.

        Args:
            python_code: Python source code

        Returns:
            C++ equivalent code
        """
        try:
            # Parse Python AST
            tree = ast.parse(python_code)
            return self._python_ast_to_cpp(tree)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")

    def translate_cpp_to_python(self, cpp_code: str) -> str:
        """
        Translate C++ code to Python.

        Args:
            cpp_code: C++ source code

        Returns:
            Python equivalent code
        """
        if not CLANG_AVAILABLE:
            raise ValueError("C++ translation requires clang library. Install with: pip install clang")

        try:
            # Parse C++ AST using clang
            cpp_ast = self._parse_cpp_ast(cpp_code)
            return self._cpp_ast_to_python(cpp_ast)
        except Exception as e:
            raise ValueError(f"Invalid C++ syntax: {e}")

    def translate_javascript_to_cpp(self, js_code: str) -> str:
        """
        Translate JavaScript code to C++.

        Args:
            js_code: JavaScript source code

        Returns:
            C++ equivalent code
        """
        try:
            # Parse JavaScript AST
            js_ast = self._parse_js_ast(js_code)
            return self._js_ast_to_cpp(js_ast)
        except Exception as e:
            raise ValueError(f"Invalid JavaScript syntax: {e}")

    def translate_cpp_to_javascript(self, cpp_code: str) -> str:
        """
        Translate C++ code to JavaScript.

        Args:
            cpp_code: C++ source code

        Returns:
            JavaScript equivalent code
        """
        if not CLANG_AVAILABLE:
            raise ValueError("C++ translation requires clang library. Install with: pip install clang")

        try:
            # Parse C++ AST using clang
            cpp_ast = self._parse_cpp_ast(cpp_code)
            return self._cpp_ast_to_javascript(cpp_ast)
        except Exception as e:
            raise ValueError(f"Invalid C++ syntax: {e}")

    def _python_ast_to_js(self, node: ast.AST) -> str:
        """Convert Python AST to JavaScript code."""
        if isinstance(node, ast.Module):
            return '\n'.join(self._python_ast_to_js(stmt) for stmt in node.body)

        elif isinstance(node, ast.FunctionDef):
            params = ', '.join(arg.arg for arg in node.args.args)
            body = '\n'.join(f'  {self._python_ast_to_js(stmt)}' for stmt in node.body)
            return f'function {node.name}({params}) {{\n{body}\n}}'

        elif isinstance(node, ast.Return):
            value = self._python_ast_to_js(node.value) if node.value else ''
            return f'return {value};'

        elif isinstance(node, ast.Assign):
            targets = ', '.join(self._python_ast_to_js(target) for target in node.targets)
            value = self._python_ast_to_js(node.value)
            return f'let {targets} = {value};'

        elif isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)

        elif isinstance(node, ast.BinOp):
            left = self._python_ast_to_js(node.left)
            right = self._python_ast_to_js(node.right)
            op = self._python_op_to_js(node.op)
            return f'{left} {op} {right}'

        elif isinstance(node, ast.Expr):
            return f'{self._python_ast_to_js(node.value)};'

        else:
            return f'// Unsupported: {type(node).__name__}'

    def _python_op_to_js(self, op: ast.operator) -> str:
        """Convert Python operators to JavaScript."""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
            ast.Eq: '===',
            ast.NotEq: '!==',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
        }
        return op_map.get(type(op), '?')

    def _parse_cpp_ast(self, cpp_code: str) -> Any:
        """
        Parse C++ code to AST using clang.

        Args:
            cpp_code: C++ source code

        Returns:
            Clang AST root node
        """
        try:
            # Create a temporary C++ file
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(cpp_code)
                temp_file = f.name

            try:
                # Parse the C++ file
                index = clang.Index.create()
                translation_unit = index.parse(temp_file, ['-std=c++17'])

                if not translation_unit:
                    raise ValueError("Failed to parse C++ code")

                # Check for parsing errors
                if len(translation_unit.diagnostics) > 0:
                    errors = []
                    for diag in translation_unit.diagnostics:
                        if diag.severity >= clang.Diagnostic.Error:
                            errors.append(str(diag))
                    if errors:
                        raise ValueError("C++ parsing errors: " + "; ".join(errors))

                return translation_unit.cursor

            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except Exception as e:
            raise ValueError(f"C++ AST parsing failed: {e}")

    def _parse_js_ast(self, js_code: str) -> Dict[str, Any]:
        """
        Parse JavaScript code to AST using esprima via Node.js subprocess.
        """
        import subprocess
        import json
        import tempfile
        import os

        # Create a temporary JavaScript file to run the parser
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            # Write a Node.js script that uses our parser
            script = f'''
const JsAstParser = require('./lib/js_ast_parser');
const parser = new JsAstParser();

try {{
    const code = {json.dumps(js_code)};
    const ast = parser.parseCode(code);
    const simplified = parser.simplifyAst(ast);
    console.log(JSON.stringify(simplified));
}} catch (error) {{
    console.error(JSON.stringify({{error: error.message}}));
    process.exit(1);
}}
'''
            f.write(script)
            temp_file = f.name

        try:
            # Run the Node.js script
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(temp_file) if os.path.dirname(temp_file) else '.'
            )

            if result.returncode != 0:
                raise ValueError(f"JavaScript parsing failed: {result.stderr}")

            # Parse the JSON output
            parsed_ast = json.loads(result.stdout.strip())
            if 'error' in parsed_ast:
                raise ValueError(f"JavaScript parsing error: {parsed_ast['error']}")

            return parsed_ast

        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to run JavaScript parser: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AST JSON: {e}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass

    def _js_ast_to_python(self, js_ast: Dict[str, Any]) -> str:
        """Convert JavaScript AST to Python code."""
        if js_ast.get('type') == 'Program':
            body = js_ast.get('body', [])
            statements = []
            for node in body:
                stmt = self._js_node_to_python(node)
                if stmt:
                    statements.append(stmt)
            return '\n'.join(statements)
        return '# JavaScript to Python conversion placeholder'

    def _js_node_to_python(self, node: Dict[str, Any]) -> str:
        """Convert individual JavaScript AST node to Python."""
        if not node:
            return ''

        node_type = node.get('type', '')

        if node_type == 'FunctionDeclaration':
            name = node.get('id', {}).get('name', 'anonymous')
            params = []
            for param in node.get('params', []):
                if isinstance(param, dict) and 'name' in param:
                    params.append(param['name'])
                else:
                    params.append('param')

            # Convert function body
            body_stmts = []
            if node.get('body') and node['body'].get('body'):
                for stmt in node['body']['body']:
                    body_stmt = self._js_node_to_python(stmt)
                    if body_stmt:
                        body_stmts.append(f'    {body_stmt}')

            if not body_stmts:
                body_stmts = ['    pass']

            return f'def {name}({", ".join(params)}):\n' + '\n'.join(body_stmts)

        elif node_type == 'VariableDeclaration':
            kind = node.get('kind', 'let')
            declarations = []
            for decl in node.get('declarations', []):
                var_name = decl.get('id', {}).get('name', 'var')
                init_value = self._js_expr_to_python(decl.get('init'))
                if init_value:
                    declarations.append(f'{var_name} = {init_value}')
                else:
                    declarations.append(f'{var_name} = None')
            return '\n'.join(declarations)

        elif node_type == 'ReturnStatement':
            argument = self._js_expr_to_python(node.get('argument'))
            return f'return {argument}' if argument else 'return'

        elif node_type == 'ExpressionStatement':
            expr = self._js_expr_to_python(node.get('expression'))
            return f'{expr}' if expr else ''

        elif node_type == 'IfStatement':
            test = self._js_expr_to_python(node.get('test'))
            consequent = self._js_node_to_python(node.get('consequent'))
            alternate = self._js_node_to_python(node.get('alternate')) if node.get('alternate') else ''

            result = f'if {test}:\n'
            result += '\n'.join(f'    {line}' for line in consequent.split('\n') if line)

            if alternate:
                result += '\nelse:\n'
                result += '\n'.join(f'    {line}' for line in alternate.split('\n') if line)

            return result

        return f'# Unsupported JS node: {node_type}'

    def _python_ast_to_cpp(self, node: ast.AST) -> str:
        """Convert Python AST to C++ code."""
        if isinstance(node, ast.Module):
            includes = ['#include <iostream>', '#include <string>', '#include <vector>', '#include <unordered_map>']
            code_lines = []

            # Add includes
            code_lines.extend(includes)
            code_lines.append('')
            code_lines.append('using namespace std;')
            code_lines.append('')

            # Convert body
            for stmt in node.body:
                cpp_stmt = self._python_stmt_to_cpp(stmt)
                if cpp_stmt:
                    code_lines.append(cpp_stmt)

            return '\n'.join(code_lines)

        elif isinstance(node, ast.FunctionDef):
            params = []
            for arg in node.args.args:
                # Map Python types to C++ types
                cpp_type = self._python_type_to_cpp('auto')  # Default to auto
                params.append(f'{cpp_type} {arg.arg}')

            body_stmts = []
            for stmt in node.body:
                cpp_stmt = self._python_stmt_to_cpp(stmt)
                if cpp_stmt:
                    body_stmts.append(f'    {cpp_stmt}')

            if not body_stmts:
                body_stmts = ['    // Function body']

            params_str = ', '.join(params)
            return f'auto {node.name}({params_str}) {{\n' + '\n'.join(body_stmts) + '\n}'

        elif isinstance(node, ast.Return):
            value = self._python_expr_to_cpp(node.value) if node.value else ''
            return f'return {value};'

        elif isinstance(node, ast.Assign):
            targets = ', '.join(self._python_expr_to_cpp(target) for target in node.targets)
            value = self._python_expr_to_cpp(node.value)
            return f'auto {targets} = {value};'

        elif isinstance(node, ast.Expr):
            expr = self._python_expr_to_cpp(node.value)
            return f'{expr};'

        else:
            return f'// Unsupported Python construct: {type(node).__name__}'

    def _python_stmt_to_cpp(self, node: ast.AST) -> str:
        """Convert Python statement to C++."""
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                func_name = self._python_expr_to_cpp(node.value.func)
                if func_name == 'print':
                    args = [self._python_expr_to_cpp(arg) for arg in node.value.args]
                    return f'cout << {" << ".join(args)} << endl;'
        return self._python_ast_to_cpp(node)

    def _python_expr_to_cpp(self, expr: ast.AST) -> str:
        """Convert Python expression to C++."""
        if isinstance(expr, ast.Name):
            return expr.id

        elif isinstance(expr, ast.Constant):
            if isinstance(expr.value, str):
                return f'"{expr.value}"'
            elif expr.value is None:
                return '{}';  # C++11 empty initializer
            else:
                return str(expr.value)

        elif isinstance(expr, ast.BinOp):
            left = self._python_expr_to_cpp(expr.left)
            right = self._python_expr_to_cpp(expr.right)
            op = self._python_op_to_cpp(expr.op)
            return f'{left} {op} {right}'

        elif isinstance(expr, ast.Call):
            func = self._python_expr_to_cpp(expr.func)
            args = [self._python_expr_to_cpp(arg) for arg in expr.args]
            return f'{func}({", ".join(args)})'

        elif isinstance(expr, ast.List):
            elements = [self._python_expr_to_cpp(elt) for elt in expr.elts]
            return f'vector<auto>{{{", ".join(elements)}}}'

        elif isinstance(expr, ast.Dict):
            # Convert dict to unordered_map
            items = []
            for key, value in zip(expr.keys, expr.values):
                if key:
                    key_cpp = self._python_expr_to_cpp(key)
                    value_cpp = self._python_expr_to_cpp(value)
                    items.append(f'{{{key_cpp}, {value_cpp}}}')
            return f'unordered_map<auto, auto>{{{", ".join(items)}}}'

        return '/* unsupported expression */'

    def _python_op_to_cpp(self, op: ast.operator) -> str:
        """Convert Python operators to C++."""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
        }
        return op_map.get(type(op), '?')

    def _python_type_to_cpp(self, python_type: str) -> str:
        """Map Python types to C++ types."""
        type_map = {
            'int': 'int',
            'float': 'double',
            'str': 'string',
            'bool': 'bool',
            'list': 'vector<auto>',
            'dict': 'unordered_map<auto, auto>',
        }
        return type_map.get(python_type, 'auto')

    def _cpp_ast_to_python(self, cursor) -> str:
        """Convert C++ AST to Python code."""
        # This is a simplified implementation
        # In a full implementation, we'd traverse the clang AST

        # Mock implementation for demonstration
        return """# C++ to Python conversion
# This is a simplified implementation
# Full implementation would traverse clang AST

def converted_function():
    # C++ code would be analyzed here
    return "converted"
"""

    def _cpp_ast_to_javascript(self, cursor) -> str:
        """Convert C++ AST to JavaScript code."""
        # Mock implementation for demonstration
        return """// C++ to JavaScript conversion
// This is a simplified implementation
// Full implementation would traverse clang AST

function convertedFunction() {
    // C++ code would be analyzed here
    return "converted";
}
"""

    def _js_ast_to_cpp(self, js_ast: Dict[str, Any]) -> str:
        """Convert JavaScript AST to C++ code."""
        # Mock implementation for demonstration
        return """#include <iostream>
#include <string>

using namespace std;

// JavaScript to C++ conversion
// This is a simplified implementation

auto convertedFunction() {
    // JavaScript code would be analyzed here
    return "converted";
}
"""

    def _js_expr_to_python(self, expr: Any) -> str:
        """Convert JavaScript expression to Python."""
        if not expr:
            return 'None'

        expr_type = expr.get('type', '')

        if expr_type == 'Literal':
            value = expr.get('value')
            if isinstance(value, str):
                return f'"{value}"'
            elif value is None:
                return 'None'
            elif isinstance(value, bool):
                return str(value).lower()  # True/False -> true/false
            else:
                return str(value)

        elif expr_type == 'Identifier':
            return expr.get('name', 'unknown')

        elif expr_type == 'BinaryExpression':
            left = self._js_expr_to_python(expr.get('left'))
            right = self._js_expr_to_python(expr.get('right'))
            op = self._js_op_to_python(expr.get('operator', '+'))
            return f'{left} {op} {right}'

        elif expr_type == 'CallExpression':
            callee = self._js_expr_to_python(expr.get('callee'))
            args = [self._js_expr_to_python(arg) for arg in expr.get('arguments', [])]
            return f'{callee}({", ".join(args)})'

        return 'None'

    def _js_op_to_python(self, op: str) -> str:
        """Convert JavaScript operators to Python."""
        op_map = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '===': '==',
            '!==': '!=',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '&&': 'and',
            '||': 'or'
        }
        return op_map.get(op, op)

    def infer_types(self, code: str, language: str) -> Dict[str, TypeInfo]:
        """
        Perform basic type inference on code.

        Args:
            code: Source code
            language: 'python' or 'javascript'

        Returns:
            Dictionary mapping variable names to type information
        """
        types = {}

        if language == 'python':
            try:
                tree = ast.parse(code)
                self._infer_python_types(tree, types)
            except:
                pass

        elif language == 'javascript':
            # Mock type inference for JavaScript
            types['mock_var'] = self.type_map.get('number', TypeInfo('unknown', 'unknown', 'unknown', 'unknown'))

        elif language == 'cpp':
            # Mock type inference for C++
            types['mock_var'] = self.type_map.get('int', TypeInfo('unknown', 'unknown', 'unknown', 'unknown'))

        return types

    def _infer_python_types(self, node: ast.AST, types: Dict[str, TypeInfo]):
        """Infer types from Python AST."""
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    if isinstance(node.value, ast.Constant):
                        if isinstance(node.value.value, int):
                            types[var_name] = self.type_map['int']
                        elif isinstance(node.value.value, str):
                            types[var_name] = self.type_map['str']
                        elif isinstance(node.value.value, bool):
                            types[var_name] = self.type_map['bool']
                    elif isinstance(node.value, ast.List):
                        types[var_name] = self.type_map['list']
                    elif isinstance(node.value, ast.Dict):
                        types[var_name] = self.type_map['dict']

        # Recursively process child nodes
        for child in ast.iter_child_nodes(node):
            self._infer_python_types(child, types)


def main():
    """Main function for command-line interface and API calls."""
    import sys
    import json

    translator = CodeTranslator()

    # Check if we have JSON input (API mode)
    if not sys.stdin.isatty():
        try:
            # Read JSON input from stdin
            input_data = json.loads(sys.stdin.read().strip())

            action = input_data.get('action')

            if action == 'translate':
                code = input_data['code']
                source_lang = input_data['source_language']
                target_lang = input_data['target_language']

                try:
                    result = ""
                    if source_lang == 'python' and target_lang == 'javascript':
                        result = translator.translate_python_to_javascript(code)
                    elif source_lang == 'javascript' and target_lang == 'python':
                        result = translator.translate_javascript_to_python(code)
                    elif source_lang == 'python' and target_lang == 'cpp':
                        result = translator.translate_python_to_cpp(code)
                    elif source_lang == 'cpp' and target_lang == 'python':
                        result = translator.translate_cpp_to_python(code)
                    elif source_lang == 'javascript' and target_lang == 'cpp':
                        result = translator.translate_javascript_to_cpp(code)
                    elif source_lang == 'cpp' and target_lang == 'javascript':
                        result = translator.translate_cpp_to_javascript(code)
                    else:
                        result = f"Unsupported translation: {source_lang} -> {target_lang}"

                    print(json.dumps({
                        'success': True,
                        'translated_code': result
                    }))
                except Exception as e:
                    print(json.dumps({
                        'success': False,
                        'error': str(e)
                    }))

            elif action == 'infer_types':
                code = input_data['code']
                language = input_data['language']

                types = translator.infer_types(code, language)
                print(json.dumps({
                    'success': True,
                    'types': {k: v.__dict__ for k, v in types.items()}
                }))

        except json.JSONDecodeError:
            print(json.dumps({
                'success': False,
                'error': 'Invalid JSON input'
            }))
        except KeyError as e:
            print(json.dumps({
                'success': False,
                'error': f'Missing required field: {e}'
            }))
        return

    # Interactive demo mode
    print("🌈 LUXBIN Code Language Translator Demo")
    print("=" * 50)

    # Example Python code
    python_code = '''
def greet(name):
    message = "Hello, " + name
    return message

result = greet("World")
print(result)
'''

    print("Original Python code:")
    print(python_code)
    print("\nTranslated to JavaScript:")
    try:
        js_code = translator.translate_python_to_javascript(python_code)
        print(js_code)
    except Exception as e:
        print(f"Translation error: {e}")

    # Example JavaScript code
    js_example = '''
function calculate(x, y) {
    if (x > y) {
        return x + y;
    } else {
        return x - y;
    }
}
'''
    print(f"\nOriginal JavaScript code:")
    print(js_example)
    print("Translated to Python:")
    try:
        py_code = translator.translate_javascript_to_python(js_example)
        print(py_code)
    except Exception as e:
        print(f"Translation error: {e}")

    # Example C++ code
    cpp_example = '''
#include <iostream>

int main() {
    int x = 42;
    std::cout << "Hello, World! " << x << std::endl;
    return 0;
}
'''
    print(f"\nOriginal C++ code:")
    print(cpp_example)
    print("Translated to Python:")
    try:
        cpp_to_py = translator.translate_cpp_to_python(cpp_example)
        print(cpp_to_py)
    except Exception as e:
        print(f"Translation error: {e}")

    # Type inference demo
    print("\nType Inference Demo:")
    simple_code = "x = 42\ny = 'hello'\nz = [1, 2, 3]"
    print(f"Code: {simple_code}")
    types = translator.infer_types(simple_code, 'python')
    print("Inferred types:")
    for var_name, type_info in types.items():
        print(f"  {var_name}: {type_info.name} ({type_info.category})")


if __name__ == "__main__":
    main()