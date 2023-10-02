import sys
import os
from pathlib import Path

from vm_translator.parser import Parser
from vm_translator.code_writer import CodeWriter
from vm_translator.command import CommandType


def translate(input_path_str: str):
    input_path = Path(input_path_str)
    if input_path.is_file():
        translate_file(input_path_str)
    elif input_path.is_dir():
        translate_folder(input_path)


def translate_file(input_path: str) -> Path:
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

    return Path(output_path)


def translate_folder(input_folder: Path):
    vm_files = sorted(input_folder.glob("*.vm"))
    asm_files = [translate_file(str(vm_file)) for vm_file in vm_files]
    out_file_path = input_folder / f"{input_folder.name}.asm"

    with out_file_path.open(mode="w") as out_file:
        for asm_file_path in asm_files:
            with asm_file_path.open(mode="r") as asm_file:
                asm_text = asm_file.read()
                out_file.write(f"// > {asm_file_path.name}\n{asm_text}")

            asm_file_path.unlink()


if __name__ == "__main__":
    print(f"Start translating for '{sys.argv[1]}'")
    translate(sys.argv[1])
    print("Completed")
