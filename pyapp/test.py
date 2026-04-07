import socket
import struct
from streams.pixelOutputStream import PixelOutputStream
from streams.pixelInputStream import PixelInputStream
from dataclasses import dataclass
from entitys.pixel import Pixel

def main():
    pixels = [
        Pixel(1, 1, 0xCCBBBB),
        Pixel(0, 1, 0xCC00FF)
    ]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5000))

        output_stream = s.makefile('wb')
        input_stream = s.makefile('rb')

        pos: PixelOutputStream = PixelOutputStream(pixels, len(pixels), output_stream)
        pis: PixelInputStream = PixelInputStream(input_stream)

        while (True):
            pixels_recv = pis.readPixels()
            print("Pixels recebidos:")
            for p in pixels_recv:
                print(f"{p.x}, {p.y}, {p.color}")
            

if __name__ == "__main__":
    main()