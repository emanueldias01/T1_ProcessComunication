package br.com.sd.streams;

import br.com.sd.entitys.Pixel;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class PixelInputStream extends InputStream {

    private InputStream in;

    public PixelInputStream(InputStream in) {
        this.in = in;
    }

    @Override
    public int read() throws IOException {
        return in.read();
    }

    public int[][] readPixelMap() throws IOException {
        int width = readInt();
        int height = readInt();

        int[][] map = new int[width][height];

        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                map[i][j] = readInt();
            }
        }

        return map;
    }

    public Pixel[] readPixels() throws IOException {
        int quantidade = readInt();

        Pixel[] pixels = new Pixel[quantidade];

        for (int i = 0; i < quantidade; i++) {
            int x = readInt();
            int y = readInt();
            int color = readInt();

            pixels[i] = new Pixel(x, y, color);
        }

        return pixels;
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
