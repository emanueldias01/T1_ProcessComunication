import socket
import struct

from streams.pixelOutputStream import PixelOutputStream
from streams.pixelInputStream import PixelInputStream
from streams.boardInputStream import BoardInputStream
from entitys.pixel import Pixel

class PixelHub():
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("10.10.241.238", 5001))
        
        self.output_stream = self.s.makefile('wb')
        self.input_stream  = self.s.makefile('rb')

        self.bis: BoardInputStream = BoardInputStream(self.input_stream)
        self.pos: PixelOutputStream = PixelInputStream(self.input_stream)
    
    def send_pixels(self, pixels):
        pos: PixelOutputStream = PixelOutputStream(pixels, len(pixels), self.output_stream)
        pos.writePixels()

    def recv_pixels(self):
        return self.pos.readPixels()

    def recv_board(self):
        return self.bis.readBoard()
    
    def disconnect(self):
        self.s.close()
