package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelInputStream;

import java.io.IOException;

public class DefaultInput {
    public static void main(String[] args) throws IOException {

        PixelInputStream pis = new PixelInputStream(System.in);

        Pixel[] pixels = pis.readPixels();

        for (Pixel p : pixels) {
            System.out.println(p.getX() + ", " + p.getY() + ", " + p.getColor());
        }
    }
}
