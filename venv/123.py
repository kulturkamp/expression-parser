import unittest
from unittest.mock import Mock


class UserBase():
    def __init__(self):
        self.users = {}

    def addUser(self, name, pas):
        self.users[name] = pas

    def delUser(self, name):
        del self.users[name]



class sbvTesting(unittest.TestCase):
    def testStateVerification(self):
        base = UserBase()
        self.assertFalse(base.users)

        base.addUser('Ivan', 123)
        self.assertTrue(base.users)
        self.assertEqual(len(base.users), 1)
        self.assertEqual(list(base.users)[0], 'Ivan')

        base.addUser('Viktor', 345)
        self.assertEqual(len(base.users), 2)
        self.assertEqual(list(base.users)[1], 'Viktor')

        base.delUser('Ivan')
        self.assertEqual(len(base.users), 1)
        self.assertEqual(list(base.users)[0], 'Viktor')

    def testBehaviorVerification(self):
        base = UserBase()
        base.addUser = Mock()

        base.addUser('Ivan')
        base.addUser.assert_called_once()
        base.addUser.asser_called_with('Ivan')

        base.addUser('Viktor')
        base.addUser.asser_called_with('Viktor')

        base.delUser = Mock()
        base.delUser('Ivan')
        base.delUser('Viktor')
        self.assertEqual(base.delUser.call_count, 2)


def run():
    unittest.main()


if __name__ == '__main__':
    run()