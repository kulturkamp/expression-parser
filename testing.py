import unittest
from RPN import RPN
from expression import Expression
import math
from unittest.mock import Mock
from ddt import ddt, data, unpack

# class RpnUnitTesting(unittest.TestCase):
#     def setUp(self):
#         self.expr1 = 'sin(x)'
#         self.expr2 = '2*sin(1/(exp(3*x)+1)-tg(x+PI/2))'
#         self.expr3 = 'sin(x+y)'
#         self.expr4 = '((2+3)*(4+5))^2'
#
#     def testRpnTokenize(self):
#         rpn = RPN(self.expr1)
#         self.assertEqual(rpn.tokens, ['sin', '(', 'x', ')'])
#
#     def testRpnConvert1(self):
#         rpn = RPN(self.expr1)
#         self.assertEqual(rpn.notation, ['x', 'sin'])
#
#     def testRpnConvert2(self):
#         rpn = RPN(self.expr2)
#         self.assertEqual(rpn.notation, ['2', '1', '3', 'x', '*', 'exp', '1', '+', '/', 'x', 'PI', '2', '/', '+',
#                                         'tg', '-', 'sin', '*'])
#
#     def testRpnEvaluate1(self):
#         rpn = RPN(self.expr3)
#         self.assertAlmostEqual(rpn.evaluate(x=math.pi/2, y=math.pi/2), 0)
#
#     def testRpnEvaluate2(self):
#         rpn = RPN(self.expr2)
#         self.assertEqual(rpn.evaluate(x=math.pi / 2), 0.017806384741744875)
#
#     def testRpnCalculate(self):
#         rpn = RPN()
#         self.assertEqual(rpn.calculate(self.expr4), 2025)


# class RpnExpressionOrderedTesting(unittest.TestCase):
#     def setUp(self):
#         self.expr1 = 'sin(x)'
#         self.expr2 = '2*sin(1/(exp(3*x)+1)-tg(x+PI/2))'
#         self.expr3 = 'sin(asdfafdfdf) + asdfasdf + coc(z)'
#
#     def testRpnConvert1(self):
#         rpn = RPN(self.expr1)
#
#         tokens = rpn.tokens
#         self.assertEqual(tokens, ['sin', '(', 'x', ')'])
#
#         notation = rpn.convert()
#         self.assertEqual(notation, ['x', 'sin'])
#
#     def testExpressionEvaluate1(self):
#         expression = Expression(self.expr2)
#
#         tokens = expression.rpn.tokens
#         self.assertEqual(tokens, ['2', '*', 'sin', '(', '1', '/', '(', 'exp', '(', '3', '*', 'x', ')', '+', '1', ')',
#                                   '-', 'tg', '(', 'x', '+', 'PI', '/', '2', ')', ')'])
#
#         notation = expression.rpn.notation
#         self.assertEqual(notation, ['2', '1', '3', 'x', '*', 'exp', '1', '+', '/', 'x', 'PI', '2', '/', '+', 'tg', '-',
#                                     'sin', '*'])
#
#         self.assertEqual(expression.evaluate(math.pi), 1.630394220705093)
#
#     def testExpressionTabulate(self):
#         expression = Expression(self.expr1)
#
#         tokens = expression.rpn.tokens
#         self.assertEqual(tokens, ['sin', '(', 'x', ')'])
#
#         notation = expression.rpn.notation
#         self.assertEqual(notation, ['x', 'sin'])
#
#         expression.tabulate(math.pi, 2*math.pi,  0.01)
#         self.assertAlmostEqual(expression.table[math.pi], 0)
#
#     def testRpnConvert2(self):
#         expression = Expression(self.expr3)
#
#         tokens = expression.rpn.tokens
#         self.assertEqual(tokens, ['sin', '(', 'asdfafdfdf', ')', '+', 'asdfasdf', '+', 'coc', '(', 'z', ')'])
#
#         self.assertRaises(RuntimeError, expression.rpn.convert, self.expr3)
#

