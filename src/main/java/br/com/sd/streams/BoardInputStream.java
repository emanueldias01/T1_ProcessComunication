package br.com.sd.streams;

import br.com.sd.entitys.Board;
import br.com.sd.services.BoardService;

import java.io.IOException;
import java.io.InputStream;

public class BoardInputStream extends InputStream {

    private InputStream in;

    public BoardInputStream(InputStream in) {
        this.in = in;
    }

    @Override
    public int read() throws IOException {
        return in.read();
    }

    public Board readBoard() throws IOException {
        int width = readInt();
        int height = readInt();

        int[][] grid = new int[width][height];

        for (int y = 0; y < width; y++) {
            for (int x = 0; x < height; x++) {
                grid[y][x] = readInt();
            }
        }

        return new Board(grid);
    }

    private int readInt() throws IOException {
        int b1 = in.read();
        int b2 = in.read();
        int b3 = in.read();
        int b4 = in.read();

        if ((b1 | b2 | b3 | b4) < 0) {
            throw new IOException("Fim do stream inesperado");
        }

        return ((b1 << 24) |
                (b2 << 16) |
                (b3 << 8) |
                b4);
    }
}
