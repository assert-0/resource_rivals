from typing import Set
from uuid import uuid4

from pydantic import BaseModel, Field

from consts import TEAMS_STARTING_POPULATION
from entities.dynamic.units.unit import Unit
from simulation.map import Map
from utils.math import Point


class Resources(BaseModel):
    food: int = 0
    wood: int = 0
    minerals: int = 0


class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    visibleArea: Set[Point] = Field(default_factory=set)
    resources: Resources = Resources()
    maxPopulation: int = TEAMS_STARTING_POPULATION

    def get_current_population(self, _map: Map) -> int:
        population = 0
        for entity in _map.get_entities_by_team(self.id):
            if isinstance(entity, Unit):
                population += 1

        return population
