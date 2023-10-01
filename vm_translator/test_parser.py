import unittest

from vm_translator.parser import Parser
from vm_translator.command import CommandType


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

    def test_command_type_given_label_command(self):
        parser = Parser("label LABEL")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_LABEL)

    def test_command_type_given_goto_command(self):
        parser = Parser("goto LABEL")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_GOTO)

    def test_command_type_given_if_command(self):
        parser = Parser("if-goto LABEL")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_IF)

    def test_command_type_given_function_command(self):
        parser = Parser("function FUNC 0")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_FUNCTION)

    def test_command_type_given_call_command(self):
        parser = Parser("call FUNC 0")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_CALL)

    def test_command_type_given_return_command(self):
        parser = Parser("return")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_RETURN)

    def test_command_type_given_stack_command(self):
        parser = Parser("push constant 17\npop local 2")
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_PUSH)
        parser.advance()
        self.assertEqual(parser.command_type(), CommandType.C_POP)

    def test_arg_given_arithmetic_command(self):
        parser = Parser("add")
        parser.advance()
        self.assertEqual(parser.arg1(), "add")

    def test_arg_given_push_command(self):
        parser = Parser("push constant 1")
        parser.advance()
        self.assertEqual(parser.arg1(), "constant")
        self.assertEqual(parser.arg2(), 1)

    def test_arg_given_pop_command(self):
        parser = Parser("pop temp 12")
        parser.advance()
        self.assertEqual(parser.arg1(), "temp")
        self.assertEqual(parser.arg2(), 12)

    def test_arg_given_invalid_type(self):
        parser = Parser("sub")
        parser.advance()
        with self.assertRaises(Exception):
            parser.arg2()
