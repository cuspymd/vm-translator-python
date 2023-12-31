from enum import Enum


class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Command:
    def __init__(self, text: str):
        match text.split():
            case ["push", arg1, arg2]:
                self._command_type = CommandType.C_PUSH
                self._arg1 = arg1
                self._arg2 = int(arg2)
            case ["pop", arg1, arg2]:
                self._command_type = CommandType.C_POP
                self._arg1 = arg1
                self._arg2 = int(arg2)
            case ["label", label]:
                self._command_type = CommandType.C_LABEL
                self._arg1 = label
                self._arg2 = None
            case ["goto", label]:
                self._command_type = CommandType.C_GOTO
                self._arg1 = label
                self._arg2 = None
            case ["if-goto", label]:
                self._command_type = CommandType.C_IF
                self._arg1 = label
                self._arg2 = None
            case ["function", function_name, nvars]:
                self._command_type = CommandType.C_FUNCTION
                self._arg1 = function_name
                self._arg2 = int(nvars)
            case ["call", function_name, nvars]:
                self._command_type = CommandType.C_CALL
                self._arg1 = function_name
                self._arg2 = int(nvars)
            case ["return"]:
                self._command_type = CommandType.C_RETURN
                self._arg1 = None
                self._arg2 = None
            case [command, *_]:
                self._command_type = CommandType.C_ARITHMETIC
                self._arg1 = command
                self._arg2 = None

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @property
    def arg1(self) -> str:
        return self._arg1

    @property
    def arg2(self) -> int:
        if self._arg2 is None:
            raise Exception("Not supported type")
        return self._arg2
