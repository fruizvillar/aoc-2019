import math
from enum import Enum

from intcode_computer import Computer
from lib import Coord

N = 11


class Colour(Enum):
    Black = 0, '.'
    White = 1, '#'

    def __init__(self, n, c):
        self.n = n
        self.c = c

    @classmethod
    def infer_color(cls, n):
        inferred = [k for k, v in cls.__members__.items() if v.n == n][0]
        return cls[inferred]


class Rotation(Enum):
    Left = 0
    Right = 1


class Orientation(Enum):
    Up = Coord(0, 1)
    Down = Coord(0, -1)
    Right = Coord(1, 0)
    Left = Coord(-1, 0)


class Canvas:
    RobotOrientation = {Orientation.Right: '>', Orientation.Up: '^', Orientation.Left: '<', Orientation.Down: 'v'}

    CellSep = ''
    RowSep = '\n'
    Margin = 0
    SpanX = 75
    SpanY = 75

    PaintedCoords = {Coord(0, 0): Colour.Black}

    def get_repr_fixed(self):
        return self._get_repr_with_lims(- self.SpanX, self.SpanX, -self.SpanY, self.SpanY)

    def get_repr_margins(self):
        x0 = min(c.x for c in self.PaintedCoords.keys()) - self.Margin
        xf = max(c.x for c in self.PaintedCoords.keys()) + self.Margin
        y0 = min(c.y for c in self.PaintedCoords.keys()) - self.Margin
        yf = max(c.y for c in self.PaintedCoords.keys()) + self.Margin
        return self._get_repr_with_lims(x0, xf, y0, yf)

    def _get_repr_with_lims(self, x_0, x_f, y_0, y_f):
        rows = []
        for y in range(y_0, y_f + 1):
            row = []
            for x in range(x_0, x_f + 1):
                c = Coord(x, y)
                if c in self.Robots:
                    row.append(self.RobotOrientation[self.Robots[c]])
                elif c in self.PaintedCoords:
                    row.append(self.PaintedCoords[c].c)
                else:
                    row.append(Colour.Black.c)
            rows.append(self.CellSep.join(row))
        return self.RowSep.join(reversed(rows))

    def paint(self, coord, color):
        self.PaintedCoords[coord] = color

    def update_robot_pos(self, pos, orientation):
        self.Robots = {pos: orientation}

    def __repr__(self):
        return self.get_repr_margins()


class Robot:
    Orientations = [Orientation.Up, Orientation.Right, Orientation.Down, Orientation.Left]

    def __init__(self, canvas: Canvas, computer: Computer):
        self.canvas = canvas
        self.computer = computer
        self.pos = Coord(0, 0)
        self.orientation = Orientation.Up
        self.update_canvas_pos()

    def scan(self):
        return self.canvas.PaintedCoords.get(self.pos, Colour.Black)

    def execute(self):
        scanned_colour = self.scan()
        print(f'Scanned colour: {scanned_colour}')
        self.computer.input.append(scanned_colour.n)
        self.computer.run()
        received_colour = Colour.infer_color(self.computer.output.pop(0))
        received_rotation = Rotation(self.computer.output.pop(0))

        print(f'Obtained from program: {received_colour}, {received_rotation}')
        self.paint(received_colour)
        self.move(received_rotation)

    def paint(self, color):
        print(f'Painting {self.pos} into: {color}')
        self.canvas.paint(self.pos, color)
        pass

    def move(self, rotation):
        self.rotate(rotation)
        self.step_forward()
        self.update_canvas_pos()

    def update_canvas_pos(self):
        self.canvas.update_robot_pos(self.pos, self.orientation)

    def __repr__(self):
        return f'Robot is in {self.pos} and oriented to {self.orientation}'

    def rotate(self, rotation):
        current_index = self.Orientations.index(self.orientation)

        new_index = (current_index + 1 if rotation == Rotation.Right else current_index - 1) % len(self.Orientations)
        new_orientation = self.Orientations[new_index]

        self.orientation = new_orientation
        print(f'Robot reoriented to {new_orientation} (turned {rotation})')

    def step_forward(self):
        self.pos = self.pos + self.orientation.value
        print(f'Robot stepped to {self.pos}.')

    def print_canvas(self):
        print(self.canvas)


