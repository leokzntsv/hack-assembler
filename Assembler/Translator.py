from Cmd import AInstructionCmd, CInstructionCmd, LabelCmd
from CmdVisitor import CmdVisitor
from Parser import Parser
from SymbolTable import SymbolTable


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
            if address in self.symbol_table.table:
                binary_address = bin(int(self.symbol_table.table[address]))[2:]
            else:
                self.symbol_table.table[address] = self.symbol_memory_address
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

        comp = self.parser.parse_comp(c_instruction)
        instruction.append(self.comp_table[comp])

        dest = self.parser.parse_dest(c_instruction)
        if dest:
            instruction.append(self.dest_table[dest])
        else:
            instruction.append(self.dest_table["null"])

        jump = self.parser.parse_jump(c_instruction)
        if jump:
            instruction.append(self.jump_table[jump])
        else:
            instruction.append(self.jump_table["null"])

        return "".join(instruction)
