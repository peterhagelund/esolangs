from io import TextIOWrapper
from sys import stdin, stdout


class Interpreter:
    """Brainfuck interpreter.

    :param size: The memory size.
    :type size: int
    """

    def __init__(self, input: TextIOWrapper = stdin, output: TextIOWrapper = stdout, size: int = 30000):
        super().__init__()
        self.input = input
        self.output = output
        self._size = size

    def run(self, input: str | TextIOWrapper):
        """Runs the specified code.

        :param input: The Brainfuck code to run.
        :type input: str | TextIOWrapper
        :raises ValueError: If the code is not valid Brainfuck.
        """
        if isinstance(input, str):
            code = input
        else:
            code = input.read()
        stack = [0 for _ in range(len(code))]
        stack_ptr = 0
        targets = [0 for _ in range(len(code))]
        for code_ptr in range(len(code)):
            match code[code_ptr]:
                case '[':
                    stack[stack_ptr] = code_ptr
                    stack_ptr += 1
                case ']':
                    if stack_ptr == 0:
                        raise ValueError(f'unmatched "]" at position {code_ptr}')
                    stack_ptr -= 1
                    targets[code_ptr] = stack[stack_ptr]
                    targets[stack[stack_ptr]] = code_ptr
        if stack_ptr > 0:
            stack_ptr -= 1
            raise ValueError(f'unmatched "[" at position {stack[stack_ptr]}')
        data = bytearray(self._size)
        data_ptr = 0
        code_ptr = 0
        while code_ptr < len(code):
            match code[code_ptr]:
                case '+':
                    data[data_ptr] += 1
                case '-':
                    data[data_ptr] -= 1
                case '<':
                    data_ptr -= 1
                case '>':
                    data_ptr += 1
                case ',':
                    c = self.input.read(1)
                    data[data_ptr] = ord(c)
                case '.':
                    print(chr(data[data_ptr]), end="", file=self.output)
                case '[':
                    if data[data_ptr] == 0:
                        code_ptr = targets[code_ptr]
                case ']':
                    if data[data_ptr] != 0:
                        code_ptr = targets[code_ptr]
            code_ptr += 1
