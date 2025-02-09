import os
import sys

from Cmd import LabelCmd
from Parser import Parser
from SymbolTable import SymbolTable
from Translator import Translator

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
    if isinstance(cmd, LabelCmd):
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
