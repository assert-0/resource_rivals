from typing import List, Optional, Set, Collection

from pydantic import BaseModel

from entities.entity import Entity
from observer import Observable, ObserverEvent


class Map(BaseModel, Observable):
    sectors: List[List[Optional[Entity]]]
    entities: Set[Entity]

    def add_entity(self, entity: Entity):
        self.entities.add(entity)
        self.sectors[entity.x][entity.y] = entity
        self.notify_observers(entity, event=ObserverEvent.ADDED)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)
        self.sectors[entity.x][entity.y] = None
        self.notify_observers(entity, event=ObserverEvent.REMOVED)

    def update_entity(self, entity: Entity, x: int, y: int):
        self.sectors[entity.x][entity.y] = None
        self.sectors[entity.x][entity.y] = entity
        self.notify_observers(entity, event=ObserverEvent.UPDATED)

    def get_entity(self, x: int, y: int) -> Optional[Entity]:
        return self.sectors[x][y]

    @staticmethod
    def from_entities(entities: Collection[Entity], w: int, h: int) -> 'Map':
        sectors = [[None for _ in range(h)] for _ in range(w)]
        for entity in entities:
            sectors[entity.x][entity.y] = entity
        return Map(sectors=sectors, entities=entities)
