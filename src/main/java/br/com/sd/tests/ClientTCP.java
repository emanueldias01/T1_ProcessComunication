package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.streams.PixelOutputStream;

import java.io.IOException;
import java.net.Socket;

public class ClientTCP {
    public static void main(String[] args) throws IOException {

        Pixel[] pixels = {
                new Pixel(10, 20, "red"),
                new Pixel(30, 40, "blue")
        };

        Socket socket = new Socket("localhost", 8080);

        PixelOutputStream pos = new PixelOutputStream(
                pixels,
                pixels.length,
                socket.getOutputStream()
        );

        pos.writePixels();

        socket.close();
    }
}