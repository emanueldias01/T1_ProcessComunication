package br.com.sd.tests;

import br.com.sd.entitys.Pixel;

import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

import br.com.sd.streams.PixelInputStream;


public class ServerTCP {
    public static void main(String[] args) throws IOException {

        ServerSocket server = new ServerSocket(8080);

        System.out.println("Servidor esperando conexão...");

        Socket client = server.accept();

        PixelInputStream pis = new PixelInputStream(client.getInputStream());

        Pixel[] pixels = pis.readPixels();

        System.out.println("Pixels recebidos:");

        for (Pixel p : pixels) {
            System.out.println(p.getX() + ", " + p.getY() + ", " + p.getColor());
        }

        client.close();
        server.close();
    }
}
