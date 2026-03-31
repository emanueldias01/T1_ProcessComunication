package br.com.sd.services;

import br.com.sd.entitys.Pixel;

import java.util.List;
import java.util.stream.Collectors;

public class PixelService {

    public Pixel createPixel(int x, int y, String color) {
        return new Pixel(x, y, color);
    }

    public List<Pixel> getPixelsByColor(List<Pixel> pixels, String color) {
        return pixels.stream()
                .filter(p -> p.getColor().equalsIgnoreCase(color))
                .collect(Collectors.toList());
    }

    public Pixel findPixelAtPosition(List<Pixel> pixels, int x, int y) {
        return pixels.stream()
                .filter(p -> p.getX() == x && p.getY() == y)
                .findFirst()
                .orElse(null);
    }
}
