from io import TextIOWrapper
from sys import stdin, stdout

XLAT_1 = '+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z\';FNQuY]szf$!BS/|t:Pn6^Ha'
XLAT_2 = '5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK\'X~xDl}REokN:#?G\"i@'
MEM_SIZE = 3**10
OPERATIONS = "ji*p</vo"
P9 = [1, 9, 81, 729, 6561]
O = [
    [4, 3, 3, 1, 0, 0, 1, 0, 0],
    [4, 3, 5, 1, 0, 2, 1, 0, 2],
    [5, 5, 4, 2, 2, 1, 2, 2, 1],
    [4, 3, 3, 1, 0, 0, 7, 6, 6],
    [4, 3, 5, 1, 0, 2, 7, 6, 8],
    [5, 5, 4, 2, 2, 1, 8, 8, 7],
    [7, 6, 6, 7, 6, 6, 4, 3, 3],
    [7, 6, 8, 7, 6, 8, 4, 3, 5],
    [8, 8, 7, 8, 8, 7, 5, 5, 4],
]


class Interpreter:
    """Malbolge interpreter."""

    def __init__(self, input: TextIOWrapper = stdin, output: TextIOWrapper = stdout):
        super().__init__()
        self.input = input
        self.output = output

    def run(self, input: str | TextIOWrapper):
        """Runs the specified code.

        :param input: The Malbolge code to run.
        :type input: str | TextIOWrapper
        :raises ValueError: If the code is not valid Malbolge.
        """
        if isinstance(input, str):
            code = input
        else:
            code = input.read()
        mem = [0 for _ in range(MEM_SIZE)]
        mem_ptr = 0
        for c in code:
            x = ord(c)
            if x < 32:
                continue
            if 32 < x < 127:
                operation = XLAT_1[(x - 33 + mem_ptr) % 94]
                if operation not in OPERATIONS:
                    raise ValueError(f'invalid operation "{c}"/"{operation}" at position {mem_ptr}')
            if mem_ptr == MEM_SIZE:
                raise ValueError('code too large')
            mem[mem_ptr] = x
            mem_ptr += 1
        while mem_ptr < MEM_SIZE:
            mem[mem_ptr] = self.crazy(mem[mem_ptr - 1], mem[mem_ptr - 2])
            mem_ptr += 1
        self.exec(mem)

    def exec(self, mem: list[int]):
        """Executes the code in the specified memory.

        :param mem: The memory containing the code and data.
        :type mem: list[int]
        """
        a = 0
        c = 0
        d = 0
        while True:
            if 32 < mem[c] < 127:
                operation = XLAT_1[(mem[c] - 33 + c) % 94]
                match operation:
                    case 'j':
                        d = mem[d]
                    case 'i':
                        c = mem[d]
                    case '*':
                        a = int(mem[d] / 3) + mem[d] % 3 * 19683
                        mem[d] = a
                    case 'p':
                        a = self.crazy(a, mem[d])
                        mem[d] = a
                    case '<':
                        print(chr(a & 0xFF), end="", file=self.output)
                    case '/':
                        c = self.input.read(1)
                        if len(c) == 0:
                            a = MEM_SIZE
                        else:
                            a = ord(c)
                    case 'v':
                        return
                mem[c] = ord(XLAT_2[mem[c] - 33])
            c = (c + 1) % MEM_SIZE
            d = (d + 1) % MEM_SIZE

    def crazy(self, input_1: int, input_2: int) -> int:
        """Performs the Malbolge `crazy` operation.

        :param input_1: The first input.
        :type input_1: int
        :param input_2: The second input.
        :type input_2: int
        :return: The Output of the `crazy` operation.
        :rtype: int
        """
        output = 0
        for i in range(len(P9)):
            output += O[int(input_2 / P9[i]) % 9][int(input_1 / P9[i]) % 9] * P9[i]
        return output
