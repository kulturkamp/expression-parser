from RPN import RPN, Variable
import matplotlib.pyplot as plt
import re
import math
import json


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
        if token == '-' and (i == 0 or tokens[i - 1] in '^*/+-('):
            tokens[i] = '#'


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


class Expression:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = self.tokenize()
        self.notation = self.get_rpn()
        self.table = {}

    def tokenize(self):
        if not (check_parentheses(self.expression)):
            raise RuntimeError("parentheses do not match")
        tokens = re.findall(r"(\b\w*[\.]?\w+\b|[\(\|\^\,\)\+\*\-\/])", self.expression)
        replace_brackets(tokens)
        replace_unary_minus(tokens)
        return tokens

    def get_rpn(self):
        rpn_obj = RPN()
        rpn_obj.convert(self.tokens)
        return rpn_obj.notation

    def evaluate(self, arg):
        rpn_obj = RPN()
        rpn_obj.convert(self.tokens)
        return rpn_obj.evaluate(x=arg)

    def tabulate(self, start, stop, step):
        arg = Variable()
        arg.set_table(start, stop, step)
        rpn_obj = RPN()
        rpn_obj.convert(self.tokens)
        for value in arg.table:
            self.table[value] = rpn_obj.evaluate(x=value)

    def draw(self):
        if not self.table:
            raise RuntimeError("expression is not tabulated")
        x, y = zip(*self.table.items())
        fig, ax = plt.subplots()
        ax.grid()
        ax.axhline(y=0, color='black')
        plt.axvline(x=0, color='black')
        plt.plot(x, y)
        plt.show()

    def print(self, table=True):
        print("expression: {}\ntokens: {}\nreverse polish notation: {}"
              .format(self.expression, self.tokens, self.notation))
        if table:
            print("table: ")
            print(json.dumps(self.table, indent=1))


# some tests
def case1():
    expr_obj = Expression("sin(x)")
    expr_obj.tabulate(-math.pi, math.pi, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


def case2():
    expr_obj = Expression("|x|")
    expr_obj.tabulate(-5, 5, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


def case3():
    # parentheses error
    expr_obj = Expression("2*sin(1/(exp(3*x)+1)-tg(x+PI/2)")
    expr_obj.tabulate(-5, 5, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


def case4():
    # token value error
    expr_obj = Expression("sin(asdfafdfdf) + asdfasdf + coc(z)")
    expr_obj.tabulate(math.pi, math.pi, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


def case5():
    expr_obj = Expression("2*sin(1/(exp(3*x)+1))-tg(x+PI/2)")
    expr_obj.tabulate(-10*math.pi, 10*math.pi, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


if __name__ == '__main__':
    expr = Expression("exp(x)")
    expr.tabulate(-2, 2, 0.01)
    expr.draw()
    # case1()
    # case2()
    # case3()
    # case4()
    # case5()
