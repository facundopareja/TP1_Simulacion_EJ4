from constants import key1
from util import generate_random_normalized_value


class Square:
    def __init__(self):
        self.occupant = None
        self.possible_occupants = []

    def attempt_to_occupy(self, occupant):
        """Agrega a occupant a la lista de posibles ocupantes, para decidir ganador mas tarde."""
        if self.occupant is not None:
            return
        self.possible_occupants.append(occupant)

    def vacate(self, previous_occupant):
        """Elimina el ocupante de la celda si coincide con el parametro recibido."""
        if previous_occupant == self.occupant:
            self.occupant = None

    def resolve_conflict(self):
        """Decide un ganador de todos los posibles."""
        if len(self.possible_occupants) == 0 or self.occupied():
            return
        winner_index = int(len(self.possible_occupants) * generate_random_normalized_value(key1))
        self.occupant = self.possible_occupants[winner_index]
        self.possible_occupants = []

    def compare_speeds(self, speed):
        """Devuelve True si la velocidad recibida es mayor que la del ocupante actual.
        False si no.."""
        return speed > self.occupant.speed

    def occupied(self):
        return self.occupant is not None

    def won(self, occupant):
        return occupant == self.occupant

    def get_symbol(self):
        if self.occupant is None:
            return "Ø"
        return self.occupant.get_symbol()