# class MockTesting(unittest.TestCase):
#     def setUp(self):
#         self.expr1 = 'sin(x)'
#         self.expr2 = '2*sin(1/(exp(3*x)+1)-tg(x+PI/2))'
#
#     def testMock1(self):
#         expression = Expression(self.expr1)
#         expression.rpn.evaluate = Mock(return_value=0)
#         print('\nmock test 1')
#         expression.print()
#         self.assertEqual(expression.evaluate(math.pi), 0)
#
#         expression.rpn.evaluate.assert_called_once()
#         expression.rpn.evaluate.assert_called_with(x=math.pi)
#
#     def testMock2(self):
#         expression = Expression()
#         rpn = RPN()
#         expression.rpn = Mock(**{'expression': 'sin(x)',
#                                 'tokens': ['sin', '(', 'x', ')'],
#                                 'notation': ['x', 'sin']
#                                 })
#
#         print('\nmock test 2')
#         expression.print()
#         self.assertAlmostEqual(rpn.evaluate(expr=expression.rpn.expression, x=math.pi), 0)
#
#
#     def log_eval(self, x):
#         rpn_mock = Mock(**{'evaluate.return_value': 0})
#         print('evaluating with x = {}'.format(x))
#         return rpn_mock
#
#     def testMock3(self):
#         expression = Expression(self.expr2)
#
#         get_rpn = Mock()
#         get_rpn.side_effect = self.log_eval
#         expression.rpn = get_rpn(math.pi)
#         print('\nmock test 3')
#         expression.print()
#         self.assertEqual(expression.evaluate(math.pi), 0)
#         get_rpn.assert_called_once_with(math.pi)




@ddt
class DataDrivenTesting(unittest.TestCase):

    @data(
        ('sin(x)', ['sin', '(', 'x', ')']),
        ('2*sin(1/(exp(3*x)+1)-tg(x+PI/2))', ['2', '*', 'sin', '(', '1', '/', '(', 'exp', '(', '3', '*', 'x', ')', '+',
                                              '1', ')', '-', 'tg', '(', 'x', '+', 'PI', '/', '2', ')', ')']),
        ('((2+3)*(4+5))^2', ['(', '(', '2', '+', '3', ')', '*', '(', '4', '+', '5', ')', ')', '^', '2'])
    )
    @unpack
    def testRpnTokenize(self, val, expected):
        rpn = RPN(val)
        self.assertEqual(rpn.tokens, expected)

    @data(
        ('sin(x)', ['x', 'sin']),
        ('2*sin(1/(exp(3*x)+1)-tg(x+PI/2))', ['2', '1', '3', 'x', '*', 'exp', '1', '+', '/', 'x', 'PI', '2', '/', '+',
                                              'tg', '-', 'sin', '*']),
        ('((2+3)*(4+5))^2', ['2', '3', '+', '4', '5', '+', '*', '2', '^'])
    )
    @unpack
    def testRpnConvert(self, val, expected):
        rpn = RPN(val)
        self.assertEqual(rpn.notation, expected)

    @data(
        ('sin(x)', math.pi, 0),
        ('2*sin(1/(exp(3*x)+1)-tg(x+PI/2))', math.pi/2, 0.017806384741744875)
    )
    @unpack
    def testRpnEvaluate(self, val, arg, expected):
        rpn = RPN(val)
        self.assertAlmostEqual(rpn.evaluate(x=arg), expected)

    @data(
        ('((2+3)*(4+5))^2', 2025),
        ('2^10+250', 1274),
        ('sin(PI/2+PI/2)', 0)
    )
    @unpack
    def testRpnCalculate(self, val, expected):
        rpn = RPN()
        self.assertAlmostEqual(rpn.calculate(val), expected)

def run():
    unittest.main()


if __name__ == '__main__':
    run()
