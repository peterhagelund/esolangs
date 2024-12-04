from enum import Enum
from io import TextIOWrapper
from random import randint, seed
from sys import stdin, stdout


class Stack:
    """Befunge stack."""

    def __init__(self):
        super().__init__()
        self.values: list[int] = []

    def push(self, value: int):
        """Pushes the specified value onto the stack.

        :param value: The value.
        :type value: int
        """
        self.values.append(value)

    def pop(self) -> int:
        """Pops the topmost value off the stack.

        **Please note**: If the stack is empty, the value `0` is returned.

        :return: The topmost value.
        :rtype: int
        """
        if len(self.values) > 0:
            return self.values.pop()
        else:
            return 0

    def dup(self):
        """Duplicates the topmost value."""
        if len(self.values) > 0:
            self.values.append(self.values[-1])

    def swap(self):
        """Swaps the two topmost values."""
        if len(self.values) > 1:
            self.values[-1], self.values[-2] = self.values[-2], self.values[-1]


class Direction(Enum):
    """Direction of the Befunge code flow."""

    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Interpreter:
    """Befunge interpreter.

    :param input: The input stream (`stdin` by default).
    :type input: IOBase
    :param input: The output stream (`stdout` by default).
    :type input: IOBase
    """

    def __init__(self, input: TextIOWrapper = stdin, output: TextIOWrapper = stdout):
        super().__init__()
        self.input = input
        self.output = output

    def run(self, input: str | TextIOWrapper):
        """Runs the specified code.

        :param input: The Befunge code to run.
        :type input: str | IOBase
        :raises ValueError: If the code is not valid Befunge.
        """
        if isinstance(input, str):
            code = input
        else:
            code = input.read()
        lines = code.splitlines()
        width = max(*[len(line) for line in lines])
        if width > 80:
            raise ValueError("code is too wide")
        height = len(lines)
        if height > 25:
            raise ValueError("code is too tall")
        if width == 0 or height == 0:
            raise ValueError("code is empty")
        grid = [bytearray([32 for _ in range(width)]) for _ in lines]
        y = 0
        for line in lines:
            x = 0
            for c in line:
                grid[y][x] = ord(c)
                x += 1
            y += 1
        self.exec(grid)

    def exec(self, grid: list[bytearray]):
        """Executes the code in the specified grid.

        :param grid: The code grid.
        :type grid: list[bytearray]
        """
        seed()
        stack = Stack()
        y = 0
        x = 0
        direction = Direction.RIGHT
        step = 1
        string_mode = False
        while True:
            instruction = chr(grid[y][x])
            if instruction == '"':
                string_mode = not string_mode
            else:
                if string_mode:
                    stack.push(int(ord(instruction)))
                else:
                    match instruction:
                        case digit if instruction in "01234567890":
                            value = int(digit)
                            stack.push(value)
                        case "+":
                            a = stack.pop()
                            b = stack.pop()
                            stack.push(a + b)
                        case "-":
                            a = stack.pop()
                            b = stack.pop()
                            stack.push(b - a)
                        case "*":
                            a = stack.pop()
                            b = stack.pop()
                            stack.push(a * b)
                        case "/":
                            a = stack.pop()
                            b = stack.pop()
                            stack.push(int(b / a))
                        case "%":
                            a = stack.pop()
                            b = stack.pop()
                            stack.push(b % a)
                        case "!":
                            value = stack.pop()
                            if value == 0:
                                stack.push(1)
                            else:
                                stack.push(0)
                        case "`":
                            a = stack.pop()
                            b = stack.pop()
                            if b > a:
                                stack.push(1)
                            else:
                                stack.push(0)
                        case ">":
                            direction = Direction.RIGHT
                        case "<":
                            direction = Direction.LEFT
                        case "^":
                            direction = Direction.UP
                        case "v":
                            direction = Direction.DOWN
                        case "?":
                            d = randint(0, 3)
                            match d:
                                case 0:
                                    direction = Direction.RIGHT
                                case 1:
                                    direction = Direction.LEFT
                                case 2:
                                    direction = Direction.UP
                                case 3:
                                    direction = Direction.DOWN
                        case "_":
                            value = stack.pop()
                            if value == 0:
                                direction = Direction.RIGHT
                            else:
                                direction = Direction.LEFT
                        case "|":
                            value = stack.pop()
                            if value == 0:
                                direction = Direction.DOWN
                            else:
                                direction = Direction.UP
                        case ":":
                            stack.dup()
                        case "\\":
                            stack.swap()
                        case "$":
                            stack.pop()
                        case ".":
                            value = stack.pop()
                            print(f"{value}", end=" ", file=self.output)
                        case ",":
                            value = stack.pop()
                            print(chr(value), end="", file=self.output)
                        case "#":
                            step = 2
                        case "p":
                            y = stack.pop()
                            x = stack.pop()
                            value = stack.pop()
                            grid[y][x] = value & 0xFF
                        case "g":
                            y = stack.pop()
                            x = stack.pop()
                            stack.push(int(grid[y][x]))
                        case "&":
                            number: int = None
                            while number is None:
                                print("enter a number:", end=" ", file=self.output)
                                s = str(self.input.readline()).strip()
                                try:
                                    number = int(s)
                                except:
                                    print(f"'{s}' is not a valid number", file=self.output)
                            stack.push(number)
                        case "~":
                            value: int = None
                            while value is None:
                                print("enter a single character:", end=" ", file=self.output)
                                s = str(self.input.readline()).strip()
                                if len(s) == 1:
                                    value = ord(s)
                                else:
                                    print(f"'{s}' is not a single character", file=self.output)
                            stack.push(value)
                        case "@":
                            return
            match direction:
                case Direction.RIGHT:
                    x += step
                    if x >= len(grid[0]):
                        x = 0
                case Direction.LEFT:
                    x -= step
                    if x < 0:
                        x = len(grid[0]) - 1
                case Direction.UP:
                    y -= step
                    if y < 0:
                        y = len(grid) - 1
                case Direction.DOWN:
                    y += step
                    if y >= len(grid):
                        y = 0
            step = 1
