from entities.dynamic.buildings.building import Building
from entities.dynamic.units.worker import Worker
from entities.entity import ConcreteEntity


class Capital(Building, ConcreteEntity):
    def on_turn_end(self, game) -> None:
        super().on_turn_end(game)
        self.generate_unit(game, Worker)
