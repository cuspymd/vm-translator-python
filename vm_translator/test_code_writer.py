import unittest
import os
from pathlib import Path
from typing import List, Tuple

from vm_translator.code_writer import CodeWriter


class TestCodeWriter(unittest.TestCase):
    def test_file_processing(self):
        code_writer = CodeWriter("test.vm")
        self.assertFalse(code_writer._file.closed)
        code_writer.close()
        self.assertTrue(code_writer._file.closed)
        os.remove("test.vm")

    def test_write_arithmetic_given_add(self):
        self._test_write_arthimetic("add")

    def test_write_arithmetic_given_sub(self):
        self._test_write_arthimetic("sub")

    def test_write_arithmetic_given_neg(self):
        self._test_write_arthimetic("neg")

    def test_write_arithmetic_given_not(self):
        self._test_write_arthimetic("not")

    def test_write_arithmetic_given_eq(self):
        self._test_write_arthimetic("eq")

    def test_write_arithmetic_given_gt(self):
        self._test_write_arthimetic("gt")

    def test_write_arithmetic_given_lt(self):
        self._test_write_arthimetic("lt")

    def test_write_arithmetic_given_and(self):
        self._test_write_arthimetic("and")

    def test_write_arithmetic_given_or(self):
        self._test_write_arthimetic("or")

    def test_write_arithmetic_given_ltgt(self):
        out_file = "ltgt.asm"

        with CodeWriter(out_file) as cw:
            cw.write_arithmetic("lt")
            cw.write_arithmetic("gt")

        self._verify_output(out_file)
        os.remove(out_file)

    def test_write_push_pop_given_push_local(self):
        self._test_write_push_pop("pushlocal2", [("push", "local", 2)])

    def test_write_push_pop_given_push_argument(self):
        self._test_write_push_pop("pushargument2", [("push", "argument", 2)])

    def test_write_push_pop_given_push_this(self):
        self._test_write_push_pop("pushthis2", [("push", "this", 2)])

    def test_write_push_pop_given_push_that(self):
        self._test_write_push_pop("pushthat2", [("push", "that", 2)])

    def test_write_push_pop_given_pop_local(self):
        self._test_write_push_pop("poplocal2", [("pop", "local", 2)])

    def test_write_push_pop_given_pop_argument(self):
        self._test_write_push_pop("popargument2", [("pop", "argument", 2)])

    def test_write_push_pop_given_pop_this(self):
        self._test_write_push_pop("popthis2", [("pop", "this", 2)])

    def test_write_push_pop_given_pop_that(self):
        self._test_write_push_pop("popthat2", [("pop", "that", 2)])

    def test_write_push_pop_given_push_pointer(self):
        self._test_write_push_pop("pushpointer", [
            ("push", "pointer", 0),
            ("push", "pointer", 1),
        ])

    def test_write_push_pop_given_pop_pointer(self):
        self._test_write_push_pop("poppointer", [
            ("pop", "pointer", 0),
            ("pop", "pointer", 1),
        ])

    def test_write_push_pop_given_push_temp(self):
        self._test_write_push_pop("pushtemp2", [("push", "temp", 2)])

    def test_write_push_pop_given_pop_temp(self):
        self._test_write_push_pop("poptemp2", [("pop", "temp", 2)])

    def test_write_push_pop_given_push_constant(self):
        self._test_write_push_pop("pushconstant2", [("push", "constant", 2)])

    def test_write_push_pop_given_push_static(self):
        self._test_write_push_pop("pushstatic2", [("push", "static", 2)])

    def test_write_push_pop_given_pop_static(self):
        self._test_write_push_pop("popstatic2", [("pop", "static", 2)])

    def test_write_function_given_no_vars(self):
        self._test_write_function("function0", [("Main.test", 0)])

    def test_write_function_given_2_vars(self):
        self._test_write_function("function2", [("Main.test", 2)])

    def _test_write_function(self, test_name: str, commands: List[Tuple[str, int]]):
        out_file = f"{test_name}.asm"

        with CodeWriter(out_file) as cw:
            for (function_name, nvars) in commands:
                cw.write_function(function_name, nvars)

        self._verify_output(out_file)
        os.remove(out_file)

    def _test_write_push_pop(self, test_name: str, commands: List[Tuple[str, str, int]]):
        out_file = f"{test_name}.asm"

        with CodeWriter(out_file) as cw:
            for (command, segment, index) in commands:
                cw.write_push_pop(command, segment, index)

        self._verify_output(out_file)
        os.remove(out_file)

    def _test_write_arthimetic(self, test_command: str):
        out_file = f"{test_command}.asm"

        with CodeWriter(out_file) as cw:
            cw.write_arithmetic(test_command)

        self._verify_output(out_file)
        os.remove(out_file)

    def _load_text(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            return f.read()

    def _verify_output(self, out_file: str):
        out = self._load_text(out_file)
        solution_file = f"test_data/solution_{Path(out_file).stem}.asm"
        solution = self._load_text(solution_file)

        self.assertEqual(out, solution)
