import befunge
import brainfuck
import deadfish
import malbolge

BEFUNGE_HELLO = """>              v
v  ,,,,,"Hello"<
>47+4*,48*,    v
v,,,,,,"World!"<
>25*,@
"""

BRAINFUCK_HELLO = """++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."""

DEADFISH_HELLO = """iiisdsiiiiiiiioiiiiiiiiiiiiiiiiiiiiiiiiiiiiioiiiiiiiooiiio
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddoddddddddddddo
dddddddddddddddddddddsddoddddddddoiiioddddddoddddddddo
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddo"""

MALBOLGE_HELLO = """(=<`#9]~6ZY327Uv4-QsqpMn&+Ij"'E%e{Ab~w=_:]Kw%o44Uqp0/Q?xNvL:`H%c#DD2^WV>gY;dts76qKJImZkj"""


def main():
    befunge_say_hello()
    brainfuck_say_hello()
    deadfish_say_hello()
    malbolge_say_hello()


def befunge_say_hello():
    interpreter = befunge.Interpreter()
    interpreter.run(BEFUNGE_HELLO)


def brainfuck_say_hello():
    interpreter = brainfuck.Interpreter()
    interpreter.run(BRAINFUCK_HELLO)


def deadfish_say_hello():
    interpreter = deadfish.Interpreter()
    interpreter.run(DEADFISH_HELLO)


def malbolge_say_hello():
    interpreter = malbolge.Interpreter()
    interpreter.run(MALBOLGE_HELLO)


if __name__ == "__main__":
    main()
