package br.com.sd.services;

import br.com.sd.entitys.Pixel;

public class BucketService {
    public Pixel fillIn(int x, int y, int color) {


        return new Pixel(x, y, color);
    }
}
