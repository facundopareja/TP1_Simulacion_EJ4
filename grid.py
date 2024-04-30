class Grid:
    def __init__(self, width, height, default_value=None):
        self.width = width
        self.height = height
        self.grid = [[default_value for _ in range(width)] for _ in range(height)]

    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        self.grid[index] = value

    def get(self, x, y):
        x -= 1
        y -= 1
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return None

    def set(self, x, y, value):
        x -= 1
        y -= 1
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
        else:
            raise ValueError("Coordinates out of bounds")

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.grid])