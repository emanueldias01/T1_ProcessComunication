package br.com.sd.services;

import br.com.sd.entitys.Board;
import br.com.sd.entitys.Pixel;

import java.util.ArrayList;
import java.util.List;

public class BoardService {

    private Board board;

    public Board createBoard(int height, int width) {
        this.board = new Board(height, width);
        return board;
    }

    public Board getBoard() {
        return board;
    }

    public boolean setPixel(Pixel pixel) {
        if (board == null) {
            throw new IllegalStateException("Board não foi criado");
        }

        // valida se o pixel está dentro do quadro
        if (pixel.getX() < 0 || pixel.getX() >= board.getWidth() ||
                pixel.getY() < 0 || pixel.getY() >= board.getHeight()) {
            return false;
        }

        this.board.setPixel(pixel.getX(), pixel.getY(), pixel.getColor());
        return true;
    }

    public String toString() {
        if (board == null) {
            throw new IllegalStateException("Board não foi criado");
        }

        return this.board.toString();
    }
}