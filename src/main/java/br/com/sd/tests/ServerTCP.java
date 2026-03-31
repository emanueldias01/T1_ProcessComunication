package br.com.sd.tests;

import br.com.sd.entitys.Pixel;

import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerTCP {
    public static void main(String[] args) throws IOException {

        ServerSocket server = new ServerSocket(8080);

        System.out.println("Servidor esperando conexão...");

        Socket client = server.accept();
        InputStream in = client.getInputStream();

        while (true) {
            int data = in.read();
            if (data == -1) break;

            System.out.print(data + " ");
        }

        client.close();
        server.close();
    }
}
