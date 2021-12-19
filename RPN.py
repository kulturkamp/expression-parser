import numpy as np
import math
import operator
import re


def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def peek(lst):
    return lst[len(lst) - 1]


def check_parentheses(srt):
    stack = []
    for i in srt:
        if i == '(':
            stack.append(i)
        elif i == ')':
            if len(stack) > 0:
                stack.pop()
            else:
                return False
    return len(stack) == 0


def replace_brackets(tokens):
    for i, token in enumerate(tokens):
        if token == '|':
            tokens[i] = 'abs'
            tokens.insert(i + 1, '(')
            j = len(tokens) - 1
            while True:
                if tokens[j] == '|':
                    tokens[j] = ')'
                    break
                j -= 1


def replace_unary_minus(tokens):
    for i, token in enumerate(tokens):
        if token == '-' and (i == 0 or tokens[i - 1] in '^*/+-(,'):
            tokens[i] = '#'


def tokenize(expr):
    if not (check_parentheses(expr)):
        raise RuntimeError("parentheses do not match")
    tokens = re.findall(r"(\b\w*[\.]?\w+\b|[\(\|\^\,\)\+\*\-\/])", expr)
    replace_brackets(tokens)
    replace_unary_minus(tokens)
    return tokens


class Variable:
    def __init__(self, val=None):
        self.value = val
        self.table = []

    def set_table(self, start, stop, step):
        self.table = np.arange(start, stop, step)


class RPN:
    def __init__(self, expr=None):
        # operator, priority, associativity(right==0)
        self.binary_ops = {
            '^': (operator.pow, 3, 0),
            'pow': (operator.pow, 3, 0),
            '*': (operator.mul, 2, 1),
            '/': (operator.truediv, 2, 1),
            '+': (operator.add, 1, 1,),
            '-': (operator.sub, 1, 1)
        }
        self.funcs = {
            'sin': math.sin,
            'cos': math.cos,
            'tg': math.tan,
            'ctg': lambda arg: 1/math.tan(arg),
            'exp': math.exp,
            'abs': math.fabs,
            'sqrt': math.sqrt,
            '#': lambda arg: arg * -1  # unary minus
        }
        self.const = {
            'E': math.e,
            'PI': math.pi
        }
        self.variables = {
            'x': None,
            'y': None,
            'z': None
        }
        self.expression = expr
        self.tokens = tokenize(expr) if expr else []
        try:
            self.notation = self.convert()
        except RuntimeError:
            self.notation = []

    def to_pop_operator(self, left_op, right_op):
        if not (left_op in self.binary_ops or left_op == '(' or left_op == '#'):
            raise RuntimeError("excepted operator on top of the stack, got {}".format(left_op))

        if left_op == '#':
            return True

        if left_op == '(':
            return False

        if self.binary_ops[left_op][1] > self.binary_ops[right_op][1]:
            return True

        if self.binary_ops[left_op][1] < self.binary_ops[right_op][1]:
            return False

        if self.binary_ops[left_op][2] == 0:
            return True
        else:
            return False

    def convert(self, expr=None):
        tokens = tokenize(expr) if expr else self.tokens
        if not tokens:
            return []
        stack = []
        notat = []
        for token in tokens:
            if token == ',':
                continue

            if token in self.funcs:
                stack.append(token)
                continue

            if token == ')':
                while peek(stack) != '(':
                    notat.append(stack.pop())
                stack.pop()
                if stack and peek(stack) in self.funcs:
                    notat.append(stack.pop())
                continue

            if token == '(':
                stack.append(token)
                continue

            if is_number(token) or token in self.variables or token in self.const:
                notat.append(token)
                continue

            if token in self.binary_ops:
                if not stack:
                    stack.append(token)
                    continue

                while stack and self.to_pop_operator(peek(stack), token):
                    notat.append(stack.pop())
                stack.append(token)
                continue
            else:
                raise RuntimeError("inappropriate token value: {}".format(token))

        while stack:
            tok = stack.pop()
            notat.append(tok)
        return notat

    def evaluate(self, expr=None, **values, ):
        notation = self.convert(expr) if expr else self.notation
        stack = []
        for token in notation:
            if is_number(token):
                stack.append(float(token))

            if token in self.const:
                stack.append(self.const[token])

            if token in self.variables:
                for value in values:
                    if token == value:
                        self.variables[token] = Variable(values[token])
                        stack.append(self.variables[token].value)
                if not self.variables[token]:
                    raise RuntimeError("variable {} was not given".format(token))

            elif token in self.binary_ops:
                if len(stack) < 2:
                    break
                b, a = stack.pop(), stack.pop()
                stack.append(self.binary_ops[token][0](a, b))

            elif token in self.funcs:
                a = stack.pop()
                stack.append(self.funcs[token](a))
        if not stack:
            raise RuntimeError("empty input for evaluate")
        return stack.pop()

    def calculate(self, expr):
        rpn = self.convert(expr)
        stack = []
        for token in rpn:
            if is_number(token):
                stack.append(float(token))
                continue

            if token in self.const:
                stack.append(self.const[token])
                continue

            elif token in self.binary_ops:
                if len(stack) < 2:
                    break
                b, a = stack.pop(), stack.pop()
                stack.append(self.binary_ops[token][0](a, b))
                continue

            elif token in self.funcs:
                a = stack.pop()
                stack.append(self.funcs[token](a))
                continue
        if not stack:
            raise RuntimeError("empty input for calculate")
        return stack.pop()

    def print(self):
        print("expression: {}\ntokens: {}\nreverse polish notation: {}"
              .format(self.expression, self.tokens, self.notation))


if __name__ == '__main__':
    # rpn = RPN('sin(x+y)')
    # rpn.print()
    # print(rpn.evaluate(x=math.pi/2, y=math.pi/2))
    # rpn = RPN('((2+3)*(4+5))^2')
    # print(rpn.notation)
    # print(rpn.evaluate(expr='sin(x)', x=math.pi))
    rpn = RPN()
    print(rpn.calculate('sin(PI/2+PI/2)'))


