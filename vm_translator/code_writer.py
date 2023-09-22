from pathlib import Path


class CodeWriter:
    def __init__(self, file_path: str):
        self._file = open(file_path, "w+")
        self._file_base_name = Path(file_path).stem
        self._branch_index = 1
        self._first_pop = '''@SP
M=M-1
A=M
D=M
'''
        self._second_pop = '''@SP
M=M-1
A=M
'''
        self._final_push = '''@SP
A=M
M=D
@SP
M=M+1
'''

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write_arithmetic(self, command: str):
        match command:
            case "add":
                assem = self._get_binary_input_asm("add", "D=D+M\n")
            case "sub":
                assem = self._get_binary_input_asm("sub", "D=D-M\n")
            case "and":
                assem = self._get_binary_input_asm("and", "D=D&M\n")
            case "or":
                assem = self._get_binary_input_asm("or", "D=D|M\n")
            case "neg":
                assem = self._get_unary_input_asm("neg", "D=-D\n")
            case "not":
                assem = self._get_unary_input_asm("not", "D=!D\n")
            case "eq":
                assem = self._get_binary_input_asm("eq", self._get_comparison_asm("eq"))
            case "gt":
                assem = self._get_binary_input_asm("gt", self._get_comparison_asm("gt"))
            case "lt":
                assem = self._get_binary_input_asm("lt", self._get_comparison_asm("lt"))

        self._file.write(assem)

    def _get_binary_input_asm(self, command_name: str, command_asm: str):
        return f"// {command_name}\n" + self._first_pop + self._second_pop + \
            command_asm + self._final_push

    def _get_unary_input_asm(self, command_name: str, command_asm: str):
        return f"// {command_name}\n" + self._first_pop + command_asm + self._final_push

    def _get_comparison_asm(self, command: str):
        assem_template = '''D=D-M
@THEN{index}
D;{jump}
@0
D=A
@END{index}
;JMP
(THEN{index})
@1
D=A
(END{index})
'''
        match command:
            case "eq":
                assem = assem_template.format(jump="JEQ", index=self._branch_index)
            case "gt":
                assem = assem_template.format(jump="JGT", index=self._branch_index)
            case "lt":
                assem = assem_template.format(jump="JLT", index=self._branch_index)

        self._branch_index += 1
        return assem

    def write_push_pop(self, command: str, segment: str, index: int):
        assem = f"// {command} {segment} {index}\n"

        match (command, segment, index):
            case ("push", "local", index):
                assem += f'''@LCL
D=M
@{index}
A=D+A
D=M
{self._final_push}'''
            case ("pop", "local", index):
                assem += f'''@LCL
D=M
@{index}
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
'''
            case ("push", "pointer", 0):
                assem += f'''@THIS
D=M
{self._final_push}'''
            case ("push", "pointer", 1):
                assem += f'''@THAT
D=M
{self._final_push}'''
            case ("pop", "pointer", 0):
                assem += f'''{self._first_pop}@THIS
M=D
'''
            case ("pop", "pointer", 1):
                assem += f'''{self._first_pop}@THAT
M=D
'''
            case ("push", "temp", index):
                assem += f'''@5
D=A
@{index}
A=D+A
D=M
{self._final_push}'''
            case ("pop", "temp", index):
                assem += f'''@5
D=A
@{index}
D=D+A
@R13
M=D
{self._first_pop}@R13
A=M
M=D
'''
            case ("push", "constant", index):
                assem += f'''@{index}
D=A
{self._final_push}'''
            case ("push", "static", index):
                assem += f'''@{self._file_base_name}.{index}
D=M
{self._final_push}'''
            case ("pop", "static", index):
                assem += f'''{self._first_pop}@{self._file_base_name}.{index}
M=D
'''

        self._file.write(assem)
