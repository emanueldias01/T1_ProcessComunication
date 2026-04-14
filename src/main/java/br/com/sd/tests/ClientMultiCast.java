package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.services.BoardService;
import br.com.sd.streams.BoardInputStream;
import br.com.sd.streams.PixelInputStream;
import br.com.sd.streams.PixelOutputStream;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.*;

public class ClientMultiCast {
    private static final String MULTICAST_IP = "238.1.1.4";
    private static final int MULTICAST_PORT = 12347;
    private static final int SERVER_TCP_PORT = 5001;

    public static void main(String[] args) throws IOException {
        BoardService boardService = new BoardService();
        boardService.createBoard(500, 500);

        System.out.println("Conectando ao servidor via TCP para baixar o Board...");
        try (Socket socket = new Socket("localhost", SERVER_TCP_PORT)) {

            BoardInputStream bis = new BoardInputStream(socket.getInputStream());
            boardService.loadBoard(bis.readBoard());
            System.out.println("Board carregado com sucesso!");

            Pixel[] pixelsToSend = { new Pixel(1, 1, 0xFF0000) };
            PixelOutputStream pos = new PixelOutputStream(pixelsToSend, pixelsToSend.length, socket.getOutputStream());
            pos.writePixels();

            startMulticastListener(boardService);

            // Mantém a main viva para enviar dados se quiser ou apenas observar
            while(true) { Thread.sleep(1000); }

        } catch (Exception e) {
            System.err.println("Erro na conexão: " + e.getMessage());
        }
    }

    /**
     * Escuta as atualizações em tempo real via UDP Multicast
     */
    private static void startMulticastListener(BoardService boardService) {
        Thread.ofPlatform().start(() -> {
            try (MulticastSocket mcs = new MulticastSocket(MULTICAST_PORT)) {
                InetAddress group = InetAddress.getByName(MULTICAST_IP);
                mcs.joinGroup(group);

                System.out.println("Escutando atualizações via Multicast...");

                while (true) {
                    byte[] buffer = new byte[65507]; // Tamanho máximo de um pacote UDP
                    DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

                    mcs.receive(packet);

                    // Transforma os bytes recebidos de volta em objetos Pixel
                    ByteArrayInputStream bais = new ByteArrayInputStream(packet.getData(), 0, packet.getLength());
                    PixelInputStream pis = new PixelInputStream(bais);

                    Pixel[] pixels_recv = pis.readPixels();

                    if (pixels_recv != null) {
                        for (Pixel p : pixels_recv) {
                            boardService.setPixel(p);
                            System.out.println("UDP Update: " + p.getX() + "," + p.getY() + " Color: " + p.getColor());
                        }
                    }
                }
            } catch (IOException e) {
                System.err.println("Erro no listener Multicast: " + e.getMessage());
            }
        });
    }
}