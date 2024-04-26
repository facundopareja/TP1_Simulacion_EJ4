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
        self.first_print = False
        self.requested_cells = []

    def prepare_next_move(self, grid, green_light):
        """Se intenta captar las siguientes VEHICLE_WIDTH grillas posteriores en linea vertical. Tanto si se tiene exito
        como si no, se pierde uno de los movimientos disponibles. Se considera que se termino de cruzar
        cuando Y == largo de la senda peatonal."""
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
            if self.remaining_body == 0:
                self.done_crossing = True
                if not self.first_print:
                    print("Auto cruzo calle")
                    self.first_print = True
                return
            for x in range(self.x, self.x + VEHICLE_WIDTH):
                grid.get_cell(x, self.y - self.remaining_body + 1).vacate(self)
            self.remaining_body -= 1
            return
        for cell in self.requested_cells:
            if not cell.won(self):
                self.requested_cells.remove(cell)
        if len(self.requested_cells) < VEHICLE_WIDTH:
            for cell in self.requested_cells:
                cell.vacate(self)
            self.requested_cells = []
            return
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
