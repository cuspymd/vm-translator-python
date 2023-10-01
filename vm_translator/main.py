import sys
import os

from vm_translator.parser import Parser
from vm_translator.code_writer import CodeWriter
from vm_translator.command import CommandType


def translate(input_path: str):
    folder_path, file_name = os.path.split(input_path)
    file_base_name, _ = os.path.splitext(file_name)
    output_path = os.path.join(folder_path, f"{file_base_name}.asm")

    with open(input_path, "r") as input_file:
        input_text = input_file.read()

    parser = Parser(input_text)
    with CodeWriter(output_path) as code_writer:
        while parser.has_more_lines():
            parser.advance()

            match parser.command_type():
                case CommandType.C_ARITHMETIC:
                    code_writer.write_arithmetic(parser.arg1())
                case CommandType.C_PUSH:
                    code_writer.write_push_pop("push", parser.arg1(), parser.arg2())
                case CommandType.C_POP:
                    code_writer.write_push_pop("pop", parser.arg1(), parser.arg2())
                case CommandType.C_LABEL:
                    code_writer.write_label(parser.arg1())
                case CommandType.C_GOTO:
                    code_writer.write_goto(parser.arg1())
                case CommandType.C_IF:
                    code_writer.write_if(parser.arg1())
                case CommandType.C_FUNCTION:
                    code_writer.write_function(parser.arg1(), parser.arg2())
                case CommandType.C_CALL:
                    code_writer.write_call(parser.arg1(), parser.arg2())
                case CommandType.C_RETURN:
                    code_writer.write_return()


if __name__ == "__main__":
    print(f"Start translating for '{sys.argv[1]}'")
    translate(sys.argv[1])
    print("Completed")
