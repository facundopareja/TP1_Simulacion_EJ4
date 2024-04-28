from util import get_random_speed


class Pedestrian:
    def __init__(self, previous_green_light, reverse, cell):
        self.cell = cell
        self.reverse = reverse
        self.next_cell = None
        self.done_crossing = False
        self.first_print = False
        self.previous_light_was_green = previous_green_light
        self.speed = get_random_speed()
        self.symbol = 'p'

    def faster_than_pedestrian_behind_cell(self, grid, x, y, speed):
        if x == 1:
            return True
        for i in range(1, x):
            if grid.get_cell(x - i, y).occupied():
                if grid.get_cell(x - i, y).compare_speeds(speed):
                    break
                else:
                    return False

    def crossed(self):
        return (not self.reverse and self.cell.right_edge() or
                self.reverse and self.cell.left_edge())

    def waiting(self):
        return (not self.reverse and self.cell.left_edge() or
                self.reverse and self.cell.right_edge())

    def get_first_empty_cell_in_front(self, grid_manager, green_light):
        self.next_cell = grid_manager.get_furthest_possible_cell(self.reverse, self.cell, self.speed, green_light)
        return self.cell == self.next_cell

    def calculate_next_cell(self, grid_manager, green_light):
        if self.get_first_empty_cell_in_front(grid_manager, green_light):
            return
        # elif self.move_either_way(grid):
        #     value = generate_random_normalized_value(key1)
        #     if value >= 0.5:
        #         print("Cruce para abajo")
        #         self.next_cell = grid.get_cell(self.x, self.y + 1)
        #     else:
        #         print("Cruce para arriba")
        #         self.next_cell = grid.get_cell(self.x, self.y - 1)
        # elif self.move_top(grid):
        #     self.next_cell = grid.get_cell(self.x, self.y - 1)
        #     print("Cruce para arriba")
        # elif self.move_bottom(grid):
        #     self.next_cell = grid.get_cell(self.x, self.y + 1)
        #     print("Cruce para abajo")

    def prepare_next_move(self, grid_manager, green_light):
        """Se intenta captar la grilla posterior en linea horizontal. Tanto si se tiene exito
        como si no, se pierde uno de los movimientos disponibles. Se considera que se termino de cruzar
        cuando X equivale al ancho de la senda peatonal. En caso de estar roja la luz, o no quedar movimientos
        o haber terminado de cruzar, se vuelve sin pedir nuevas grillas."""
        if self.crossed():
            self.done_crossing = True
            return
        if self.done_crossing:
            return
        if not green_light:
            if self.waiting():
                return
        self.calculate_next_cell(grid_manager, green_light)
        #print(self.next_cell.get_coordinates())
        self.next_cell.attempt_to_occupy(self)

    def move(self):
        """Se realiza el movimiento. En caso de haber finalizado de cruzar, se libera la grilla actual y se imprime
        un mensaje una unica vez. En caso de no haber finalizado, si se gano la nueva grilla, se libera la grilla actual
        y se aumenta la coordenada X en 1."""
        if self.done_crossing:
            self.cell.vacate(self)
            if not self.first_print:
                x, y = self.cell.get_coordinates()
                print(f"Peaton cruzo por linea {y - 1}")
                self.first_print = True
            return
        if self.next_cell is None or not self.next_cell.won(self):
            return
        self.cell.vacate(self)
        self.cell = self.next_cell
        self.next_cell = None

    def get_symbol(self):
        return self.symbol

    def get_direction(self):
        return self.reverse
