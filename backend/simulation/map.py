from typing import List, Optional, Set, Collection, Dict

from entities.entity import Entity
from utils.model_serde import ModelSerde
from utils.observer import Observable, ObserverEvent


class Map(Observable):
    sectors: List[List[List[Entity]]]
    entities: Dict[str, Entity]

    def add_entity(self, entity: Entity):
        entity = entity.model_copy(deep=True)

        self.entities[entity.id] = entity
        self.sectors[entity.position.x][entity.position.y].append(entity)
        self.notify_observers(  # type: ignore
            entity, event=ObserverEvent.ADDED
        )

    def remove_entity(self, entity: Entity):
        self.expect_entity_by_id(entity.id)

        del self.entities[entity.id]
        self.sectors[entity.position.x][entity.position.y].remove(entity)
        self.notify_observers(  # type: ignore
            entity, event=ObserverEvent.REMOVED
        )

    def update_entity(self, entity: Entity):
        old_entity = self.expect_entity_by_id(entity.id)
        entity = entity.model_copy(deep=True)

        if old_entity == entity:
            return

        self.sectors[old_entity.position.x][old_entity.position.y].remove(
            old_entity
        )

        self.entities[entity.id] = entity
        self.sectors[entity.position.x][entity.position.y].append(entity)
        self.notify_observers(  # type: ignore
            entity, event=ObserverEvent.UPDATED
        )

    def get_entities_at_position(self, x: int, y: int) -> List[Entity]:
        return [entity.model_copy(deep=True) for entity in self.sectors[x][y]]

    def get_entity_by_id(self, _id: str) -> Optional[Entity]:
        entity = self.entities.get(_id, None)
        if entity is None:
            return None
        return entity.model_copy(deep=True)

    def expect_entity_by_id(self, _id: str) -> Entity:
        entity = self.get_entity_by_id(_id)
        if entity is None:
            raise ValueError(f"Entity with id '{_id}' not found in map")
        return entity

    def add_entities(self, entities: Collection[Entity]):
        for entity in entities:
            self.add_entity(entity)

    def remove_entities(self, entities: Collection[Entity]):
        for entity in entities:
            self.remove_entity(entity)

    def update_entities(self, entities: Collection[Entity]):
        for entity in entities:
            self.update_entity(entity)

    def get_entities(self) -> Set[Entity]:
        return {
            entity.model_copy(deep=True) for entity in self.entities.values()
        }

    def get_entities_by_team(self, team_id: str) -> Set[Entity]:
        return {
            entity.model_copy(deep=True) for entity in self.entities.values()
            if entity.teamId == team_id
        }

    @staticmethod
    def from_entities(entities: Collection[Entity], w: int, h: int) -> 'Map':
        sectors: List[List[List[Entity]]] = [
            [[] for _ in range(h)] for _ in range(w)
        ]
        for entity in entities:
            sectors[entity.position.x][entity.position.y].append(entity)

        entities_map = {entity.id: entity for entity in entities}

        return Map(sectors=sectors, entities=entities_map)  # type: ignore

    @staticmethod
    def from_file(file_path: str) -> 'Map':
        tree = ModelSerde.load_model(Map, file_path)

        return tree