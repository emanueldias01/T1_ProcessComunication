import struct
from typing import BinaryIO
from entitys.pixel import Pixel

class PixelOutputStream:

    pixels: list[Pixel]
    quantidade: int
    os: BinaryIO

    def __init__(self, pixels: list[Pixel], quantidade: int, out):
        self.pixels = pixels
        self.quantidade = quantidade
        self.out = out
    

    def write(self, b: int) -> None:
        self.out.write(b)

    def writePixels(self) -> None:
        self.writeInt(self.quantidade);

        for i in range(self.quantidade):
            self.writePixel(self.pixels[i])

        self.out.flush()

    def writeInt(self, value: int) -> None:
        self.out.write(struct.pack('!I', value))
    
    def writePixel(self, pixel: Pixel) -> None:
        self.out.write(struct.pack('!III', pixel.x, pixel.y, pixel.color))

