from grids import Grid

from constants import (SIMULATION_TIME, CROSSWALK_WIDTH,
                       CROSSWALK_HEIGHT, key1,
                       PEDESTRIAN_ARRIVAL_RATE, VEHICLE_ARRIVAL_RATE,
                       key2, GREEN_LIGHT, RED_LIGHT)
from pedestrian import Pedestrian
from square import Square
from util import generate_exponential_value, show_grid_state
from vehicle import Vehicle

pedestrians = []
vehicles = []

grid = Grid(CROSSWALK_WIDTH, CROSSWALK_HEIGHT)

for j in range(1, CROSSWALK_HEIGHT + 1):
    for i in range(1, CROSSWALK_WIDTH + 1):
        grid.update_cell(i, j, Square())


def get_arrival_times(key, lambda_value):
    time = 0
    list_arrival_times = []
    while time <= SIMULATION_TIME:
        number = generate_exponential_value(key, lambda_value)
        time += number
        list_arrival_times.append(time)
    return list_arrival_times


pedestrian_arrival_times = get_arrival_times(key1, PEDESTRIAN_ARRIVAL_RATE)
vehicle_arrival_times = get_arrival_times(key2, VEHICLE_ARRIVAL_RATE)


def move_all_entities(green_light):
    entities = pedestrians + vehicles
    finished_entities = 0
    while finished_entities < len(entities):
        for entity in entities:
            entity.prepare_next_move(grid, green_light)
        for column in grid:
            for cell in column:
                cell.resolve_conflict()
        finished_entities = 0
        for entity in entities:
            entity.move(grid)
            if entity.done_moving():
                finished_entities += 1
        show_grid_state(grid)
    for entity in entities:
        entity.reset_movement()
    for pedestrian in pedestrians:
        if pedestrian.done_crossing:
            pedestrians.remove(pedestrian)
    for vehicle in vehicles:
        if vehicle.done_crossing:
            vehicles.remove(vehicle)


def is_green_light_on(time):
    cycle_duration = GREEN_LIGHT + RED_LIGHT
    mod_cycle_duration = time % cycle_duration
    if mod_cycle_duration < GREEN_LIGHT:
        return True
    return False


vehicles.append(Vehicle(1, 0))


def run_simulation():
    pedestrian_starting_position = 1
    vehicle_starting_lane = 1
    time = 0
    while time < SIMULATION_TIME:
        green_light = is_green_light_on(time)
        for arrival_time in pedestrian_arrival_times:
            if time < arrival_time < time + 1:
                pedestrians.append(Pedestrian(0, pedestrian_starting_position))
                pedestrian_starting_position += 1
                if pedestrian_starting_position > CROSSWALK_HEIGHT:
                    pedestrian_starting_position = 1
        for arrival_time in vehicle_arrival_times:
            if time < arrival_time < time + 1:
                pass
                # vehicles.append(Vehicle(vehicle_starting_lane, 0))
                # vehicle_starting_lane += (VEHICLE_WIDTH+1)
                # if vehicle_starting_lane > CROSSWALK_WIDTH:
                #     vehicle_starting_lane = 1
        move_all_entities(green_light)
        time += 1


run_simulation()

# for arrival_time in vehicle_arrival_times:
#     if t < arrival_time < t + 1:
#         pass
#         vehicles.append(Vehicle(0, 0, 5))
