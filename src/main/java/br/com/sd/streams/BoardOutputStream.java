package br.com.sd.streams;

import br.com.sd.entitys.Board;

import java.io.IOException;
import java.io.OutputStream;

public class BoardOutputStream extends OutputStream {
    private Board board;
    private OutputStream out;

    public BoardOutputStream(Board board, OutputStream out) {
        this.board = board;
        this.out = out;
    }

    @Override
    public void write(int b) throws IOException {
        out.write(b);
    }

    public void writeBoard() throws IOException {
        writeInt(board.getWidth());
        writeInt(board.getHeight());

        int[][] grid = board.getGrid();

        for (int y = 0; y < board.getHeight(); y++) {
            for (int x = 0; x < board.getWidth(); x++) {
                writeInt(grid[y][x]);
            }
        }

        out.flush();
    }

    private void writeInt(int value) throws IOException {
        out.write((value >> 24) & 0xFF);
        out.write((value >> 16) & 0xFF);
        out.write((value >> 8) & 0xFF);
        out.write(value & 0xFF);
    }
}
