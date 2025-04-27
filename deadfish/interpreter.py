from io import TextIOWrapper
from sys import stdout
from typing import TextIO


class Interpreter:
    """Deadfish interpreter.

    :param strict: A Boolean flag indicating whether the interpreter should operate in strict mode or not.
    :type strict: bool
    """

    def __init__(self, output: TextIO = stdout, strict: bool = False):
        super().__init__()
        self.output = output
        self.strict = strict

    def run(self, input: str | TextIOWrapper):
        """Runs the specified code.

        :param input: The Deadfish code to run.
        :type input: str | TextIOWrapper
        """
        if isinstance(input, str):
            code = input
        else:
            code = input.read()
        a = 0
        for c in code:
            match c:
                case "i":
                    a += 1
                case "d":
                    a -= 1
                case "s":
                    a *= a
                case "o":
                    print(a, file=self.output)
                case "h":
                    break
                case " " | "\t" | "\n" | "\r":
                    pass
                case _:
                    if self.strict:
                        raise ValueError(f"character '{c}' is not valid")
                    pass
            if a < 0 or a == 256:
                a = 0
