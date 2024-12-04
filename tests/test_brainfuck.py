from io import StringIO, TextIOBase

from brainfuck import Interpreter

HELLO = """++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."""


def test_hello_world():
    input = StringIO()
    output = StringIO()
    interpreter = Interpreter(input=input, output=output)
    interpreter.run(HELLO)
    value = output.getvalue()
    assert value == "Hello World!\n"
