import math
import random
import time
from enum import Enum

from intcode_computer import Computer
from lib import Coord

N = 15

PART_1 = False


class AllDiscoveredError(Exception):
    pass


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    @classmethod
    def from_coord(cls, coord):
        directions = [d for d, c in cls.MapToCoords.items() if c == coord]
        if directions:
            return directions[0]


dir_to_coord = {Direction.NORTH: Coord(0, 1), Direction.SOUTH: Coord(0, -1),
                 Direction.EAST: Coord(1, 0), Direction.WEST: Coord(-1, 0)}


def get_coord_from_dir(direction: Direction):
    return dir_to_coord[direction]


def get_dir_from_coord(coord: Coord):
    return [d for d, c in dir_to_coord.items() if c == coord][0]


class Status(Enum):
    WALL_HIT = 0
    MOVE_OK = 1
    OXYGEN = 2


class Canvas:
    CellSep = ''
    RowSep = '\n'
    Margin = 0
    SpanX = 20
    SpanY = 20

    RobotPos = Coord(0, 0)

    ExploredCoords = {Coord(0, 0): Status.MOVE_OK}

    def get_repr_fixed(self):
        return self._get_repr_with_lims(- self.SpanX, self.SpanX, -self.SpanY, self.SpanY)

    def get_repr_margins(self):
        x0 = min(c.x for c in self.ExploredCoords.keys()) - self.Margin
        xf = max(c.x for c in self.ExploredCoords.keys()) + self.Margin
        y0 = min(c.y for c in self.ExploredCoords.keys()) - self.Margin
        yf = max(c.y for c in self.ExploredCoords.keys()) + self.Margin
        return self._get_repr_with_lims(x0, xf, y0, yf)

    def _get_repr_with_lims(self, x_0, x_f, y_0, y_f):
        rows = []
        for y in range(y_0, y_f + 1):
            row = []
            for x in range(x_0, x_f + 1):
                c = Coord(x, y)
                if c in self.ExploredCoords:
                    status = self.ExploredCoords[c]
                    if c == self.RobotPos:
                        char = 'X'
                    elif status == Status.WALL_HIT:
                        char = '█'
                    elif status == Status.OXYGEN:
                        char = 'O'
                    else:
                        char = '.'
                    row.append(char)
                else:
                    row.append('░')
            rows.append(self.CellSep.join(row))
        return self.RowSep.join(reversed(rows))

    def __repr__(self):
        return self.get_repr_margins()


class Robot:

    def __init__(self, canvas: Canvas, computer: Computer):
        self.canvas = canvas
        self.computer = computer
        self.location = Coord(0, 0)
        self.visited = [self.location]

    def execute(self, direction):
        self.computer.input.append(direction.value)
        self.computer.run()
        result = Status(self.computer.output.pop(0))

        new_location = self.location + get_coord_from_dir(direction)

        self.canvas.ExploredCoords[new_location] = result

        if result != Status.WALL_HIT:
            self.location = new_location
            self.visited.append(new_location)
            self.canvas.RobotPos = new_location
        return result

    def step_back(self):
        try:
            current_location = self.visited.pop()
            previous_location = self.visited[-1]
        except IndexError:
            raise AllDiscoveredError

        direction = get_dir_from_coord(previous_location - current_location)

        # print(f'Stepping back from {current_location} to {previous_location} ({direction})')

        self.computer.input.append(direction.value)
        self.computer.run()
        result = Status(self.computer.output.pop(0))

        if result is not Status.MOVE_OK:
            raise ValueError(f'Stepping back did not work (from {current_location} to {previous_location})')

        self.canvas.RobotPos = previous_location
        self.location = previous_location
        return result

    def find_wise(self):
        for direction in [Direction(1 + i) for i in range(4)]:
            new_pos = self.location + get_coord_from_dir(direction)
            if new_pos not in self.canvas.ExploredCoords:
                break
        else:  # Here when all dirs have already been explored. Stepping back
            return self.step_back()

        result = self.execute(direction)
        # print(result)
        print(len(self.canvas.ExploredCoords))
        return result

    def __repr__(self):
        return self.canvas.__repr__()

    def expand_oxygen(self):
        delta_t = 0

        new_values = [k for k, v in self.canvas.ExploredCoords.items() if v == Status.OXYGEN]  # 1st iter

        while new_values:
            delta_t += 1
            iter_values = new_values
            new_values = []
            for v in iter_values:
                for i in range(1, 5):
                    c_iter = v + get_coord_from_dir(Direction(i))
                    try:
                        if self.canvas.ExploredCoords[c_iter] == Status.MOVE_OK:
                            self.canvas.ExploredCoords[c_iter] = Status.OXYGEN
                            new_values.append(c_iter)
                    except KeyError:
                        continue
        return delta_t - 1  # last iteration will not fill any coordinate.


