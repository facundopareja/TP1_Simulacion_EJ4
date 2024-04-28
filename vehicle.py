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
        self.requested_cells = set(initial_cells)

    def prepare_next_move(self, grid_manager, green_light):
        """Se intenta captar las siguientes VEHICLE_WIDTH grillas posteriores en linea vertical.
        Se considera que se termino de cruzar cuando Y == largo de la senda peatonal."""
        if green_light and cells_are_waiting_cells(self.requested_cells):
            return
        if (self.y == CROSSWALK_HEIGHT_LIMIT or
                not green_light and grid_manager.road_is_clear(self.x, self.y)):
            self.done_crossing = True
            return
        if self.done_crossing:
            return
        limit = CROSSWALK_HEIGHT_START
        if self.y >= CROSSWALK_HEIGHT_START + VEHICLE_LENGTH:
            limit = self.y - VEHICLE_LENGTH
        cells = grid_manager.get_vehicle_cells(self.x, self.y+1, limit)
        self.requested_cells.update(set(cells))
        for cell in cells:
            cell.attempt_to_occupy(self)

    def move(self):
        if self.done_crossing:
            if not self.first_print:
                print(f"Auto cruzo")
                self.first_print = True
            return
        cells_to_free = []
        all_cells_acquired = True
        for requested_cell in self.requested_cells:
            if requested_cell.won(self):
                cells_to_free.append(requested_cell)
            else:
                all_cells_acquired = False
        if not all_cells_acquired:
            for cell in cells_to_free:
                cell.vacate(self)
        self.requested_cells = set()

    def get_symbol(self):
        return self.symbol
