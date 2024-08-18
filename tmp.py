# Using Polymorphism

## Commands

class Cmd:
    def visit(self, visitor):
        assert(False)

class LabelCmd(Cmd):
    def visit(self, visitor):
        return visitor.label(self)

class AddressCmd(Cmd):
    def visit(self, visitor):
        return visitor.address(self)

class CommandCmd(Cmd):
    def visit(self, visitor):
        return visitor.command(self)


## Visitors

class CmdVisitor:
    def label(self, label: LabelCmd):
        assert(False)
    def address(self, address: AddressCmd):
        assert(False)
    def command(self, command: CommandCmd):
        assert(False)


class Translator(CmdVisitor):
    def label(self, label: LabelCmd):
        assert(False)
    def address(self, address: AddressCmd):
        assert(False)
    def command(self, command: CommandCmd):
        assert(False)


## Usage

with open("") as f:
    parser = Parser(f)
    while parser.has_next_command():
        cmd = parser.parse_next_command()
        cmd.visit(translator)    


commands = [LabelCmd(...), AddressCmd(...), CommandCmd(...), CommandCmd(...), ...]
translator = Translator(...)
for cmd in cmd_iter:
    cmd.visit(translator)


## Translation

def translateLabel(cmd: Cmd):
    assert(cmd.type == CmdType.LABEL)
    pass
def translateAddress(address: AddressCmd):
    pass
def translateCommand(command: CommandCmd):
    pass


# Using Enums and Union

class CmdType(Enum):
    LABEL = 1
    ADDRESS = 2
    COMMAND = 3

class Cmd:
    type: CmdType
    # # union {
    # label: Optional[LabelCmd]
    # address: Optional[AddressCmd]
    # command: Optional[CommandCmd]
    # # }
    value: Union[LabelCmd, AddressCmd, CommandCmd]


## Translation

def translateLabel(label: LabelCmd):    
    pass
def translateAddress(address: AddressCmd):
    pass
def translateCommand(command: CommandCmd):
    pass

dispatchTable = {
    CmdType.LABEL: translateLabel,
    CmdType.ADDRESS: translateAddress,
    CmdType.COMMAND: translateCommand,
}
for cmd in cmd_iter:
    dispatchTable[cmd.type](cmd)



# True Parser – top down look-ahead-1 recursive descent parser

'\0'

class Stream:
    def la1() -> str:
        pass
    def consume1():
        pass


class FileStream(Stream):
    ...


program = "............."



abc   =  23423


def consume_int(stream):
    assert(is_digit(stream.la1()))
    result = []
    while is_digit(stream.la1()):
        result.append(stream.la1()) # Better than += to string
        stream.consume1()
    return ''.join(result)

def consume_identifier(stream):
    assert(is_alpha(stream.la1()))
    pass

def consume_optional_spaces(stream):
    while is_whitespace(stream.la1()):
        stream.consume1()

def consume_assignment(stream):
    identifier = consume_identifier(stream)
    consume_optional_spaces(steam)
    consume_single_char(steam, "=")
    consume_optional_spaces(stream)
    value = consume_int(stream)
    return AssignOp(identifier, value)




def consume_optional_spaces(stream):
    while stream.la1() in ' \t\r':
        stream.consume1()

def consume_newline_or_oef(stream):
    switch stream.la1():
        case '\0':
            break
        case '\n':
            steam.consume1()
        default:
            raise ParseError(...)

def consume_single_char(steam, predicate):
    if predicate(stream.la1()):
        return stream.consume1()
    raise ParseError()

# LABEL_NAME
def consume_label_name(stream):
    name = []
    name.append(consume_single_char(stream, is_alpha))
    while is_alpha(steam.la1()) or is_digit(stream.la1()) or ...:
        name.append(stream.consume1())
    return ''.join(name)

# (LABEL_NAME)
def consume_label(stream):
    consume_single_char(stream, lambda c: c == '(')
    label_name = consume_label_name(stream)
    consume_single_char(stream, lambda c: c == ')')
    return label_name

def consume_address(stream):
    consume_single_char(steam, lambda c: c == '@')
    switch stream.la():
        case '0'...'9':
            nums = consume_numeric_address(stream)
            return AddressCmd(AddressCmdType.NUMERIC, nums)
        case 'a'...'z' | 'A'...'Z':
            identifier = consume_label_name(stream)
            return AddressCmd(AddressCmdType.SYMBOLIC, identifier)
        default:
            raise ParseError()

def consume_cmd(stream) -> Cmd:
    cmd = None
    consume_spaces(stream)
    switch stream.la1():
        case '(':
            label = consume_label(stream)
            cmd = Cmd(CmdType.LABEL, label)
        case '@':
            address = consume_address(stream)
            cmd = Cmd(CmdType.ADDRESS, address)
        default:
            command = consume_command(stream)
            cmd = Cmd(CmdType.COMMAND, command)
    consume_optional_spaces(stream)
    consume_newline_or_oef(steam)
    return cmd

def consume_program(stream):
    while True:
        if stream.la1() == '\0':
            return
        yield consume_cmd(stream)

for cmd in consume_program(stream):
    translator.translate(cmd)


# top down look-ahead-1 recursive descent parser


