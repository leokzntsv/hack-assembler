from enum import Enum

from Cmd import AInstructionCmd, CInstructionCmd, Cmd, LabelCmd


class Parser:
    class Symbols(Enum):
        COMMENT = "//"
        A_INSTRUCTION = "@"
        C_INSTRUCTION_DEST = "="
        C_INSTRUCTION_JUMP = ";"
        LABEL = "("

    def __init__(self, file_name):
        self.file_name = file_name
        self.reset()

    def has_more_commands(self):
        current_position = self.position
        has_more_lines = True

        while has_more_lines:
            line = self.__get_line(position=current_position)
            if not line:
                has_more_lines = False
                break

            current_position += len(line) + 1
            processed_line = self.__process_line(line=line)

            if processed_line:
                return True

        return False

    def advance(self) -> Cmd:
        line = self.__get_next_line()

        if not line:
            return Cmd()

        self.position += len(line) + 1
        processed_line = self.__process_line(line=line)

        if processed_line:
            command = self.__parse_command(processed_line)

            if type(command) is not LabelCmd:
                self.current_command_number += 1

            return command
        else:
            return self.advance()

    def reset(self):
        self.position = 0
        self.current_command_number = -1

    def parse_label(self, label_cmd: LabelCmd):
        return label_cmd.command[1:-1]

    def parse_address(self, ai_cmd: AInstructionCmd):
        return ai_cmd.command[1:]

    def parse_dest(self, ci_cmd: CInstructionCmd):
        end_index = ci_cmd.command.find(Parser.Symbols.C_INSTRUCTION_DEST.value)
        if end_index != -1:
            return ci_cmd.command[:end_index]

    def parse_comp(self, ci_cmd: CInstructionCmd):
        command = ci_cmd.command
        start_index = command.find(Parser.Symbols.C_INSTRUCTION_DEST.value)
        end_index = command.find(Parser.Symbols.C_INSTRUCTION_JUMP.value)

        if end_index == -1:
            end_index = len(command)

        return command[(start_index + 1) : end_index]

    def parse_jump(self, ci_cmd: CInstructionCmd):
        start_index = ci_cmd.command.find(Parser.Symbols.C_INSTRUCTION_JUMP.value)

        if start_index != -1:
            return ci_cmd.command[(start_index + 1) :]

    # Private Methods

    def __parse_command(self, line) -> Cmd:
        if line[0] == Parser.Symbols.A_INSTRUCTION.value:
            return AInstructionCmd(line)
        elif line[0] == Parser.Symbols.LABEL.value:
            return LabelCmd(
                command=line, command_number=self.current_command_number + 1
            )
        else:
            return CInstructionCmd(line)

    def __process_line(self, line):
        line = self.__strip_comment(line=line)
        line = self.__strip_whitespace(line=line)
        return line

    def __get_next_line(self):
        return self.__get_line(position=self.position)

    def __get_line(self, position):
        with open(self.file_name, "r") as f:
            f.seek(position)
            line = f.readline()
            return line

    def __strip_comment(self, line):
        return line.split(Parser.Symbols.COMMENT.value)[0]

    def __strip_whitespace(self, line):
        return line.strip()
