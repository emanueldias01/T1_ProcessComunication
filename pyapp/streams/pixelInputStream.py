from entitys.pixel import Pixel

class PixelInputStream:
    def __init__(self, inputStream):
        self.inputStream = inputStream

    def read(self):
        return self.inputStream.read()

    def readPixels(self):
        self.quantidade = self.readInt()

        pixels = []

        for _ in range(self.quantidade):
            x = self.readInt()
            y = self.readInt()
            color = self.readInt()

            pixels.append(Pixel(x, y, color))


        return pixels

    def readInt(self):
        integer_b = self.inputStream.read(4)
        integer = int.from_bytes(integer_b, byteorder='big')
        return integer
