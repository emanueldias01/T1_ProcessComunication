from entitys.pixel import Pixel
from entitys.board import Board


class BoardInputStream:
    def __init__(self, inputStream):
        self.inputStream = inputStream

    def read(self):
        return self.inputStream.read()

    def readBoard(self):
        width = self.readInt()
        height = self.readInt()

        grid = []

        for y in range(height):
            grid.append([])
            for _ in range(width):
                grid[y].append(self.readInt())

        return Board(grid, width, height)

    def readInt(self):
        integer_b = self.inputStream.read(4)
        integer = int.from_bytes(integer_b, byteorder='big')
        return integer

