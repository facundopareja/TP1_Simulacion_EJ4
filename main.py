from constants import (SIMULATION_TIME, key1, key2,DRAW_GRID, MAX_PEDESTRIANS_WAITING)
from grid_manager import GridManager
from util import generate_exponential_value

amount_pedestrians_waiting_right = amount_pedestrians_waiting_left = 0


def get_arrival_times(key, lambda_value):
    """A partir de una llave (para el algoritmo pseudoaleatorio) y un parametro lambda,
    se obtiene una lista de tiempos de llegada para un evento con distribucion exponencial."""
    time = 0
    list_arrival_times = []
    while time <= SIMULATION_TIME:
        number = generate_exponential_value(key, lambda_value)
        time += number
        list_arrival_times.append(time)
    return list_arrival_times


def move_all_entities(green_light, pedestrians_that_crossed, pedestrians_crossed_during_green_light,
                      vehicles, pedestrians, grid_manager, vehicle_conflicts):
    """El movimiento de los autos y transeuntes (ambos cuentan como entidades)
    se realiza en 3 partes: preparacion (prepare_next_move), resolucion de conflictos (resolve_conflict)
     y movimiento (move). Finalmente se eliminan las entidades que ya terminaron de cruzar y se les resetea
     la cantidad de movimientos que pueden realizar (= a velocidad inicial)."""
    global amount_pedestrians_waiting_right, amount_pedestrians_waiting_left
    entities = pedestrians+vehicles
    for entity in entities:
        entity.prepare_next_move(grid_manager, green_light)
    grid_manager.resolve_cell_conflicts()
    for entity in entities:
        entity.move(green_light)
    for pedestrian in pedestrians:
        if pedestrian.done_crossing:
            pedestrians_that_crossed += 1
            if pedestrian.crossed_during_green_light:
                pedestrians_crossed_during_green_light += 1
            pedestrians.remove(pedestrian)
        if pedestrian.waiting():
            if pedestrian.reverse:
                amount_pedestrians_waiting_right += 1
            else:
                amount_pedestrians_waiting_left += 1
    for vehicle in vehicles:
        if vehicle.done_crossing:
            if vehicle.had_conflict():
                vehicle_conflicts += 1
            vehicles.remove(vehicle)
    return pedestrians_that_crossed, pedestrians_crossed_during_green_light, vehicle_conflicts


def is_green_light_on(time, GREEN_LIGHT, RED_LIGHT):
    """Devuelve true o false segun este prendida la luz que permite el paso de los transeuntes o no."""
    cycle_duration = GREEN_LIGHT + RED_LIGHT
    mod_cycle_duration = time % cycle_duration
    if mod_cycle_duration < GREEN_LIGHT:
        return True
    return False


def run_simulation(GREEN_LIGHT, RED_LIGHT, PEDESTRIAN_ARRIVAL_RATE, VEHICLE_ARRIVAL_RATE, alternate_directions=True):
    pedestrian_arrival_times = get_arrival_times(key1, PEDESTRIAN_ARRIVAL_RATE)
    vehicle_arrival_times = get_arrival_times(key2, VEHICLE_ARRIVAL_RATE)
    global amount_pedestrians_waiting_right, amount_pedestrians_waiting_left
    time = 0
    pedestrian_index = 0
    vehicle_index = 0
    pedestrians_to_spawn = 0
    pedestrians_that_crossed = 0
    pedestrians_crossed_during_green_light = 0
    vehicle_conflicts = 0
    pedestrians = []
    vehicles = []
    reverse = False
    grid_manager = GridManager()
    while time < SIMULATION_TIME:
        if DRAW_GRID:
            grid_manager.show_grid_state()
        green_light = is_green_light_on(time, GREEN_LIGHT, RED_LIGHT)
        while time < pedestrian_arrival_times[pedestrian_index] < time + 1:
            pedestrians_to_spawn += 1
            pedestrian_index += 1
        while pedestrians_to_spawn > 0:
            if alternate_directions:
                reverse = not reverse
            if reverse:
                if amount_pedestrians_waiting_left > MAX_PEDESTRIANS_WAITING:
                    break
            else:
                if amount_pedestrians_waiting_right > MAX_PEDESTRIANS_WAITING:
                    break
            pedestrians.append(grid_manager.create_new_pedestrian(green_light, reverse))
            pedestrians_to_spawn -= 1
        while time < vehicle_arrival_times[vehicle_index] < time + 1:
            vehicles.append(grid_manager.create_new_vehicle())
            vehicle_index += 1
        amount_pedestrians_waiting_right = 0
        amount_pedestrians_waiting_left = 0
        pedestrians_that_crossed, pedestrians_crossed_during_green_light, vehicle_conflicts = move_all_entities(green_light,
                                                                                             pedestrians_that_crossed,
                                                                                             pedestrians_crossed_during_green_light,
                                                                                             vehicles, pedestrians, grid_manager,
                                                                                             vehicle_conflicts)
        time += 1
    print(f"En total cruzaron {pedestrians_that_crossed} peatones donde {pedestrians_crossed_during_green_light} cruzaron en verde con "
          f"{vehicle_conflicts} conflictos")
    return pedestrians_crossed_during_green_light, vehicle_conflicts
