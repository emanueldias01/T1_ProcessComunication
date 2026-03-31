package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelOutputStream;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileOutput {
    public static void main(String[] args) {

        Pixel[] pixels = {
                new Pixel(10, 20, "red"),
                new Pixel(30, 40, "blue")
        };

        FileOutputStream fos = null;
        try {
            fos = new FileOutputStream("pixels.txt");
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }

        PixelOutputStream pos = new PixelOutputStream(pixels, pixels.length, fos);
        try {
            pos.writePixels();
            fos.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}
