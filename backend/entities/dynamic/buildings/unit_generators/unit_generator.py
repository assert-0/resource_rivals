from typing import Type, Optional

from entities.dynamic.units.unit import Unit
from entities.entity import Entity


class UnitGenerator(Entity):
    @classmethod
    def get_namespace(cls) -> str:
        return "buildings/unit_generators"
