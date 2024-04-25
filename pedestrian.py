from constants import CROSSWALK_WIDTH, key1
from util import generate_random_normalized_value, show_grid_state


class Pedestrian:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y
        value = generate_random_normalized_value(key1)
        self.done_crossing = False
        self.first_print = False
        if value > 0.978:
            self.speed = 6
        elif 0.978 >= value > 0.93:
            self.speed = 5
        elif 0.93 >= value > 0.793:
            self.speed = 4
        elif 0.793 >= value > 0.273:
            self.speed = 3
        elif value <= 0.273:
            self.speed = 2
        self.remaining_moves = self.speed
        self.symbol = 'p'

    def prepare_next_move(self, grid, green_light):
        if self.x == CROSSWALK_WIDTH:
            self.done_crossing = True
            return
        if self.remaining_moves == 0 or self.done_crossing:
            return
        if not green_light and self.x == 0:
            self.remaining_moves = 0
            return
        grid.get_cell(self.x+1, self.y).attempt_to_occupy(self)
        self.remaining_moves -= 1

    def move(self, grid):
        if self.done_crossing:
            self.remaining_moves = 0
            old_cell = grid.get_cell(self.x, self.y)
            old_cell.vacate(self)
            if not self.first_print:
                print(f"Done crossing at lane {self.y}")
                self.first_print = True
            return
        new_cell = grid.get_cell(self.x+1, self.y)
        if not new_cell.won(self):
            self.remaining_moves = 0
            return
        old_cell = grid.get_cell(self.x, self.y)
        old_cell.vacate(self)
        self.x += 1

    def done_moving(self):
        return self.remaining_moves == 0

    def reset_movement(self):
        self.remaining_moves = self.speed

    def get_symbol(self):
        return self.symbol
