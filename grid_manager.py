from random import randrange

from constants import CROSSWALK_HEIGHT_LIMIT, CROSSWALK_WIDTH_LIMIT, \
    CROSSWALK_WIDTH_START, CROSSWALK_HEIGHT_START, VEHICLE_WIDTH, MAX_SPEED, VEHICLE_SPEED, VEHICLE_LENGTH, \
    CROSSWALK_HEIGHT, CROSSWALK_WIDTH, key1
from grid import Grid
from pedestrian import Pedestrian
from cell import Cell
from util import generate_random_normalized_value, get_random_y_position
from vehicle import Vehicle


class GridManager:
    def __init__(self):
        self.grid = Grid(CROSSWALK_WIDTH_LIMIT, CROSSWALK_HEIGHT_LIMIT)
        self.car_lane_start = 2
        for j in range(1, CROSSWALK_HEIGHT_LIMIT + 1):
            for i in range(1, CROSSWALK_WIDTH_LIMIT + 1):
                if (j == 1 or j == CROSSWALK_HEIGHT_LIMIT or
                        i == 1 or i == CROSSWALK_WIDTH_LIMIT):
                    self.grid.set(i, j, Cell(i, j, True))
                else:
                    self.grid.set(i, j, Cell(i, j, False))

    def create_new_pedestrian(self, green_light, reverse):
        x = CROSSWALK_WIDTH_START - 1
        if reverse:
            x = CROSSWALK_WIDTH_LIMIT
        pedestrian_position = get_random_y_position()
        cell = self.grid.get(x, pedestrian_position)
        return Pedestrian(green_light, reverse, cell)

    def get_next_empty_row(self, x, y):
        for j in range(y + 1, y + VEHICLE_SPEED + 1):
            latest_y = j
            if j >= CROSSWALK_HEIGHT_LIMIT:
                return CROSSWALK_HEIGHT_LIMIT
            for i in range(x, x + VEHICLE_WIDTH):
                if self.grid.get(i, j).occupied():
                    return latest_y - 1
        return latest_y

    def get_vehicle_cells(self, x, y):
        row = self.get_next_empty_row(x, y)
        cells = []
        for j in range(row, row - VEHICLE_LENGTH, -1):
            if j < CROSSWALK_WIDTH_START or j > CROSSWALK_WIDTH_LIMIT:
                break
            cells += self.get_row_vehicle_cells(x, j)
        return cells

    def get_row_vehicle_cells(self, x, y):
        cells = []
        for i in range(x, x + VEHICLE_WIDTH):
            cells.append(self.grid.get(i, y))
        return cells

    def road_is_clear(self, x, y):
        for i in range(x, x + VEHICLE_WIDTH):
            for j in range(y, CROSSWALK_HEIGHT_LIMIT):
                if self.grid.get(i, j).occupied():
                    return False
        return True

    def create_new_vehicle(self):
        initial_cells = self.get_row_vehicle_cells(CROSSWALK_WIDTH_START, CROSSWALK_HEIGHT_START - 1)
        vehicle = Vehicle(self.car_lane_start, CROSSWALK_HEIGHT_START - 1, initial_cells)
        self.car_lane_start += VEHICLE_WIDTH + 1
        if self.car_lane_start >= CROSSWALK_WIDTH_LIMIT:
            self.car_lane_start = CROSSWALK_WIDTH_START
        return vehicle

    def resolve_cell_conflicts(self):
        for column in self.grid:
            for cell in column:
                cell.resolve_conflict()

    def get_furthest_possible_cell(self, reverse, cell, speed, green_light):
        x, y = cell.get_coordinates()
        if not green_light:
            speed = MAX_SPEED
        if not reverse:
            for i in range(x + 1, x + speed + 1):
                furthest_x = i
                current_cell = self.grid.get(furthest_x, y)
                if current_cell.right_edge():
                    break
                if current_cell.occupied():
                    if not current_cell.same_direction(reverse):
                        continue
                    furthest_x -= 1
                    break
        else:
            for i in range(x - 1, x - speed - 1, -1):
                furthest_x = i
                current_cell = self.grid.get(furthest_x, y)
                if current_cell.left_edge():
                    break
                if current_cell.occupied():
                    if not current_cell.same_direction(reverse):
                        continue
                    furthest_x += 1
                    break
        return self.grid.get(furthest_x, y)

    def faster_than_pedestrian_behind_cell(self, x, y, speed):
        for i in range(1, (x - CROSSWALK_WIDTH_START) + 1):
            if self.grid.get(x - i, y).occupied():
                if self.grid.get(x - i, y).faster(speed):
                    return True
                else:
                    return False

    def faster_than_pedestrian_behind_bottom_cell(self, cell, speed):
        x, y = cell.get_coordinates()
        if x == CROSSWALK_WIDTH_LIMIT:
            return True
        return self.faster_than_pedestrian_behind_cell(x, y + 1, speed)

    def faster_than_pedestrian_behind_top_cell(self, cell, speed):
        x, y = cell.get_coordinates()
        if x == CROSSWALK_WIDTH_START:
            return True
        return self.faster_than_pedestrian_behind_cell(x, y - 1, speed)

    def no_pedestrian_above(self, cell):
        x, y = cell.get_coordinates()
        if y == CROSSWALK_WIDTH_START:
            return False
        return self.grid.get(x, y - 1).occupied()

    def no_pedestrian_under(self, cell):
        x, y = cell.get_coordinates()
        if y == CROSSWALK_HEIGHT:
            return False
        return self.grid.get(x, y + 1).occupied()

    def behind_a_pedestrian(self, cell, reverse):
        x, y = cell.get_coordinates()
        if (not reverse and x == CROSSWALK_WIDTH or
                reverse and x == CROSSWALK_WIDTH_START - 1):
            return False
        x_in_front = x + 1
        if reverse:
            x_in_front = x - 1
        return self.grid.get(x_in_front, y).occupied()

    def distance_to_nearest_top_neighbor_larger_speed(self, cell, speed):
        max_empty_cells = 0
        x, y = cell.get_coordinates()
        for i in range(1, (y - CROSSWALK_HEIGHT_START) + 1):
            if self.grid.get(x, y - i).occupied():
                max_empty_cells = i
                break
        if max_empty_cells > speed:
            return True
        return False

    def distance_to_nearest_bottom_neighbor_larger_speed(self, cell, speed):
        max_empty_cells = 0
        x, y = cell.get_coordinates()
        for j in range(1, CROSSWALK_HEIGHT - y + 1):
            if self.grid.get(x, y + j).occupied():
                max_empty_cells = j
                break
        if max_empty_cells > speed:
            return True
        return False

    def top_cell(self, pedestrian):
        print("Cruce para arriba")
        x, y = pedestrian.cell.get_coordinates()
        pedestrian.next_cell = self.grid.get(x, y - 1)

    def bottom_cell(self, pedestrian):
        print("Cruce para abajo")
        x, y = pedestrian.cell.get_coordinates()
        pedestrian.next_cell = self.grid.get(x, y + 1)

    def top_or_bottom_cell(self, pedestrian):
        value = generate_random_normalized_value(key1)
        if value >= 0.5:
            self.bottom_cell(pedestrian)
        else:
            self.top_cell(pedestrian)

    def show_grid_state(self):
        print("")
        for j in range(CROSSWALK_HEIGHT_START, CROSSWALK_HEIGHT_LIMIT):
            for i in range(CROSSWALK_WIDTH_START, CROSSWALK_WIDTH_LIMIT):
                print(self.grid.get(i, j).get_symbol(), end="")
            print("")
        print("")
