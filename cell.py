from constants import key1, CROSSWALK_WIDTH_START, CROSSWALK_WIDTH_LIMIT, CROSSWALK_WIDTH, CROSSWALK_HEIGHT_LIMIT
from util import generate_random_normalized_value


class Cell:
    def __init__(self, x, y, waiting_cell):
        self.occupant = None
        self.x = x
        self.y = y
        self.waiting_cell = waiting_cell
        self.possible_occupants = []
        self.multiple_occupants = []

    def attempt_to_occupy(self, occupant):
        if self.waiting_cell:
            return
        """Agrega a occupant a la lista de posibles ocupantes, para decidir ganador mas tarde."""
        if self.occupant is not None or self.occupant == occupant:
            return
        self.possible_occupants.append(occupant)

    def vacate(self, previous_occupant):
        """Elimina el ocupante de la celda si coincide con el parametro recibido."""
        if self.waiting_cell:
            return
        if previous_occupant == self.occupant:
            self.occupant = None

    def resolve_conflict(self):
        """Decide un ganador de todos los posibles."""
        if len(self.possible_occupants) == 0 or self.occupied() or self.waiting_cell:
            return
        winner_index = int(len(self.possible_occupants) * generate_random_normalized_value(key1))
        self.occupant = self.possible_occupants[winner_index]
        self.possible_occupants = []

    def faster(self, speed):
        """Devuelve True si la velocidad recibida es mayor que la del ocupante actual.
        False si no."""
        return speed > self.occupant.speed

    def right_edge(self):
        return self.x == CROSSWALK_WIDTH_LIMIT

    def left_edge(self):
        return self.x == CROSSWALK_WIDTH_START-1

    def bottom(self):
        return self.y == CROSSWALK_HEIGHT_LIMIT

    def occupied(self):
        if self.waiting_cell:
            return False
        return self.occupant is not None

    def won(self, occupant):
        if self.waiting_cell:
            return True
        return occupant == self.occupant

    def get_coordinates(self):
        return self.x, self.y

    def same_direction(self, direction):
        return self.occupant.same_direction(direction)

    def get_symbol(self):
        if self.occupant is None:
            return "Ø"
        return self.occupant.get_symbol()

    def waiting(self):
        return self.waiting_cell

    def get_occupant_color(self):
        if self.occupant is None:
            return "white"
        return self.occupant.get_color()