def get_array(test=False):
    if test:
        return [3, 31, 4, 7, 4, 8, 99, 0, 1]

    return [3, 8, 1005, 8, 311, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108,
            0, 8, 10, 4, 10, 1002, 8, 1, 28, 1006, 0, 2, 2, 109, 10, 10, 1, 1, 19, 10, 1, 1103, 20, 10, 3, 8, 102, -1,
            8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1002, 8, 1, 65, 1006, 0, 33, 1, 7, 0, 10, 3, 8, 102,
            -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1002, 8, 1, 94, 3, 8, 102, -1, 8, 10, 1001, 10, 1,
            10, 4, 10, 108, 1, 8, 10, 4, 10, 101, 0, 8, 116, 1, 1002, 1, 10, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4,
            10, 108, 0, 8, 10, 4, 10, 1002, 8, 1, 142, 2, 1101, 6, 10, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10,
            108, 0, 8, 10, 4, 10, 1001, 8, 0, 168, 2, 1107, 7, 10, 1006, 0, 68, 1, 5, 6, 10, 1, 2, 5, 10, 3, 8, 1002, 8,
            -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 1002, 8, 1, 206, 1, 1008, 16, 10, 3, 8, 102, -1, 8,
            10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1001, 8, 0, 232, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4,
            10, 108, 1, 8, 10, 4, 10, 102, 1, 8, 253, 1006, 0, 30, 2, 1, 4, 10, 1, 1008, 1, 10, 2, 1109, 4, 10, 3, 8,
            102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 102, 1, 8, 291, 101, 1, 9, 9, 1007, 9, 1051,
            10, 1005, 10, 15, 99, 109, 633, 104, 0, 104, 1, 21102, 387508339604, 1, 1, 21102, 1, 328, 0, 1106, 0, 432,
            21101, 0, 47677022988, 1, 21101, 0, 339, 0, 1106, 0, 432, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3,
            10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 21102,
            209382822080, 1, 1, 21102, 386, 1, 0, 1105, 1, 432, 21101, 179318123523, 0, 1, 21102, 1, 397, 0, 1105, 1,
            432, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21102, 709584904960, 1, 1, 21101, 420, 0, 0, 1106, 0,
            432, 21102, 709580444008, 1, 1, 21102, 431, 1, 0, 1105, 1, 432, 99, 109, 2, 21202, -1, 1, 1, 21102, 1, 40,
            2, 21101, 0, 463, 3, 21101, 0, 453, 0, 1105, 1, 496, 109, -2, 2105, 1, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204,
            -1, 1001, 458, 459, 474, 4, 0, 1001, 458, 1, 458, 108, 4, 458, 10, 1006, 10, 490, 1101, 0, 0, 458, 109, -2,
            2106, 0, 0, 0, 109, 4, 2102, 1, -1, 495, 1207, -3, 0, 10, 1006, 10, 513, 21102, 1, 0, -3, 21202, -3, 1, 1,
            22102, 1, -2, 2, 21102, 1, 1, 3, 21102, 532, 1, 0, 1106, 0, 537, 109, -4, 2105, 1, 0, 109, 5, 1207, -3, 1,
            10, 1006, 10, 560, 2207, -4, -2, 10, 1006, 10, 560, 21201, -4, 0, -4, 1106, 0, 628, 22101, 0, -4, 1, 21201,
            -3, -1, 2, 21202, -2, 2, 3, 21101, 579, 0, 0, 1105, 1, 537, 21201, 1, 0, -4, 21101, 1, 0, -1, 2207, -4, -2,
            10, 1006, 10, 598, 21102, 0, 1, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 620, 21201, -1, 0, 1,
            21101, 0, 620, 0, 106, 0, 495, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2105, 1, 0]


def main():
    array = get_array()
    robot = Robot(Canvas(), Computer(array))

    robot.canvas.PaintedCoords[Coord(0, 0)] = Colour.White

    while not robot.computer.halted:
        robot.execute()
    robot.print_canvas()

    colours = robot.canvas.PaintedCoords
    print(len(colours), colours)


if __name__ == '__main__':
    main()
