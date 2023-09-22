import unittest
import os
import vm_translator.main as main


class TestMain(unittest.TestCase):
    def test_main(self):
        main.translate("test_data/Add.vm")

        out_file_path = "test_data/Add.asm"
        with open(out_file_path, "r") as out_file:
            out_assem = out_file.read()

        with open("test_data/solution_Add.asm", "r") as solution_file:
            solution_assem = solution_file.read()

        self.assertEqual(out_assem, solution_assem)
        os.remove(out_file_path)
