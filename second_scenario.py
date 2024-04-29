import numpy as np
from matplotlib import pyplot as plt

from main import run_simulation


def second_scenario():
    green_lights = [25, 30, 35, 40, 45, 50]
    CYCLE_TIME = 90
    HOUR = 3600
    pedestrian_arrival_rates = [2000/HOUR, 4000/HOUR, 6000/HOUR]
    vehicle_arrival_rates = [0.17, 0.28, 0.39]
    results = []
    x = []
    y = []
    for GREEN_LIGHT in green_lights:
        for VEHICLE_ARRIVAL_RATE in vehicle_arrival_rates:
            for PEDESTRIAN_ARRIVAL_RATE in pedestrian_arrival_rates:
                print(f"Para {VEHICLE_ARRIVAL_RATE} vehicle arrival rate and {PEDESTRIAN_ARRIVAL_RATE} pedestrian arrival "
                      f"rate with {GREEN_LIGHT}s green light timing")
                pedestrian_times, vehicle_conflicts = run_simulation(GREEN_LIGHT,
                                                                     CYCLE_TIME - GREEN_LIGHT,
                                                                     PEDESTRIAN_ARRIVAL_RATE,
                                                                     VEHICLE_ARRIVAL_RATE)
                y.append(VEHICLE_ARRIVAL_RATE)
                x.append(PEDESTRIAN_ARRIVAL_RATE)
                results.append(vehicle_conflicts)
        results = np.array(results)
        ax = plt.axes(projection='3d')
        ax.set_title(f"PA lambda x VA lambda x Number of conflicts for {GREEN_LIGHT}s GL")
        ax.set_xlabel('Pedestrian arrival lambda')
        ax.set_ylabel('Vehicle arrival lambda')
        ax.set_zlabel('Number of conflicts')
        ax.scatter3D(x, y, results)
        plt.show()
        x = []
        y = []
        results = []


second_scenario()
