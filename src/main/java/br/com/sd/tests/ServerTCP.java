package br.com.sd.tests;

import br.com.sd.entitys.Pixel;

import java.io.IOException;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CopyOnWriteArrayList;

import br.com.sd.services.BoardService;
import br.com.sd.streams.BoardOutputStream;
import br.com.sd.streams.PixelInputStream;
import br.com.sd.streams.PixelOutputStream;


public class ServerTCP {
    static private List<OutputStream> clients = new CopyOnWriteArrayList<>();
    static private ConcurrentLinkedQueue<Pixel[]> tickBuffer = new ConcurrentLinkedQueue<>();
    static private final BoardService boardService = new BoardService();

    public static void main(String[] args) throws IOException {
        boardService.createBoard(3, 3);
        System.out.println(boardService.toString());

        ServerSocket server = new ServerSocket(5000);
        System.out.println("Servidor esperando conexão...");

        Thread.ofPlatform().start(ServerTCP::tickBoard);
        while (true) {
            Socket client = server.accept();
            Thread.ofVirtual().start(() -> handleClient(client));
        }
    }

    public static void handleClient(Socket client) {
        OutputStream os = null;
        try {
            os = client.getOutputStream();
            PixelInputStream pis = new PixelInputStream(client.getInputStream());
            BoardOutputStream gos = new BoardOutputStream(boardService.getBoard(), os);
            gos.writeBoard();

            clients.add(os);
            while (!client.isClosed()) {
                Pixel[] pixels = pis.readPixels();
                System.out.println("Pixels recebidos:");
                for (Pixel p : pixels) {
                    System.out.println(p.getX() + ", " + p.getY() + ", " + p.getColor());
                }

                if (pixels.length > 0) {
                    tickBuffer.add(pixels);
                }

                System.out.println(boardService.toString());
            }
        } catch (Exception e) {
            System.out.println("conexão com cliente interrompida");
        } finally {
            if (os != null) {
                clients.remove(os);
            }
            try {
                client.close();
            } catch (IOException e) {
                System.out.println("Erro ao fechar socket: " + e.getMessage());
            }
            System.out.println("Cliente removido. Clientes online: " + clients.size());
        }
    }

    private static final Pixel[] boardTick = new Pixel[10000];
    private static int length = 0;

    @SuppressWarnings("BusyWait")
    public static void tickBoard() {
        Pixel[] chunk;
        boolean is_changed = false;
        while (true) {
            while ((chunk = tickBuffer.poll()) != null) {
                for (Pixel p : chunk) {
                    boardService.setPixel(p);
                    boardTick[length++] = p;
                }
            }

            System.out.println(boardService.toString());

            broadcast();

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static void broadcast() {
        for (OutputStream os : clients) {
            PixelOutputStream pos = new PixelOutputStream(boardTick, length, os);
            try {
                pos.writePixels();
            } catch (IOException e) {
                System.out.println("cant send pixels for one client");
            }
            System.out.println("aoba");
        }
        length = 0;
    }
}
