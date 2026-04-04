package br.com.sd.entitys;

public class Board {

    private int height;
    private int width;
    private int[][] grid;

    public Board(int height, int width) {
        this.height = height;
        this.width = width;
        this.grid = new int[height][width];

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                this.grid[i][j] = 0xFFFFFF;
            }
        }
    }

    public void setPixel(int x, int y, int color) {
        this.grid[y][x] = color;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public String toString() {
        StringBuilder out = new StringBuilder();
        out.append("Board:\n");
        for (int i = 0; i < this.height; i++) {
            for (int j = 0; j < this.width; j++) {
                String color = String.format("%06X", this.grid[i][j]);
                if (color.charAt(0) == 'F') {
                    out.append(".");
                } else {
                    out.append(color.charAt(0));
                }
                out.append("  ");
            }
            out.append("\n");
        }

        return out.toString();
    }
}
