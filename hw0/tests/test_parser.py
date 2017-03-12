from .context import Parser

import unittest

str0 = "China has proposed that North Korea suspend its tests of missile and nuclear technology to 'defuse a looming crisis'."
res0 = {'and': 1, 'a': 1, 'tests': 1, 'Korea': 1, 'North': 1, 'proposed': 1, 'that': 1, 'defuse': 1, 'of': 1, 'looming': 1, 'missile': 1, 'to': 1, 'suspend': 1, 'China': 1, 'nuclear': 1, 'has': 1, 'technology': 1, 'its': 1, 'crisis': 1}

str1 = "Hello world, Hello world, hello world,.! hello World, Hello World!"
res1 = {'world': 3, 'Hello': 3, 'World': 2, 'hello': 2}

str2 = "it was the best of times it was the worst of times it was the age of wisdom it was the age of foolishness"
res2 = {'of': 4, 'it': 4, 'the': 4, 'was': 4, 'age': 2, 'times': 2, 'foolishness': 1, 'worst': 1, 'wisdom': 1, 'best': 1}

p = Parser()

class TestParser(unittest.TestCase):

    def test_parser(self):
        self.assertTrue(p.parse(str0), res0)
        self.assertTrue(p.parse(str1), res1)
        self.assertTrue(p.parse(str2), res2)

if __name__ == '__main__':
    unittest.main()