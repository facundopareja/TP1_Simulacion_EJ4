from constants import (SIMULATION_TIME, key1,
                       PEDESTRIAN_ARRIVAL_RATE, VEHICLE_ARRIVAL_RATE,
                       key2, GREEN_LIGHT, RED_LIGHT, DRAW_GRID, MAX_PEDESTRIANS_WAITING)
from grid_manager import GridManager
from util import generate_exponential_value

pedestrians = []
vehicles = []

amount_pedestrians_waiting = 0

grid_manager = GridManager()


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


pedestrian_arrival_times = get_arrival_times(key1, PEDESTRIAN_ARRIVAL_RATE)
vehicle_arrival_times = get_arrival_times(key2, VEHICLE_ARRIVAL_RATE)
pedestrians_that_crossed = 0
vehicles_that_crossed = 0


def move_all_entities(green_light):
    """El movimiento de los autos y transeuntes (ambos cuentan como entidades)
    se realiza en 3 partes: preparacion (prepare_next_move), resolucion de conflictos (resolve_conflict)
     y movimiento (move). Finalmente se eliminan las entidades que ya terminaron de cruzar y se les resetea
     la cantidad de movimientos que pueden realizar (= a velocidad inicial)."""
    global pedestrians_that_crossed, vehicles_that_crossed, amount_pedestrians_waiting
    entities = pedestrians+vehicles
    for entity in entities:
        entity.prepare_next_move(grid_manager, green_light)
    grid_manager.resolve_cell_conflicts()
    for entity in entities:
        entity.move()
    for pedestrian in pedestrians:
        if pedestrian.done_crossing:
            pedestrians_that_crossed += 1
            pedestrians.remove(pedestrian)
        if pedestrian.waiting():
            amount_pedestrians_waiting += 1
    for vehicle in vehicles:
        if vehicle.done_crossing:
            vehicles.remove(vehicle)


def is_green_light_on(time):
    """Devuelve true o false segun este prendida la luz que permite el paso de los transeuntes o no."""
    cycle_duration = GREEN_LIGHT + RED_LIGHT
    mod_cycle_duration = time % cycle_duration
    if mod_cycle_duration < GREEN_LIGHT:
        print("Luz verde")
        return True
    else:
        print("Luz roja")
        return False


def run_simulation():
    global amount_pedestrians_waiting
    time = 0
    pedestrian_index = 0
    vehicle_index = 0
    pedestrians_to_spawn = 0
    reverse = False
    while time < SIMULATION_TIME:
        if time == 50:
            print("hola")
        if time == 200:
            print("hola")
        if DRAW_GRID:
            grid_manager.show_grid_state()
        print(f"Pasaron {time} segundos")
        green_light = is_green_light_on(time)
        while time < pedestrian_arrival_times[pedestrian_index] < time + 1:
            pedestrians_to_spawn += 1
            pedestrian_index += 1
        while pedestrians_to_spawn > 0 and amount_pedestrians_waiting <= 200:
            pedestrians.append(grid_manager.create_new_pedestrian(green_light, reverse))
            pedestrians_to_spawn -= 1
        while time < vehicle_arrival_times[vehicle_index] < time + 1:
            vehicles.append(grid_manager.create_new_vehicle())
            vehicle_index += 1
        amount_pedestrians_waiting = 0
        move_all_entities(green_light)
        time += 1
    print(f"En total cruzaron {pedestrians_that_crossed} peatones")


run_simulation()
