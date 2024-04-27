from constants import CROSSWALK_WIDTH, key1, CROSSWALK_HEIGHT, MAX_SPEED
from util import generate_random_normalized_value


def faster_than_pedestrian_behind_cell(grid, x, y, speed):
    if x == 1:
        return True
    for i in range(1, x):
        if grid.get_cell(x - i, y).occupied():
            if grid.get_cell(x - i, y).compare_speeds(speed):
                break
            else:
                return False


class Pedestrian:
    def __init__(self, initial_x, initial_y, previous_green_light):
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
        self.symbol = 'p'
        self.next_cell = None
        self.next_x = None
        self.previous_light_was_green = previous_green_light

    def faster_than_pedestrian_behind_bottom_cell(self, grid):
        return faster_than_pedestrian_behind_cell(grid, self.x, self.y + 1, self.speed)

    def faster_than_pedestrian_behind_top_cell(self, grid):
        return faster_than_pedestrian_behind_cell(grid, self.x, self.y - 1, self.speed)

    def no_pedestrian_above(self, grid):
        if self.y == 1:
            return True
        return grid.get_cell(self.x, self.y - 1).occupied()

    def no_pedestrian_under(self, grid):
        if self.y == CROSSWALK_HEIGHT:
            return True
        return grid.get_cell(self.x, self.y + 1).occupied()

    def behind_a_pedestrian(self, grid):
        if self.x == CROSSWALK_WIDTH:
            return False
        return grid.get_cell(self.x + 1, self.y).occupied()

    def distance_to_nearest_top_neighbor_larger_speed(self, grid):
        max_empty_cells = 0
        for i in range(1, self.y):
            if grid.get_cell(self.x, self.y - i).occupied():
                max_empty_cells = i
                break
        if max_empty_cells > self.speed:
            return True
        return False

    def distance_to_nearest_bottom_neighbor_larger_speed(self, grid):
        max_empty_cells = 0
        for j in range(1, CROSSWALK_HEIGHT - self.y + 1):
            if grid.get_cell(self.x, self.y + j).occupied():
                max_empty_cells = j
                break
        if max_empty_cells > self.speed:
            return True
        return False

    def move_bottom(self, grid):
        return (self.behind_a_pedestrian(grid) and
                self.no_pedestrian_under(grid) and
                not self.no_pedestrian_above(grid) and
                self.distance_to_nearest_bottom_neighbor_larger_speed(grid)
                and self.faster_than_pedestrian_behind_bottom_cell(grid))

    def move_top(self, grid):
        return (self.behind_a_pedestrian(grid) and
                self.no_pedestrian_above(grid) and
                not self.no_pedestrian_under(grid) and
                self.distance_to_nearest_top_neighbor_larger_speed(grid)
                and self.faster_than_pedestrian_behind_top_cell(grid))

    def move_either_way(self, grid):
        return (self.behind_a_pedestrian(grid) and
                self.no_pedestrian_under(grid) and self.no_pedestrian_above(grid) and
                self.distance_to_nearest_bottom_neighbor_larger_speed(grid) and
                self.distance_to_nearest_top_neighbor_larger_speed(grid) and
                self.faster_than_pedestrian_behind_bottom_cell(grid) and
                self.faster_than_pedestrian_behind_top_cell(grid))

    def get_first_empty_cell_in_front(self, grid, light_changed):
        furthest_x = 0
        speed = self.speed
        if light_changed:
            speed = MAX_SPEED
        while furthest_x < speed:
            if (self.x + furthest_x == CROSSWALK_WIDTH or
                    grid.get_cell(self.x+furthest_x+1, self.y).occupied()):
                break
            furthest_x += 1
        self.next_x = self.x + furthest_x
        self.next_cell = grid.get_cell(self.x + furthest_x, self.y)
        if furthest_x == 0:
            return False
        return True

    def calculate_next_cell(self, grid, light_changed):
        if self.get_first_empty_cell_in_front(grid, light_changed):
            return
        elif self.move_either_way(grid):
            value = generate_random_normalized_value(key1)
            if value >= 0.5:
                print("Cruce para abajo")
                self.next_cell = grid.get_cell(self.x, self.y + 1)
            else:
                print("Cruce para arriba")
                self.next_cell = grid.get_cell(self.x, self.y - 1)
        elif self.move_top(grid):
            self.next_cell = grid.get_cell(self.x, self.y - 1)
            print("Cruce para arriba")
        elif self.move_bottom(grid):
            self.next_cell = grid.get_cell(self.x, self.y + 1)
            print("Cruce para abajo")

    def prepare_next_move(self, grid, green_light):
        """Se intenta captar la grilla posterior en linea horizontal. Tanto si se tiene exito
        como si no, se pierde uno de los movimientos disponibles. Se considera que se termino de cruzar
        cuando X equivale al ancho de la senda peatonal. En caso de estar roja la luz, o no quedar movimientos
        o haber terminado de cruzar, se vuelve sin pedir nuevas grillas."""
        light_changed = self.previous_light_was_green ^ green_light
        self.previous_light_was_green = green_light
        if self.x == CROSSWALK_WIDTH:
            self.done_crossing = True
            return
        if self.done_crossing:
            return
        if not green_light:
            if self.x == 0:
                return
        self.calculate_next_cell(grid, light_changed)
        self.next_cell.attempt_to_occupy(self)

    def move(self, grid):
        """Se realiza el movimiento. En caso de haber finalizado de cruzar, se libera la grilla actual y se imprime
        un mensaje una unica vez. En caso de no haber finalizado, si se gano la nueva grilla, se libera la grilla actual
        y se aumenta la coordenada X en 1."""
        if self.done_crossing:
            old_cell = grid.get_cell(self.x, self.y)
            old_cell.vacate(self)
            if not self.first_print:
                print(f"Peaton cruzo por linea {self.y}")
                self.first_print = True
            return
        if self.next_cell is None:
            return
        if not self.next_cell.won(self):
            return
        grid.get_cell(self.x, self.y).vacate(self)
        self.x = self.next_x
        self.next_cell = None
        self.next_x = None


    def get_symbol(self):
        return self.symbol
