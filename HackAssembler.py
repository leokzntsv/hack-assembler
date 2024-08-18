import os
import sys
from enum import Enum


class Cmd:
    def visit(self, visitor):
        return ""


class LabelCmd(Cmd):
    def __init__(self, command: str, command_number: int):
        self.command = command
        self.command_number = command_number
        super().__init__()

    def visit(self, visitor):
        return visitor.label(self)


class AInstructionCmd(Cmd):
    def __init__(self, command: str):
        self.command = command
        super().__init__()

    def visit(self, visitor):
        return visitor.a_instruction(self)


class CInstructionCmd(Cmd):
    def __init__(self, command: str):
        self.command = command
        super().__init__()

    def visit(self, visitor):
        return visitor.c_instruction(self)


# Интерфейс
class CmdVisitor:
    def label(self, label: LabelCmd):
        assert False

    def a_instruction(self, a_instruction: AInstructionCmd):
        assert False

    def c_instruction(self, c_instruction: CInstructionCmd):
        assert False


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


class SymbolTable:
    table = {
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15",
        "SCREEN": "16384",
        "KBD": "24576",
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4",
    }


# Конкретный посетитель
class Translator(CmdVisitor):
    comp_table = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }

    dest_table = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }

    jump_table = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def __init__(self, parser: Parser, symbol_table: SymbolTable):
        self.parser = parser
        self.symbol_table = symbol_table
        self.symbol_memory_address = 16
        super().__init__()

    def label(self, label: LabelCmd):
        # label_symbol = self.parser.parse_label(label)
        # if not label_symbol in symbol_table.table:
        #     symbol_table.table[label_symbol] = label.command_number
        return None

    def a_instruction(self, a_instruction: AInstructionCmd):
        address = self.parser.parse_address(a_instruction)

        if address.isdigit():
            binary_address = bin(int(address))[2:]
        else:
            if address in symbol_table.table:
                binary_address = bin(int(symbol_table.table[address]))[2:]
            else:
                symbol_table.table[address] = self.symbol_memory_address
                binary_address = bin(int(self.symbol_memory_address))[2:]
                self.symbol_memory_address += 1

        instruction = []
        while len(binary_address) + len(instruction) < 15:
            instruction.append("0")

        instruction.append("0")  # op-code
        instruction.append(binary_address)

        return "".join(instruction)

    def c_instruction(self, c_instruction: CInstructionCmd):
        instruction = ["111"]

        comp = parser.parse_comp(c_instruction)
        instruction.append(self.comp_table[comp])

        dest = parser.parse_dest(c_instruction)
        if dest:
            instruction.append(self.dest_table[dest])
        else:
            instruction.append(self.dest_table["null"])

        jump = parser.parse_jump(c_instruction)
        if jump:
            instruction.append(self.jump_table[jump])
        else:
            instruction.append(self.jump_table["null"])

        return "".join(instruction)


if len(sys.argv) > 1:
    full_file_name = sys.argv[1]
else:
    print("Usage: python3 HackAssembler.py <assembler_file_name>")
    sys.exit(1)

file_name, extension = os.path.splitext(full_file_name)

if not extension or extension != ".asm":
    print("File's extension must be of type '.asm'")
    sys.exit(1)

if not os.path.exists(full_file_name):
    print(f"There is no file named {full_file_name}")
    sys.exit(1)

parser = Parser(file_name=full_file_name)
symbol_table = SymbolTable()
translator = Translator(parser, symbol_table)


# First Pass

while parser.has_more_commands():
    cmd = parser.advance()
    if type(cmd) is LabelCmd:
        label = parser.parse_label(cmd)
        symbol_table.table[label] = cmd.command_number


# Second Pass

parser.reset()

with open(f"{file_name}.hack", "w") as f:
    while parser.has_more_commands():
        cmd = parser.advance()
        instruction_bits = cmd.visit(translator)
        if instruction_bits:
            f.write(instruction_bits + "\n")
