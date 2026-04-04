import socket
import struct
from pixelOutputStream import PixelOutputStream
from dataclasses import dataclass
from pixel import Pixel

def main():
    pixels = [
        Pixel(1, 1, 0xCCBBBB),
        Pixel(0, 1, 0x0000FF)
    ]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5000))

        os = s.makefile('wb')
        
        pos: PixelOutputStream = PixelOutputStream(pixels, len(pixels), os)
        
        pos.writePixels()
            

if __name__ == "__main__":
    main()