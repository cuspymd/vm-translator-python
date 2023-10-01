from pathlib import Path
from typing import List


class CodeWriter:
    def __init__(self, file_path: str):
        self._file = open(file_path, "w+")
        self._file_base_name = Path(file_path).stem
        self._current_function_name = ""
        self._branch_index = 1
        self._first_pop = [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
        ]
        self._second_pop = [
            "@SP",
            "M=M-1",
            "A=M",
        ]
        self._final_push = [
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write_end(self):
        end_statements = [
            "(END)",
            "@END",
            "0;JMP",
        ]
        self._write_statements(end_statements)

    def _write_statements(self, statements: List[str]):
        statements = [self._post_process(statement) for statement in statements]
        for statement in statements:
            self._file.write(statement)

    def _post_process(self, statement: str) -> str:
        if statement[0] in ("(", "/"):
            return f"{statement}\n"
        else:
            return f"  {statement}\n"

    def write_arithmetic(self, command: str):
        match command:
            case "add":
                assem = self._get_binary_input_asm("add", ["D=D+M"])
            case "sub":
                assem = self._get_binary_input_asm("sub", ["D=M-D"])
            case "and":
                assem = self._get_binary_input_asm("and", ["D=D&M"])
            case "or":
                assem = self._get_binary_input_asm("or", ["D=D|M"])
            case "neg":
                assem = self._get_unary_input_asm("neg", ["D=-D"])
            case "not":
                assem = self._get_unary_input_asm("not", ["D=!D"])
            case "eq":
                assem = self._get_binary_input_asm("eq", self._get_comparison_asm("eq"))
            case "gt":
                assem = self._get_binary_input_asm("gt", self._get_comparison_asm("gt"))
            case "lt":
                assem = self._get_binary_input_asm("lt", self._get_comparison_asm("lt"))

        self._write_statements(assem)

    def _get_binary_input_asm(self, command_name: str, command_statements: List[str]) -> List[str]:
        return [
            f"// {command_name}",
            *self._first_pop,
            *self._second_pop,
            *command_statements,
            *self._final_push,
        ]

    def _get_unary_input_asm(self, command_name: str, command_statements: List[str]) -> List[str]:
        return [
            f"// {command_name}",
            *self._first_pop,
            *command_statements,
            *self._final_push,
        ]

    def _get_comparison_asm(self, command: str) -> List[str]:
        jump_symbol_table = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }
        statements = [
            "D=M-D",
            f"@THEN{self._branch_index}",
            f"D;{jump_symbol_table[command]}",
            "D=0",
            f"@END{self._branch_index}",
            "0;JMP",
            f"(THEN{self._branch_index})",
            "D=-1",
            f"(END{self._branch_index})",
        ]
        self._branch_index += 1
        return statements

    def write_push_pop(self, command: str, segment: str, index: int):
        segment_symbol_table = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        assem = [f"// {command} {segment} {index}"]

        match (command, segment, index):
            case ("push", ("local" | "argument" | "this" | "that") as segment, index):
                assem += [
                    f"@{segment_symbol_table[segment]}",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                    *self._final_push,
                ]
            case ("pop", ("local" | "argument" | "this" | "that") as segment, index):
                assem += [
                    f"@{segment_symbol_table[segment]}",
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@R13",
                    "A=M",
                    "M=D",
                ]
            case ("push", "pointer", 0):
                assem += [
                    "@THIS",
                    "D=M",
                    *self._final_push,
                ]
            case ("push", "pointer", 1):
                assem += [
                    "@THAT",
                    "D=M",
                    *self._final_push,
                ]
            case ("pop", "pointer", 0):
                assem += [
                    *self._first_pop,
                    "@THIS",
                    "M=D",
                ]
            case ("pop", "pointer", 1):
                assem += [
                    *self._first_pop,
                    "@THAT",
                    "M=D",
                ]
            case ("push", "temp", index):
                assem += [
                    "@5",
                    "D=A",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                    *self._final_push,
                ]
            case ("pop", "temp", index):
                assem += [
                    "@5",
                    "D=A",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                    *self._first_pop,
                    "@R13",
                    "A=M",
                    "M=D",
                ]
            case ("push", "constant", index):
                assem += [
                    f"@{index}",
                    "D=A",
                    *self._final_push,
                ]
            case ("push", "static", index):
                assem += [
                    f"@{self._file_base_name}.{index}",
                    "D=M",
                    *self._final_push,
                ]
            case ("pop", "static", index):
                assem += [
                    *self._first_pop,
                    f"@{self._file_base_name}.{index}",
                    "M=D",
                ]

        self._write_statements(assem)

    def write_function(self, function_name: str, nvars: int):
        statements = [
            f"// function {function_name} {nvars}",
            f"({function_name})",
            *self._get_push_nvars_asm(nvars),
        ]
        self._write_statements(statements)
        self._current_function_name = function_name

    def _get_push_nvars_asm(self, nvars: int) -> List[str]:
        push_statements = [
            "@SP",
            "A=M",
            "M=0",
            "@SP",
            "M=M+1",
        ]
        return [item for _ in range(nvars) for item in push_statements]

    def write_label(self, label: str):
        statements = [
            f"// label {label}",
            f"({self._get_label_prefix(label)}${label})",
        ]
        self._write_statements(statements)

    def write_goto(self, label: str):
        statements = [
            f"// goto {label}",
            f"@{self._get_label_prefix(label)}${label}",
            "0;JMP"
        ]
        self._write_statements(statements)

    def _get_label_prefix(self, label: str):
        return f"{self._current_function_name}" if self._current_function_name \
            else f"{self._file_base_name}"
