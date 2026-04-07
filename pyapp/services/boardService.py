from entitys.board import Board
from entitys.pixel import Pixel

class BoardService:
    board: Board

    def __init__(self, height: int, width: int):
        self.board = Board(height, width);
        return self.board;

    def loadBoard(self, board: Board) -> Board:
        self.board = board;
        return board;

    def getBoard(self) -> Board:
        return self.board;

    def setPixel(self, pixel: Pixel):
        if (self.board == None):
            raise AssertionError("Board não foi criado")

        if (pixel.getX() < 0 or pixel.getX() >= self.board.getWidth() or
                pixel.getY() < 0 or pixel.getY() >= self.board.getHeight()):
            return False;
        
        self.board.setPixel(pixel.getX(), pixel.getY(), pixel.getColor());
        return True;

    def toString(self):
        if (self.board == None):
            raise AssertionError("Board não foi criado");

        return self.board.toString();
    
