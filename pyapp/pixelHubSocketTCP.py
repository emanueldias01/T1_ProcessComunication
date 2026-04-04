import socket
import struct
from pixelOutputStream import PixelOutputStream
from dataclasses import dataclass
from pixel import Pixel

class PixelHubSocketTCP():
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 5000))
        self.os = self.s.makefile('wb')        
    
    def send_pixels(self, pixels):
        pos: PixelOutputStream = PixelOutputStream(pixels, len(pixels), self.os)
        pos.writePixels()
    
    def disconnect(self):
        self.s.close()
