package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.services.BoardService;
import br.com.sd.streams.BoardInputStream;
import br.com.sd.streams.BoardOutputStream;
import br.com.sd.streams.PixelInputStream;
import br.com.sd.streams.PixelOutputStream;

import java.io.IOException;
import java.net.Socket;

public class ClientTCP {
    public static void main(String[] args) throws IOException {
        Pixel[] pixels = {
                new Pixel(1, 1, 0x000000),
                new Pixel(0, 1, 0x0000FF)
        };

        Socket socket = new Socket("localhost", 5000);

        PixelInputStream pis = new PixelInputStream(socket.getInputStream());
        BoardInputStream bis = new BoardInputStream(socket.getInputStream());

        PixelOutputStream pos = new PixelOutputStream(
                pixels,
                pixels.length,
                socket.getOutputStream()
        );

        BoardService boardService = new BoardService();

        boardService.createBoard(3, 3);

        boardService.loadBoard(bis.readBoard());

        System.out.println(boardService.toString());

        pos.writePixels();

        while (true) {
            Pixel[] pixels_recv = pis.readPixels();
            System.out.println("Pixels recebidos:");
            for (Pixel p : pixels_recv) {
                System.out.println(p.getX() + ", " + p.getY() + ", " + p.getColor());
            }
        }
    }
}
