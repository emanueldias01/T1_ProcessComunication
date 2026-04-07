class Board:
    def __init__(self, height,  width):
        self.height = height
        self.width = width
        self.grid = []

        for i in range(height):
            for j in range(width):
                self.grid[i][j] = 0xFFFFFF

    def __init__(self, initGrid: list[list[int]], width, height):
        self.width = width
        self.height = height
        self.grid = []

        for y in range(height):
            self.grid.append([])
            for x in range(width):
                self.grid[y].append(initGrid[y][x])

    def getColorAt(self, x, y):
        return self.grid[y][x]

    def setPixel(self, x,  y,  color):
        self.grid[y][x] = color

    def getHeight(self):
        return self.height
    

    def setHeight(self, height):
        self.height = height
    

    def  getWidth(self):
        return self.width
    

    def setWidth(self, width):
        self.width = width
    

    def getGrid(self):
        gridCopy = []

        for i in range(self.height):
            for j in range(self.width):
                gridCopy[i][j] = self.grid[i][j]
        
        return gridCopy


    def toString(self):
        out = ""

        out += "Board:\n"
        for y in range(self.height):
            for x in range(self.width):
                color = hex(self.getColorAt(x, y))
                if (color[0] == 'F'):
                    out += "."
                else:
                    out += color[0]
                
                out += "  "
            
            out += "\n"
        

        return out
    

