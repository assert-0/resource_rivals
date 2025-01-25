from typing import List

from entities.dynamic.buildings.building import Building
from entities.dynamic.buildings.resource_collectors.farm import Farm
from entities.dynamic.buildings.resource_collectors.miner import Miner
from entities.dynamic.buildings.resource_collectors.sawmill import Sawmill
from entities.dynamic.units.unit import Unit
from entities.entity import ConcreteEntity
from entities.static.resources.food import Food
from entities.static.resources.mineral import Mineral
from entities.static.resources.wood import Wood
from simulation.team import Resources


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


class Worker(Unit, ConcreteEntity):
    def calculate_available_buildings(
            self, game
    ) -> List[List[str]]:  # (namespace, type) tuples
        resource_buildings = []
        other_buildings = []

        current_sector = game.map.sectors[self.position.y][self.position.x]

        for entity in current_sector:
            if entity.__class__ in RESOURCE_TO_COLLECTOR_MAPPING:
                resource_buildings.append(
                    RESOURCE_TO_COLLECTOR_MAPPING[entity.__class__]
                )

        if (
                game.map.influence[self.position.y][self.position.x]
                == self.teamId
                and len(current_sector) == 1
        ):
            other_buildings = get_all_other_buildings()

        return [
            [building.get_namespace(), building.get_type()]
            for building in resource_buildings + other_buildings
        ]

    def build(self, namespace: str, type: str, game) -> Building:
        from utils.registry import registry

        building_cls = registry.get(type, namespace)
        building_instance = building_cls(
            position=self.position, teamId=self.teamId,
        )

        if [namespace, type] not in self.calculate_available_buildings(game):
            raise ValueError("Building not allowed to be built here")

        cost = Resources(
            food=building_instance.cost[0],  # type: ignore
            wood=building_instance.cost[1],  # type: ignore
            minerals=building_instance.cost[2],  # type: ignore
        )

        if game.teams[self.teamId].resources.can_afford(cost):
            game.teams[self.teamId].resources.pay(cost)

            game.map.add_entity(building_instance)
            game.map.remove_entity(self)
        else:
            raise ValueError("Not enough resources to build")

        return building_instance  # type: ignore
