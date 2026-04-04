package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelOutputStream;

import java.io.IOException;
import java.net.Socket;

public class ClientTCP {
    public static void main(String[] args) throws IOException {
        Pixel[] pixels = {
                new Pixel(2, 2, 0xF00000),
                new Pixel(0, 1, 0x0000FF)
        };

        Socket socket = new Socket("localhost", 5000);
        PixelOutputStream pos = new PixelOutputStream(
                pixels,
                pixels.length,
                socket.getOutputStream()
        );

        pos.writePixels();
    }
}
