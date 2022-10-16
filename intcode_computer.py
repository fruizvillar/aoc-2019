class HaltException(Exception):
    pass


class EmptyInputException(Exception):
    def __init__(self):
        pass  # print('Empty input... Awaiting')


class Computer:
    def __init__(self, array: list):
        self.mem = {}

        for i, v in enumerate(array):
            self.mem[i] = Register(v)

        self.instruction_pointer = 0

        self.input = []

        self.output = []

        self.status = 'WAIT'

        self.halted = False

        self.instructions = {i.n: i for i in [SumInstruction(), MultiplyInstruction(),
                             InputInstruction(self.input), OutputInstruction(self.output),
                             JumpIfTrueInstruction(), JumpIfFalseInstruction(),
                             LessThanInstruction(),  EqualInstruction(),
                             BaseAdjustmentInstruction(),
                             HaltInstruction()]}

    def run(self):
        self.status = 'RUNNING'
        try:
            while True:
                #print_instruction(mem, instruction_pointer)
                self.instruction_pointer = self.instruction_call()
                # print(mem)

        except HaltException:
            self.status = 'HALTED'
            self.halted = True
        except EmptyInputException:
            self.status = 'WAIT'

        return self.mem

    def instruction_call(self):
        n = self.mem[self.instruction_pointer].n % 100
        return self.instructions[n].subcall(self.mem, self.instruction_pointer)


class Register:
    def __init__(self, n):
        super().__init__()
        self.n = int(n)

    def __int__(self):
        return self.n

    def __repr__(self):
        return f'<{self.n}>'


class Instruction:

    RelativeBase = 0

    def __init__(self, n, instruction_length):
        self.n = n
        self.instruction_length = instruction_length


    def get_reference_type(self, opx):
        access, opcode = divmod(opx.n, 100)
        im3_im2, im1 = divmod(access, 10)
        im3, im2, = divmod(im3_im2, 10)
        self.check_op(opcode)
        return im1, im2, im3

    def check_op(self, op):
        if op != self.n:
            raise RuntimeError(f'{self.__class__.__name__} is {self.n}')

    def __call__(self, mem, pos):
        opx = mem[pos]
        params = [mem[pos + i] for i in range(1, self.instruction_length)]
        modes = self.get_reference_type(opx)[:len(params)]

        for i, mode in enumerate(modes):
            if mode != 1:
                index = params[i].n + self.RelativeBase if mode == 2 else params[i].n
                try:
                    params[i] = mem[index]
                except KeyError:
                    mem[index] = Register(0)
                    params[i] = mem[index]
        # print(f'{pos:3d}|Call {self.__class__.__name__}({opx}) with params {params} (modes={modes})')

        ret = self.oper(params)
        return ret if ret is not None else self.std_return(pos)

    def std_return(self, pos):
        return pos + self.instruction_length

    def oper(self, params):
        raise NotImplementedError("Inherit from this class to properly use it")

    def instruction_length_n(self, register):
        n = register.n
        return self.instructions[n % 100].instruction_length

    def subcall(self, mem, pos=0):
        return self(mem, pos)

    def get_with_mode(self, array, val, mod):
        if mod == 1:
            return val

        index = val + self.RelativeBase if mod == 2 else val
        return array[index]


class SumInstruction(Instruction):
    def __init__(self):
        super().__init__(n=1, instruction_length=4)

    def oper(self, params):
        s1, s2, dest = params

        dest.n = int(s1) + int(s2)


class MultiplyInstruction(Instruction):
    def __init__(self):
        super().__init__(n=2, instruction_length=4)

    def oper(self, params):
        s1, s2, dest = params
        dest.n = int(s1) * int(s2)


class InputInstruction(Instruction):
    def __init__(self, input):
        super().__init__(n=3, instruction_length=2)

        self.input = input

    def oper(self, params):
        res, = params
        try:
            res.n = int(self.input.pop(0))
        except IndexError:
            raise EmptyInputException


class OutputInstruction(Instruction):
    def __init__(self, output):
        super().__init__(n=4, instruction_length=2)

        self.output = output

    def oper(self, params):
        v, = params

        self.output.append(int(v))


class JumpIfTrueInstruction(Instruction):
    def __init__(self):
        super().__init__(n=5, instruction_length=3)

    def oper(self, params):
        v, pointer = params

        if int(v):
            return int(pointer)


class JumpIfFalseInstruction(Instruction):
    def __init__(self):
        super().__init__(n=6, instruction_length=3)

    def oper(self, params):
        v, pointer = params

        if not int(v):
            return int(pointer)


class LessThanInstruction(Instruction):
    def __init__(self):
        super().__init__(n=7, instruction_length=4)

    def oper(self, params):
        param1, param2, res = params

        res.n = int(int(param1) < int(param2))


class EqualInstruction(Instruction):
    def __init__(self):
        super().__init__(n=8, instruction_length=4)

    def oper(self, params):
        p1, p2, res = params

        res.n = int(int(p1) == int(p2))


class BaseAdjustmentInstruction(Instruction):
    def __init__(self):
        super().__init__(n=9, instruction_length=2)

    def oper(self, params):
        param1, = params
        #print(f'Adjusting relative base from {Instruction.RelativeBase} to {Instruction.RelativeBase + int(param1)} '
        #       f'({param1})')
        Instruction.RelativeBase += int(param1)


class HaltInstruction(Instruction):
    def __init__(self):
        super().__init__(n=99, instruction_length=1)

    def oper(self, params):
        raise HaltException
