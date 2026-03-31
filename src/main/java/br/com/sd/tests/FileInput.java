package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelInputStream;

import java.io.FileInputStream;
import java.io.IOException;

public class FileInput {
    public static void main(String[] args) throws IOException {

        FileInputStream fis = new FileInputStream("pixels.bin");

        PixelInputStream pis = new PixelInputStream(fis);

        Pixel[] pixels = pis.readPixels();

        for (Pixel p : pixels) {
            System.out.println(p.getX() + ", " + p.getY() + ", " + p.getColor());
        }

        fis.close();
    }
}
