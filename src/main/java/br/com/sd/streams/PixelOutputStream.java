package br.com.sd.streams;

import br.com.sd.entitys.Pixel;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class PixelOutputStream extends OutputStream {

    private Pixel[] pixels;
    private int quantidade;
    private OutputStream out;

    public PixelOutputStream(Pixel[] pixels, int quantidade, OutputStream out) {
        this.pixels = pixels;
        this.quantidade = quantidade;
        this.out = out;
    }

    @Override
    public void write(int b) throws IOException {
        out.write(b);
    }

    public void writePixels() throws IOException {
        writeInt(quantidade);

        for (int i = 0; i < quantidade; i++) {
            Pixel p = pixels[i];

            writeInt(p.getX());

            writeInt(p.getY());

            byte[] colorBytes = p.getColor().getBytes(StandardCharsets.UTF_8);

            writeInt(colorBytes.length);

            out.write(colorBytes);
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
