from constants import VEHICLE_LENGTH, VEHICLE_SPEED, CROSSWALK_HEIGHT_LIMIT, CROSSWALK_HEIGHT_START
from util import cells_are_waiting_cells


class Vehicle:
    def __init__(self, x, y, initial_cells):
        self.remaining_body = VEHICLE_LENGTH
        self.x = x
        self.y = y
        self.done_crossing = False
        self.speed = VEHICLE_SPEED
        self.symbol = 'v'
        self.first_print = False
        self.current_cells = set(initial_cells)
        self.future_cells = set()

    def prepare_next_move(self, grid_manager, green_light):
        """Se intenta captar las siguientes VEHICLE_WIDTH grillas posteriores en linea vertical.
        Se considera que se termino de cruzar cuando Y == largo de la senda peatonal."""
        if green_light and cells_are_waiting_cells(self.current_cells):
            return
        if self.y == CROSSWALK_HEIGHT_LIMIT:
            self.done_crossing = True
            return
        if self.done_crossing:
            return
        self.future_cells = set(grid_manager.get_vehicle_cells(self.x, self.y))
        for cell in self.future_cells:
            cell.attempt_to_occupy(self)

    def move(self):
        if self.done_crossing:
            if not self.first_print:
                print(f"Auto cruzo")
                self.first_print = True
                for cell in self.current_cells:
                    cell.vacate(self)
                self.future_cells = set()
            return
        cells_to_free = []
        all_cells_acquired = True
        max_y = self.y
        for requested_cell in self.future_cells:
            if requested_cell.won(self):
                x, y = requested_cell.get_coordinates()
                max_y = max(max_y, y)
                cells_to_free.append(requested_cell)
            else:
                all_cells_acquired = False
        if not all_cells_acquired:
            for cell in cells_to_free:
                cell.vacate(self)
            return
        for cell in (self.current_cells.difference(self.future_cells)):
            cell.vacate(self)
        self.y = max_y
        self.current_cells = self.future_cells.copy()
        self.future_cells = set()

    def get_symbol(self):
        return self.symbol
