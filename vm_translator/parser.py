from typing import List

from vm_translator.command import CommandType, Command


class Parser:
    def __init__(self, file_text: str):
        self.lines = self._get_valid_lines(file_text)
        self.current_line_number = -1
        self.current_command: Command = None

    def _get_valid_lines(self, file_text: str) -> List[str]:
        return [
            valid_text
            for line in file_text.splitlines()
            if (valid_text := self._get_valid_text(line))
        ]

    def _get_valid_text(self, text: str) -> str:
        COMMENT_ID = "//"
        if COMMENT_ID in text:
            valid_text = text.split(COMMENT_ID)[0]
        else:
            valid_text = text

        return valid_text.strip()

    def has_more_lines(self):
        return self.current_line_number < len(self.lines)-1

    def advance(self):
        self.current_line_number += 1
        self.current_command = Command(self.lines[self.current_line_number])

    def command_type(self) -> CommandType:
        return self.current_command.command_type

    def arg1(self) -> str:
        return self.current_command.arg1

    def arg2(self) -> int:
        return self.current_command.arg2
