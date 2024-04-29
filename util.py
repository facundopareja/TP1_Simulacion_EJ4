import pyarrow as pa
import warnings
import numpy as np

from constants import key1, LENGTH

counter = pa.scalar(0, type=pa.uint64())


def next_round(x, addition):
    x = pa.compute.add(pa.compute.multiply(x, x), addition)
    shift_right = pa.compute.shift_right(x, pa.scalar(32, type=pa.uint64()))
    shift_left = pa.compute.shift_left(x, pa.scalar(32, type=pa.uint64()))
    return pa.compute.bit_wise_or(shift_right, shift_left)


def squares_rng(counter, key):
    """
    Generates a pseudo-random 32-bit number using a squares rng algorithm based on given `counter` and `key`.

    Args:
        counter (np.uint64): Current counter value used in the random number generation.
        key (np.uint64): Key value influencing the randomness.

    Returns:
        np.uint32: Pseudo-random 32-bit number generated from the input `counter` and `key`.
    """
    x = pa.uint64()
    y = pa.uint64()
    z = pa.uint64()
    x = pa.compute.multiply(counter, key)
    y = pa.compute.multiply(counter, key)
    z = pa.compute.add(y, key)
    x = next_round(x, y)
    x = next_round(x, z)
    x = next_round(x, y)
    x = pa.compute.shift_right(pa.compute.add(pa.compute.multiply(x, x), z), pa.scalar(32, type=pa.uint64()))
    return pa.compute.cast(x, pa.uint32())


def generate_random_normalized_value(key):
    """
    Generates a batch of random values based on the specified `size` and `key`.

    Args:
        size (int): Number of random values to generate.
        key (int): Key value used for randomness generation.

    Returns:
        np.array: Array of random values of length `size`, normalized to [0, 1].
    """

    with warnings.catch_warnings():
        global counter
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        key = pa.scalar(key, type=pa.uint64())
        max_32_bit_value = 4294967295
        random_number = squares_rng(counter, key)
        counter = pa.compute.add(counter, pa.scalar(1, type=pa.uint64()))
        return random_number.as_py() / max_32_bit_value


def generate_exponential_value(key, lambda_value):
    random_value = generate_random_normalized_value(key)
    return (-1 / lambda_value) * np.log(1 - random_value)


def get_random_speed():
    value = generate_random_normalized_value(key1)
    if value > 0.978:
        return 6
    elif 0.978 >= value > 0.93:
        return 5
    elif 0.93 >= value > 0.793:
        return 4
    elif 0.793 >= value > 0.273:
        return 3
    return 2


def get_random_y_position():
    value = generate_random_normalized_value(key1)
    value *= LENGTH
    return int(value+1)


def cells_are_free(cells):
    for cell in cells:
        if cell.occupied():
            return False
    return True


def cells_are_waiting_cells(cells):
    for cell in cells:
        if not cell.waiting():
            return False
    return True
