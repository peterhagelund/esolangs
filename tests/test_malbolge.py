from io import StringIO

from malbolge import Interpreter

HELLO = """(=<`#9]~6ZY327Uv4-QsqpMn&+Ij\"'E%e{Ab~w=_:]Kw%o44Uqp0/Q?xNvL:`H%c#DD2^WV>gY;dts76qKJImZkj"""


def test_hello_world():
    input = StringIO()
    output = StringIO()
    interpreter = Interpreter(input=input, output=output)
    interpreter.run(HELLO)
    value = output.getvalue()
    assert value == "Hello, world."
