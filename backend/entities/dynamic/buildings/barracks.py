from typing import List

from pydantic import Field

from consts import BUILDING_COSTS
from entities.dynamic.buildings.building import Building
from entities.entity import ConcreteEntity


class Barracks(Building, ConcreteEntity):
    pass
