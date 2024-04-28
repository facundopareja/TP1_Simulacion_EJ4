from random import randrange

from grids import Grid

from constants import CROSSWALK_HEIGHT_LIMIT, CROSSWALK_WIDTH_LIMIT, \
    CROSSWALK_WIDTH_START, CROSSWALK_HEIGHT_START, VEHICLE_WIDTH, MAX_SPEED
from pedestrian import Pedestrian
from cell import Cell
from vehicle import Vehicle


class GridManager:
    def __init__(self):
        self.grid = Grid(CROSSWALK_WIDTH_LIMIT, CROSSWALK_HEIGHT_LIMIT)
        for j in range(1, CROSSWALK_HEIGHT_LIMIT + 1):
            for i in range(1, CROSSWALK_WIDTH_LIMIT + 1):
                if (j == 1 or j == CROSSWALK_HEIGHT_LIMIT or
                        i == 1 or i == CROSSWALK_WIDTH_LIMIT):
                    self.grid.update_cell(i, j, Cell(i, j, True))
                else:
                    self.grid.update_cell(i, j, Cell(i, j, False))

    def create_new_pedestrian(self, green_light, reverse):
        x = CROSSWALK_WIDTH_START
        if reverse:
            x = CROSSWALK_WIDTH_LIMIT
        # Hacer esto con nuestro PRNG
        pedestrian_position = randrange(CROSSWALK_HEIGHT_START, CROSSWALK_HEIGHT_LIMIT)
        cell = self.grid.get_cell(x, pedestrian_position)
        return Pedestrian(green_light, reverse, cell)

    def get_next_empty_row(self, x, y):
        latest_y = y
        for j in range(y, CROSSWALK_HEIGHT_LIMIT):
            latest_y += 1
            for i in range(x, x + VEHICLE_WIDTH):
                if self.grid.get_cell(i, j).occupied():
                    return latest_y - 1
        return latest_y

    def get_vehicle_cells(self, x, y, limit):
        row = self.get_next_empty_row(x, y)
        cells = []
        for j in range(row, limit, -1):
            cells += self.get_row_vehicle_cells(x,j)
        print(len(cells))
        return cells

    def get_row_vehicle_cells(self, x, y):
        cells = []
        for i in range(x, x + VEHICLE_WIDTH):
            cells.append(self.grid.get_cell(i, y))
        return cells

    def road_is_clear(self, x, y):
        for i in range(x, x + VEHICLE_WIDTH):
            for j in range(y, CROSSWALK_HEIGHT_LIMIT):
                if self.grid.get_cell(i, j).occupied():
                    return False
        return True

    def create_new_vehicle(self):
        initial_cells = self.get_row_vehicle_cells(CROSSWALK_WIDTH_START, CROSSWALK_HEIGHT_START - 1)
        return Vehicle(CROSSWALK_WIDTH_START, CROSSWALK_HEIGHT_START - 1, initial_cells)

    def resolve_cell_conflicts(self):
        for column in self.grid:
            for cell in column:
                cell.resolve_conflict()

    def get_furthest_possible_cell(self, reverse, cell, speed, green_light):
        x, y = cell.get_coordinates()
        if not green_light:
            speed = MAX_SPEED
        for i in range(x + 1, x + speed + 1):
            furthest_x = i
            current_cell = self.grid.get_cell(furthest_x, y)
            if current_cell.right_edge():
                break
            if current_cell.occupied():
                furthest_x -= 1
                break
        return self.grid.get_cell(furthest_x, y)

    def show_grid_state(self):
        print("")
        for j in range(CROSSWALK_HEIGHT_START, CROSSWALK_HEIGHT_LIMIT):
            for i in range(CROSSWALK_WIDTH_START, CROSSWALK_WIDTH_LIMIT):
                print(self.grid.get_cell(i, j).get_symbol(), end="")
            print("")
        print("")
