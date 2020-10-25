import numpy as np
import math
import operator


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


class Variable:
    def __init__(self, val=None):
        self.value = val
        self.table = []

    def set_table(self, start, stop, step):
        self.table = np.arange(start, stop, step)


class RPN:
    def __init__(self):
        # operator, priority, associativity(left==0)
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
        self.notation = []

    def to_pop_operator(self, left_op, right_op):
        if not (left_op in self.binary_ops or left_op == '(' or left_op == '#'):
            raise RuntimeError("excepted operstor on top of the stack, got {}".format(left_op))

        if left_op == '#':
            return True

        if left_op == '(':
            return False

        if self.binary_ops[left_op][1] > self.binary_ops[right_op][1]:
            return True

        if self.binary_ops[left_op][1] < self.binary_ops[right_op][1]:
            return False

        # left-associative
        if self.binary_ops[left_op][2] == 0:
            return True
        else:
            return False

    def convert(self, tokens):
        stack = []
        for token in tokens:
            if token == ',':
                continue

            if token in self.funcs:
                stack.append(token)
                continue

            if token == ')':
                while peek(stack) != '(':
                    self.notation.append(stack.pop())
                stack.pop()
                if stack and peek(stack) in self.funcs:
                    self.notation.append(stack.pop())
                continue

            if token == '(':
                stack.append(token)
                continue

            if is_number(token) or token in self.variables or token in self.const:
                self.notation.append(token)
                continue

            if token in self.binary_ops:
                if not stack:
                    stack.append(token)
                    continue

                while stack and self.to_pop_operator(peek(stack), token):
                    self.notation.append(stack.pop())
                stack.append(token)
                continue
            else:
                raise RuntimeError("inappropriate token value: {}".format(token))

        while stack:
            tok = stack.pop()
            self.notation.append(tok)

    def evaluate(self, **values):
        stack = []
        for token in self.notation:
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

    def calculate(self, rpn):
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


if __name__ == '__main__':
    rpn = RPN()
    tokens = ['sin', '(', 'x', ')']
    rpn.convert(tokens)
    print(rpn.notation)
    print(rpn.evaluate(x=math.pi))
