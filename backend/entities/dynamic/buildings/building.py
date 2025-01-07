from typing import List, Type, Optional

from entities.dynamic.units.unit import Unit
from entities.entity import Entity
from utils.math import Point


class Building(Entity):
    def calculate_influence(
            self,
            sectors: List[List[List['Entity']]],
            influence: List[List[str]],
    ) -> List[Point]:
        return []

    @classmethod
    def get_namespace(cls) -> str:
        return "buildings"

    def generate_unit(self, game, unit_type: Type[Unit]) -> None:
        if self._can_generate_unit(game):
            game.map.add_entity(
                unit_type(
                    position=self.position,
                    teamId=self.teamId,
                )
            )

    def upgrade_unit(
            self, game, source_type: Type[Unit], target_type: Type[Unit]
    ) -> None:
        if unit := self._contains_unit(game, source_type):
            game.map.remove_entity(unit)
            self.generate_unit(game, target_type)

    def _can_generate_unit(self, game) -> bool:
        current_sector = game.map.sectors[self.position.x][self.position.y]
        current_population = game.teams[self.teamId].get_current_population()
        max_population = game.teams[self.teamId].maxPopulation
        return len(current_sector) == 1 and current_population < max_population

    def _contains_unit(self, game, unit_type: Type[Unit]) -> Optional[Unit]:
        for entity in game.map.sectors[self.position.x][self.position.y]:
            if isinstance(entity, unit_type):
                return entity
        return None
