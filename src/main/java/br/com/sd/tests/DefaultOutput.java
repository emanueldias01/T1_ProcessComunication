package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelOutputStream;

import java.io.IOException;

public class DefaultOutput {
    public static void main(String[] args) {
        Pixel[] pixels = {
                new Pixel(10, 20, "red"),
                new Pixel(30, 40, "blue")
        };

        PixelOutputStream pos = new PixelOutputStream(pixels, pixels.length, System.out);
        try {
            pos.writePixels();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
