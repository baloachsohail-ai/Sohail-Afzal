"""A simple command-line calculator.

Supports +, -, *, /, // (floor division), % (modulo), ** (power),
parentheses, unary minus, and a few math functions (sqrt, sin, cos, ...).
Expressions are parsed safely with the `ast` module -- no eval().

Usage:
    python calculator.py            # interactive mode
    python calculator.py "2 + 3*4"  # evaluate a single expression
"""

import ast
import math
import operator
import sys

BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "round": round,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


class CalculatorError(Exception):
    """Raised when an expression cannot be evaluated."""


def _eval(node, variables):
    if isinstance(node, ast.Expression):
        return _eval(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPS:
        left = _eval(node.left, variables)
        right = _eval(node.right, variables)
        if isinstance(node.op, ast.Pow) and abs(right) > 10000:
            raise CalculatorError("exponent too large")
        return BINARY_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
        return UNARY_OPS[type(node.op)](_eval(node.operand, variables))
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise CalculatorError(f"unknown name: {node.id}")
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in FUNCTIONS
        and not node.keywords
    ):
        args = [_eval(arg, variables) for arg in node.args]
        return FUNCTIONS[node.func.id](*args)
    raise CalculatorError("unsupported expression")


def calculate(expression, variables=None):
    """Evaluate an arithmetic expression string and return the result."""
    variables = variables or {}
    try:
        tree = ast.parse(expression.replace("^", "**"), mode="eval")
        return _eval(tree, variables)
    except ZeroDivisionError:
        raise CalculatorError("division by zero")
    except SyntaxError:
        raise CalculatorError("invalid syntax")
    except (ValueError, TypeError, OverflowError) as exc:
        raise CalculatorError(str(exc))


def format_result(value):
    if isinstance(value, float) and value.is_integer() and abs(value) < 1e15:
        return str(int(value))
    return str(value)


def repl():
    print("Calculator - type an expression, 'help' for help, 'quit' to exit.")
    variables = {}
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("quit", "exit", "q"):
            break
        if line == "help":
            print("Operators: + - * / // % ** (or ^), parentheses")
            print("Functions: " + ", ".join(sorted(FUNCTIONS)))
            print("Constants: pi, e   Last result: ans")
            continue
        try:
            result = calculate(line, variables)
        except CalculatorError as exc:
            print(f"Error: {exc}")
            continue
        variables["ans"] = result
        print(format_result(result))


def main(argv):
    if len(argv) > 1:
        try:
            print(format_result(calculate(" ".join(argv[1:]))))
        except CalculatorError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0
    repl()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
