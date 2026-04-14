package br.com.sd.tests;

import br.com.sd.entitys.Pixel;
import br.com.sd.services.BoardService;
import br.com.sd.streams.BoardOutputStream;
import br.com.sd.streams.PixelInputStream;
import br.com.sd.streams.PixelOutputStream;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.*;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CopyOnWriteArrayList;

public class ServerMultiCast {
    private static final String MULTICAST_IP = "224.1.1.1";
    private static final int MULTICAST_PORT = 50003;

    static private ConcurrentLinkedQueue<Pixel[]> tickBuffer = new ConcurrentLinkedQueue<>();
    static private final BoardService boardService = new BoardService();

    public static void main(String[] args) throws IOException {
        boardService.createBoard(500, 500);

        ServerSocket server = new ServerSocket(5010);

        Thread.ofPlatform().start(ServerMultiCast::tickBoard);

        while (true) {
            Socket client = server.accept();
            Thread.ofVirtual().start(() -> handleClient(client));
        }
    }

    public static void handleClient(Socket client) {
        try {
            OutputStream os = client.getOutputStream();
            PixelInputStream pis = new PixelInputStream(client.getInputStream());

            // envia o board uma vez
            BoardOutputStream bos = new BoardOutputStream(boardService.getBoard(), os);
            bos.writeBoard();

            while (!client.isClosed()) {
                Pixel[] pixels = pis.readPixels();
                if (pixels != null && pixels.length > 0) {
                    tickBuffer.add(pixels);
                }
            }
        } catch (Exception e) {
            System.out.println("Conexão TCP com cliente encerrada.");
        }
    }

    private static final Pixel[] boardTick = new Pixel[10000];
    private static int length = 0;

    public static void tickBoard() {
        Pixel[] chunk;
        while (true) {
            while ((chunk = tickBuffer.poll()) != null) {
                for (Pixel p : chunk) {
                    boardService.setPixel(p);
                    boardTick[length++] = p;
                }
            }

            if (length != 0) {
                broadcastMulticast();
            }

            length = 0;
            
            try {
                Thread.sleep(16);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private static void broadcastMulticast() {
        try (DatagramSocket udpSocket = new DatagramSocket()) {
            InetAddress group = InetAddress.getByName(MULTICAST_IP);

            ByteArrayOutputStream baos = new ByteArrayOutputStream();

            PixelOutputStream pos = new PixelOutputStream(boardTick, length, baos);
            pos.writePixels();

            byte[] data = baos.toByteArray();
            DatagramPacket packet = new DatagramPacket(data, data.length, group, MULTICAST_PORT);

            udpSocket.send(packet);
        } catch (IOException e) {
            System.out.println("Erro no broadcast multicast: " + e.getMessage());
        }
    }
}