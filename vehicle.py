from constants import CROSSWALK_HEIGHT, VEHICLE_WIDTH, VEHICLE_LENGTH


class Vehicle:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y
        self.remaining_body = VEHICLE_LENGTH
        self.done_crossing = False
        self.started_crossing = False
        self.speed = 6
        self.remaining_moves = self.speed
        self.symbol = 'v'
        self.requested_cells = []

    def prepare_next_move(self, grid, green_light):
        if green_light and self.y == 0:
            self.remaining_moves = 0
            return
        if self.y == CROSSWALK_HEIGHT:
            self.started_crossing = True
            return
        if self.remaining_moves == 0 or self.done_crossing:
            return
        for i in range(VEHICLE_WIDTH):
            cell = grid.get_cell(self.x + i, self.y + 1)
            self.requested_cells.append(cell)
            cell.attempt_to_occupy(self)
        self.remaining_moves -= 1

    def move(self, grid):
        if len(self.requested_cells) == 0 and not self.started_crossing:
            self.remaining_moves = 0
            return
        if self.started_crossing:
            self.remaining_moves = 0
            if self.remaining_body == VEHICLE_LENGTH:
                print("Car starting to cross")
            if self.remaining_body == 0:
                print("Car crossed completely")
                self.done_crossing = True
                return
            for x in range(self.x, self.x + VEHICLE_WIDTH):
                grid.get_cell(x, self.y - self.remaining_body + 1).vacate(self)
            self.remaining_body -= 1
            return
        cells_to_free = []
        for cell in self.requested_cells:
            if not cell.won(self):
                for occupied_cell in cells_to_free:
                    occupied_cell.vacate(self)
                self.remaining_moves = 0
                return
            cells_to_free.append(cell)
        if self.y >= VEHICLE_LENGTH:
            for x in range(self.x, self.x + VEHICLE_WIDTH):
                grid.get_cell(x, self.y - VEHICLE_LENGTH + 1).vacate(self)
        self.requested_cells = []
        self.y += 1

    def get_symbol(self):
        return self.symbol

    def done_moving(self):
        return self.remaining_moves == 0

    def reset_movement(self):
        self.remaining_moves = self.speed
