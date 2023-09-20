import unittest

from vm_translator.parser import Parser


class TestParser(unittest.TestCase):
    def test_has_more_lines_given_one_line(self):
        parser = Parser("push constant 17")
        self.assertTrue(parser.has_more_lines())

    def test_has_more_lines_given_empty_line(self):
        parser = Parser("")
        self.assertFalse(parser.has_more_lines())

        parser = Parser("	")
        self.assertFalse(parser.has_more_lines())

        parser = Parser("\n   \n     \n")
        self.assertFalse(parser.has_more_lines())

        parser = Parser("\r\n   \r\n     \r\n")
        self.assertFalse(parser.has_more_lines())

        parser = Parser("\n   \n     push local 2\n")
        self.assertTrue(parser.has_more_lines())

    def test_has_more_lines_given_comment_line(self):
        parser = Parser("// comment")
        self.assertFalse(parser.has_more_lines())

    def test_advance(self):
        parser = Parser("push constant 17")
        self.assertTrue(parser.has_more_lines())
        parser.advance()
        self.assertFalse(parser.has_more_lines())

    def test_advance_given_two_lines(self):
        parser = Parser("push constant 17\npush local 2")
        self.assertTrue(parser.has_more_lines())
        parser.advance()
        self.assertTrue(parser.has_more_lines())
        parser.advance()
        self.assertFalse(parser.has_more_lines())

    def test_command_type_given_arithmetic_command(self):
        commands = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")
        for command in commands:
            parser = Parser(command)
            parser.advance()
            self.assertEqual(parser.command_type(), CommandType.C_ARITHMETIC)

