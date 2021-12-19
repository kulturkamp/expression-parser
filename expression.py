from RPN import RPN, Variable
import matplotlib.pyplot as plt
import math
import json


class Expression:
    def __init__(self, expression=None):
        self.expression = expression
        self.rpn = RPN(expression)
        self.table = {}

    def evaluate(self, arg):
        return self.rpn.evaluate(x=arg)

    def calculate(self, expr=None):
        if not expr:
            expr = self.expression
        return self.rpn.calculate(expr)

    def tabulate(self, start, stop, step):
        arg = Variable()
        arg.set_table(start, stop, step)
        for value in arg.table:
            self.table[value] = self.rpn.evaluate(x=value)

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
              .format(self.expression, self.rpn.tokens, self.rpn.notation))
        if table:
            print("table: ")
            print(json.dumps(self.table, indent=1))


# some tests
def case1():
    expr_obj = Expression("sin(x)")
    expr_obj.tabulate(-math.pi, math.pi, 0.01)
    expr_obj.print()
    print(expr_obj.evaluate(math.pi))
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
    print(expr_obj.tokens)
    expr_obj.tabulate(math.pi, math.pi, 0.01)
    expr_obj.print(table=False)
    # print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


def case5():
    expr_obj = Expression("2*sin(1/(exp(3*x)+1)-tg(x+PI/2))")
    expr_obj.tabulate(-math.pi, math.pi, 0.0001)
    expr_obj.print(table=False)
    print(expr_obj.evaluate(math.pi))
    expr_obj.draw()


if __name__ == '__main__':
    case1()