def get_array(test=False):
    if test:
        return [3, 31, 4, 7, 4, 8, 99, 0, 1]

    return [3, 1033, 1008, 1033, 1, 1032, 1005, 1032, 31, 1008, 1033, 2, 1032, 1005, 1032, 58, 1008, 1033, 3, 1032,
            1005, 1032, 81, 1008, 1033, 4, 1032, 1005, 1032, 104, 99, 1001, 1034, 0, 1039, 1001, 1036, 0, 1041, 1001,
            1035, -1, 1040, 1008, 1038, 0, 1043, 102, -1, 1043, 1032, 1, 1037, 1032, 1042, 1105, 1, 124, 102, 1, 1034,
            1039, 1001, 1036, 0, 1041, 1001, 1035, 1, 1040, 1008, 1038, 0, 1043, 1, 1037, 1038, 1042, 1106, 0, 124,
            1001, 1034, -1, 1039, 1008, 1036, 0, 1041, 1001, 1035, 0, 1040, 101, 0, 1038, 1043, 101, 0, 1037, 1042,
            1106, 0, 124, 1001, 1034, 1, 1039, 1008, 1036, 0, 1041, 1002, 1035, 1, 1040, 102, 1, 1038, 1043, 1001, 1037,
            0, 1042, 1006, 1039, 217, 1006, 1040, 217, 1008, 1039, 40, 1032, 1005, 1032, 217, 1008, 1040, 40, 1032,
            1005, 1032, 217, 1008, 1039, 37, 1032, 1006, 1032, 165, 1008, 1040, 5, 1032, 1006, 1032, 165, 1102, 1, 2,
            1044, 1105, 1, 224, 2, 1041, 1043, 1032, 1006, 1032, 179, 1102, 1, 1, 1044, 1106, 0, 224, 1, 1041, 1043,
            1032, 1006, 1032, 217, 1, 1042, 1043, 1032, 1001, 1032, -1, 1032, 1002, 1032, 39, 1032, 1, 1032, 1039, 1032,
            101, -1, 1032, 1032, 101, 252, 1032, 211, 1007, 0, 64, 1044, 1106, 0, 224, 1101, 0, 0, 1044, 1105, 1, 224,
            1006, 1044, 247, 1002, 1039, 1, 1034, 101, 0, 1040, 1035, 102, 1, 1041, 1036, 102, 1, 1043, 1038, 101, 0,
            1042, 1037, 4, 1044, 1106, 0, 0, 13, 40, 97, 1, 18, 1, 79, 93, 56, 16, 38, 41, 78, 11, 78, 25, 46, 84, 31,
            38, 76, 17, 96, 5, 78, 50, 8, 67, 77, 54, 42, 82, 39, 2, 8, 5, 11, 85, 37, 93, 37, 7, 97, 12, 94, 2, 44, 70,
            74, 78, 34, 45, 94, 75, 19, 8, 84, 72, 2, 9, 69, 74, 6, 11, 75, 79, 42, 35, 86, 83, 23, 82, 88, 40, 81, 70,
            8, 58, 46, 57, 77, 65, 76, 68, 79, 61, 24, 80, 61, 88, 70, 42, 32, 71, 16, 23, 99, 77, 73, 57, 45, 99, 39,
            29, 97, 4, 90, 76, 3, 5, 86, 11, 95, 94, 90, 59, 13, 37, 94, 29, 57, 42, 99, 4, 45, 96, 22, 74, 33, 73, 70,
            24, 96, 4, 82, 10, 3, 79, 37, 81, 97, 72, 42, 66, 3, 27, 98, 4, 73, 49, 55, 86, 12, 41, 65, 38, 21, 66, 27,
            80, 87, 53, 86, 26, 85, 80, 42, 26, 92, 17, 79, 76, 58, 69, 2, 71, 7, 88, 12, 61, 73, 16, 67, 48, 83, 87, 8,
            21, 72, 67, 50, 70, 7, 71, 9, 53, 46, 81, 99, 47, 3, 70, 11, 23, 68, 22, 86, 43, 32, 92, 30, 78, 94, 61, 81,
            32, 60, 89, 97, 58, 23, 27, 52, 99, 85, 90, 41, 20, 11, 87, 73, 57, 83, 30, 79, 2, 58, 93, 32, 81, 16, 86,
            35, 87, 38, 73, 88, 11, 6, 65, 32, 20, 81, 87, 89, 12, 11, 66, 42, 84, 12, 79, 14, 23, 72, 37, 85, 95, 15,
            48, 80, 92, 59, 56, 7, 95, 85, 21, 82, 53, 93, 45, 73, 29, 79, 6, 17, 68, 79, 34, 72, 47, 39, 81, 93, 63,
            83, 51, 67, 99, 1, 74, 56, 89, 47, 86, 95, 51, 94, 46, 3, 95, 18, 81, 20, 85, 19, 90, 60, 24, 65, 65, 46,
            91, 17, 82, 37, 87, 21, 83, 80, 22, 28, 75, 17, 68, 72, 40, 67, 82, 19, 9, 79, 42, 86, 55, 93, 91, 41, 76,
            55, 22, 74, 61, 91, 42, 96, 73, 11, 1, 79, 60, 85, 82, 40, 76, 88, 84, 2, 14, 97, 89, 29, 69, 39, 43, 65,
            19, 58, 97, 68, 45, 50, 2, 91, 54, 52, 93, 82, 61, 76, 22, 15, 77, 63, 76, 60, 81, 42, 89, 77, 45, 80, 3,
            92, 17, 10, 98, 16, 92, 38, 71, 2, 46, 81, 81, 11, 7, 43, 82, 68, 82, 93, 25, 44, 87, 60, 49, 48, 7, 47, 82,
            82, 26, 65, 93, 50, 75, 57, 92, 57, 78, 11, 39, 99, 2, 93, 42, 69, 6, 66, 60, 96, 79, 50, 20, 75, 84, 48,
            98, 57, 5, 93, 98, 62, 78, 85, 53, 85, 32, 37, 90, 90, 30, 43, 74, 57, 81, 19, 35, 19, 94, 50, 65, 60, 98,
            65, 46, 86, 75, 68, 16, 31, 83, 75, 56, 93, 35, 42, 89, 32, 69, 35, 2, 60, 82, 58, 53, 1, 87, 18, 66, 82,
            41, 73, 73, 7, 99, 91, 89, 48, 83, 20, 81, 31, 66, 17, 93, 23, 41, 86, 65, 57, 72, 13, 13, 82, 94, 79, 77,
            54, 89, 90, 62, 95, 35, 74, 82, 37, 43, 33, 66, 77, 3, 86, 26, 87, 35, 69, 19, 24, 85, 62, 18, 9, 72, 42,
            69, 25, 95, 57, 34, 41, 82, 36, 90, 24, 36, 27, 67, 49, 30, 70, 75, 82, 44, 33, 67, 70, 35, 36, 69, 33, 85,
            10, 87, 50, 72, 8, 74, 97, 18, 95, 25, 97, 5, 84, 16, 65, 60, 89, 15, 86, 81, 9, 75, 73, 58, 72, 39, 91, 10,
            55, 3, 11, 86, 96, 18, 98, 97, 28, 22, 98, 49, 89, 19, 84, 18, 98, 34, 92, 67, 37, 80, 17, 8, 65, 72, 2, 91,
            95, 55, 76, 19, 30, 78, 40, 96, 78, 34, 91, 99, 23, 14, 71, 38, 37, 71, 59, 93, 78, 83, 61, 24, 31, 97, 25,
            85, 8, 16, 84, 15, 65, 77, 14, 96, 98, 6, 89, 33, 98, 59, 4, 84, 66, 18, 74, 48, 12, 41, 86, 31, 45, 33, 74,
            97, 86, 55, 85, 16, 34, 54, 91, 77, 3, 19, 65, 70, 18, 90, 41, 98, 25, 55, 22, 95, 15, 92, 14, 67, 20, 88,
            5, 51, 69, 92, 33, 69, 75, 56, 36, 91, 3, 80, 13, 78, 36, 88, 50, 88, 79, 65, 24, 66, 5, 99, 45, 98, 88, 66,
            30, 92, 98, 84, 5, 90, 13, 67, 95, 96, 33, 77, 30, 80, 39, 99, 81, 95, 55, 86, 0, 0, 21, 21, 1, 10, 1, 0, 0,
            0, 0, 0, 0]


def main():
    array = get_array()
    robot = Robot(Canvas(), Computer(array))

    try:
        while not robot.computer.halted:
            result = robot.find_wise()
            # print(robot)
            if result == Status.OXYGEN and PART_1:
                break

        print(len(robot.visited), robot.visited[0])
    except AllDiscoveredError:
        print(robot)

    t_o2 = robot.expand_oxygen()
    print(robot)
    print(f'Took {t_o2} minutes to fill the tank')


if __name__ == '__main__':
    main()
