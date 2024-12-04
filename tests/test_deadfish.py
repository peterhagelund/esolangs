from io import StringIO

from deadfish import Interpreter

HELLO = """iiisdsiiiiiiiioiiiiiiiiiiiiiiiiiiiiiiiiiiiiioiiiiiiiooiiio
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddoddddddddddddo
dddddddddddddddddddddsddoddddddddoiiioddddddoddddddddo
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddo"""


def test_hello_world():
    output = StringIO()
    interpreter = Interpreter(output=output, strict=True)
    interpreter.run(HELLO)
    value = output.getvalue()
    message = "".join([chr(int(v)) for v in value.split()])
    assert message == "Hello, world!"
