from typing import List

from entities.dynamic.buildings.building import Building
from entities.dynamic.buildings.resource_collectors.farm import Farm
from entities.dynamic.buildings.resource_collectors.miner import Miner
from entities.dynamic.buildings.resource_collectors.sawmill import Sawmill
from entities.dynamic.units.unit import Unit
from entities.entity import ConcreteEntity, Entity
from entities.static.resources.food import Food
from entities.static.resources.mineral import Mineral
from entities.static.resources.wood import Wood


def get_all_other_buildings() -> List[Building]:
    from utils.registry import registry

    found_buildings = []

    for key, module in registry.modules.items():
        if key.startswith("buildings") and "resource_collectors" not in key:
            found_buildings.append(module)

    return found_buildings


RESOURCE_TO_COLLECTOR_MAPPING = {
    Wood: Sawmill,
    Food: Farm,
    Mineral: Miner,
}

ALL_OTHER_BUILDINGS = get_all_other_buildings()


class Worker(Unit, ConcreteEntity):
    def calculate_available_buildings(
            self, current_sector: List[Entity], _map
    ) -> List[List[str]]:  # (namespace, type) tuples
        resource_buildings = []
        other_buildings = []

        for entity in current_sector:
            if entity.__class__ in RESOURCE_TO_COLLECTOR_MAPPING:
                resource_buildings.append(
                    RESOURCE_TO_COLLECTOR_MAPPING[entity.__class__]
                )

        if (
                _map.influence[self.position.x][self.position.y] == self.teamId
                and len(current_sector) == 1
        ):
            other_buildings = ALL_OTHER_BUILDINGS

        return [
            [building.get_namespace(), building.get_type()]
            for building in resource_buildings + other_buildings
        ]

    def build(self, namespace: str, type: str, _map) -> None:
        from utils.registry import registry

        building = registry.get(type, namespace)
        building = building(
            position=self.position, teamId=self.teamId,
        )

        _map.add_entity(building)
        _map.remove_entity(self)
