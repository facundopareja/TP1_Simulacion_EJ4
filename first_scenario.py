from main import run_simulation
import numpy as np
import matplotlib.pyplot as plt


def first_scenario():
    GREEN_LIGHT = 25
    RED_LIGHT = 90 - GREEN_LIGHT
    HOUR = 3600
    pedestrian_arrival_rates = []
    for i in range(500, 5500, 500):
        pedestrian_arrival_rates.append(i / HOUR)
    vehicle_arrival_rates = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12]
    results = []
    for VEHICLE_ARRIVAL_RATE in vehicle_arrival_rates:
        for PEDESTRIAN_ARRIVAL_RATE in pedestrian_arrival_rates:
            print(f"For {VEHICLE_ARRIVAL_RATE} vehicle arrival rate and {PEDESTRIAN_ARRIVAL_RATE} pedestrian arrival "
                  f"rate:")
            results.append(run_simulation(GREEN_LIGHT, RED_LIGHT, PEDESTRIAN_ARRIVAL_RATE, VEHICLE_ARRIVAL_RATE))
    results = np.array(results)
    pedestrian_arrival_rates = np.array(pedestrian_arrival_rates)
    i = 0
    j = 0
    while i < len(results):
        values = results[i:i + len(pedestrian_arrival_rates)]
        plt.plot(np.array(pedestrian_arrival_rates), np.array(values))
        plt.title(f"Pedestrian arrival rate vs Pedestrians who cross on green light for "
                  f"{vehicle_arrival_rates[j]} vehicle arrival rate ", fontsize=8)
        plt.show()
        i += len(pedestrian_arrival_rates)
        j += 1


first_scenario()
