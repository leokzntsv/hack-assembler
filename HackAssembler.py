import os
import sys
from enum import Enum


class Parser:
    class Symbols:
        comment = "//"
        a_instruction = "@"
        c_instruction_dest = "="
        c_instruction_jump = ";"
        label_declaration = "("

    class Command(Enum):
        A_INSTRUCTION = 0
        C_INSTRUCTION = 1
        LABEL = 2
        UNKNOWN = 3

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

    def advance(self):
        line = self.__get_next_line()

        if not line:
            return

        self.position += len(line) + 1
        processed_line = self.__process_line(line=line)

        if processed_line:
            self.current_command_type = self.__get_command_type(processed_line)
            self.current_command = processed_line

            if self.current_command_type != Parser.Command.LABEL:
                self.current_command_number += 1
        else:
            self.advance()

    def reset(self):
        self.position = 0
        self.current_command_number = -1
        self.current_command = ""
        self.current_command_type = Parser.Command.UNKNOWN

    def get_address(self):
        if self.current_command_type == Parser.Command.A_INSTRUCTION:
            return self.current_command[1:]

    def get_destination(self):
        if self.current_command_type == Parser.Command.C_INSTRUCTION:
            end_index = self.current_command.find(Parser.Symbols.c_instruction_dest)
            if end_index != -1:
                return self.current_command[:end_index]

    def get_computation(self):
        if self.current_command_type == Parser.Command.C_INSTRUCTION:
            start_index = self.current_command.find(Parser.Symbols.c_instruction_dest)
            end_index = self.current_command.find(Parser.Symbols.c_instruction_jump)

            if end_index == -1:
                end_index = len(self.current_command)

            return self.current_command[(start_index + 1) : end_index]

    def get_jump(self):
        if self.current_command_type == Parser.Command.C_INSTRUCTION:
            start_index = self.current_command.find(Parser.Symbols.c_instruction_jump)

            if start_index != -1:
                return self.current_command[(start_index + 1) :]

    def get_label(self):
        if self.current_command_type == Parser.Command.LABEL:
            return self.current_command[1:-1]

    # Private Methods

    def __get_command_type(self, command):
        if not command:
            return Parser.Command.UNKNOWN

        if command[0] == Parser.Symbols.a_instruction:
            return Parser.Command.A_INSTRUCTION
        elif command[0] == Parser.Symbols.label_declaration:
            return Parser.Command.LABEL
        else:
            return Parser.Command.C_INSTRUCTION

    def __process_line(self, line):
        line = self.__strip_comment(line=line)
        line = self.__strip_whitespace(line=line)
        return line

    def __get_next_line(self):
        return self.__get_line(position=self.position)

    def __get_line(self, position):
        with open(self.file_name, "r") as file:
            file.seek(position)
            line = file.readline()
            return line

    def __strip_comment(self, line):
        return line.split(Parser.Symbols.comment)[0]

    def __strip_whitespace(self, line):
        return line.strip()


class Translator:
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

    def address_bits(self, address):
        binary_address = bin(int(address))[2:]
        while len(binary_address) < 15:
            binary_address = "0" + binary_address
        return binary_address

    def dest_bits(self, instruction):
        if instruction:
            return self.dest_table[instruction]
        else:
            return self.dest_table["null"]

    def comp_bits(self, instruction):
        if instruction:
            return self.comp_table[instruction]

    def jump_bits(self, instruction):
        if instruction:
            return self.jump_table[instruction]
        else:
            return self.jump_table["null"]


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
translator = Translator()
symbol_table = {
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

# First Pass
while parser.has_more_commands():
    parser.advance()
    label = parser.get_label()
    if label:
        symbol_table[label] = str(parser.current_command_number + 1)

# Second Pass
parser.reset()
symbol_memory_address = 16

with open(f"{file_name}.hack", "w") as file:
    while parser.has_more_commands():
        parser.advance()

        result_instruction_bits = ""

        address_symbol = parser.get_address()
        comp_instruction = parser.get_computation()

        if address_symbol:
            if address_symbol.isdigit():
                address = address_symbol
                address_bits = translator.address_bits(address=address_symbol)
            else:
                if address_symbol in symbol_table:
                    address_bits = translator.address_bits(
                        address=symbol_table[address_symbol]
                    )
                    address = symbol_table[address_symbol]
                else:
                    symbol_table[address_symbol] = symbol_memory_address
                    address_bits = translator.address_bits(
                        address=symbol_memory_address
                    )
                    symbol_memory_address += 1

            result_instruction_bits += "0" + address_bits

        elif comp_instruction:
            dest_instruction = parser.get_destination()
            jump_instruction = parser.get_jump()
            dest_bits = translator.dest_bits(instruction=dest_instruction)
            comp_bits = translator.comp_bits(instruction=comp_instruction)
            jump_bits = translator.jump_bits(instruction=jump_instruction)

            result_instruction_bits += "111" + comp_bits + dest_bits + jump_bits

        else:
            continue

        if result_instruction_bits:
            file.write(result_instruction_bits + "\n")
