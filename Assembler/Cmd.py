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
