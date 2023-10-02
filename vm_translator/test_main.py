import unittest
import os
from pathlib import Path
import vm_translator.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_main_given_stack_commands(self):
        self._test_vm("Add.vm")

    def test_main_given_control_commands(self):
        self._test_vm("Control.vm")

    def test_main_given_folder(self):
        self._test_vm("TestFolder")

    def test_main_given_multi_comparison_commands(self):
        self._test_vm("TestInternalSymbol")

    def _test_vm(self, test_dest: str):
        test_name = Path(test_dest).stem
        is_folder = test_name == test_dest
        main.translate(f"test_data/{test_dest}")

        out_file_path = f"test_data/{test_name}/{test_name}.asm" if is_folder else \
            f"test_data/{test_name}.asm"

        with open(out_file_path, "r") as out_file:
            out_assem = out_file.read()

        with open(f"test_data/solution_{test_name}.asm", "r") as solution_file:
            solution_assem = solution_file.read()

        self.assertEqual(out_assem, solution_assem)
        os.remove(out_file_path)
