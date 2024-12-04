from io import StringIO

from befunge import Interpreter

HELLO = """>              v
v  ,,,,,"Hello"<
>47+4*,48*,    v
v,,,,,,"World!"<
>25*,@
"""


def test_hello_world():
    """Tests the `Interpreter` can execute a simple "Hello, World!" program."""
    input = StringIO()
    output = StringIO()
    interpreter = Interpreter(input=input, output=output)
    interpreter.run(HELLO)
    value = output.getvalue()
    assert value == "Hello, World!\n"
