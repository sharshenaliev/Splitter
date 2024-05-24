import unittest
import re
from split_msg import split_message


class TestStringMethods(unittest.TestCase):
    max_len = 1000
    source = "source.html"
    litte_max_len = 1
    message_1 = "Error:"
    message_2 = "Max_len is less than one tag block"

    def test_split_message(self):
        with open(self.source, "r", encoding='utf-8') as f:
            text = f.read()
        for part in split_message(text, self.max_len):
            self.assertLessEqual(len(part[1]), self.max_len) 
            self.assertEqual(len(re.findall("<\w+", part[1])), 
                len(re.findall("</\w+", part[1])))

    def test_error(self):
        with open(self.source, "r", encoding='utf-8') as f:
            text = f.read()
        for part in split_message(text, self.litte_max_len):
            self.assertEqual(part[0], self.message_1)
            self.assertEqual(part[1], self.message_2)

if __name__ == '__main__':
    unittest.main()
    