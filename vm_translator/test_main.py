import unittest
import os
import vm_translator.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_main_given_stack_commands(self):
        self._test_vm_file("Add")

    def test_main_given_control_commands(self):
        self._test_vm_file("Control")

    def _test_vm_file(self, test_name: str):
        main.translate(f"test_data/{test_name}.vm")

        out_file_path = f"test_data/{test_name}.asm"
        with open(out_file_path, "r") as out_file:
            out_assem = out_file.read()

        with open(f"test_data/solution_{test_name}.asm", "r") as solution_file:
            solution_assem = solution_file.read()

        self.assertEqual(out_assem, solution_assem)
        os.remove(out_file_path)
