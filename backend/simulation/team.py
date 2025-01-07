from typing import Set, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from consts import TEAMS_STARTING_POPULATION
from entities.dynamic.units.unit import Unit
from entities.entity import Entity
from simulation.map import Map
from utils.math import Point


class Resources(BaseModel):
    food: int = 0
    wood: int = 0
    minerals: int = 0

    def can_afford(self, cost: "Resources") -> bool:
        return all(
            getattr(self, resource) >= getattr(cost, resource)
            for resource in self.model_fields.keys()
        )

    def pay(self, cost: "Resources") -> None:
        if not self.can_afford(cost):
            raise ValueError("Not enough resources")

        for resource in self.model_fields.keys():
            setattr(
                self, resource,
                getattr(self, resource) - getattr(cost, resource)
            )


class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    visibleArea: Set[Point] = Field(default_factory=set)
    resources: Resources = Resources()
    maxPopulation: int = TEAMS_STARTING_POPULATION
    isDefeated: bool = False

    def get_current_population(self, _map: Map) -> int:
        population = 0
        for entity in _map.get_entities_by_team(self.id):
            if isinstance(entity, Unit):
                population += 1

        return population

    def recalculate_visible_area(self, _map: Map) -> None:
        for entity in _map.get_entities_by_team(self.id):
            if isinstance(entity, Unit):
                self.visibleArea.update(entity.get_visible_area(_map))

    def get_visible_map(self, _map: Map) -> List[List[Optional[List[Entity]]]]:
        visible_map = _map.model_copy(deep=True)

        for x in range(visible_map.width):
            for y in range(visible_map.height):
                if Point(x, y) not in self.visibleArea:
                    visible_map.sectors[x][y] = None

        return visible_map.sectors
