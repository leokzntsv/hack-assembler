from Cmd import AInstructionCmd, CInstructionCmd, LabelCmd


# Интерфейс
class CmdVisitor:
    def label(self, label: LabelCmd):
        assert False

    def a_instruction(self, a_instruction: AInstructionCmd):
        assert False

    def c_instruction(self, c_instruction: CInstructionCmd):
        assert False
