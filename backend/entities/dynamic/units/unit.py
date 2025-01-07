from typing import List, Set

from pydantic import Field

from consts import UNITS_CONFIG
from entities.entity import Entity
from entities.static.obstacles.obstacle import Obstacle
from utils.math import Point


class Unit(Entity):
    health: int
    armor: int
    damage: int
    movementRange: int
    attackRange: int

    def __init__(self, **kwargs):
        kwargs['health'] = self.get_health()
        kwargs['armor'] = self.get_armor()
        kwargs['damage'] = self.get_damage()
        kwargs['movementRange'] = self.get_movement_range()
        kwargs['attackRange'] = self.get_attack_range()

        super().__init__(**kwargs)

    def act(self, target_position: Point, _map) -> None:
        target_sector = _map.sectors[target_position.x][target_position.y]
        target = None

        for entity in target_sector:
            if isinstance(entity, Unit) and entity.teamId != self.teamId:
                target = entity
                break

        if target is None:
            self.move(target_position, _map)
        else:
            self.attack(target, _map)

    def attack(self, target: 'Unit', _map) -> None:
        if not self._check_in_attack_range(target.position):
            raise ValueError("Target is out of range")

        if self.teamId == target.teamId:
            raise ValueError("Cannot attack friendly units")

        target._defend(self, self.damage)
        if target.health <= 0:
            _map.remove_entity(target)
        else:
            _map.update_entity(target)

        if self.health <= 0:
            _map.remove_entity(self)
        else:
            _map.update_entity(self)

    def move(self, target: Point, _map) -> None:
        if target not in self.calculate_reachable_sectors(_map.sectors):
            raise ValueError("Target is out of range")

        self.position = target
        _map.update_entity(self)

    def calculate_reachable_sectors(
            self, game
    ) -> List[Point]:
        movable_sectors = []
        attackable_sectors = []

        sectors = game.map.sectors

        for i, row in enumerate(sectors):
            for j, sector in enumerate(row):
                if (
                        self._check_in_movement_range(Point(i, j))
                        and self._sector_free(sectors[i][j])
                ):
                    movable_sectors.append(Point(i, j))

        for i, row in enumerate(sectors):
            for j, sector in enumerate(row):
                if (
                        self._check_in_attack_range(Point(i, j))
                        and self._contains_enemy_unit(sectors[i][j])
                ):
                    attackable_sectors.append(Point(i, j))

        return movable_sectors + attackable_sectors

    def calculate_visible_area(self) -> Set[Point]:
        visible_sectors = set()

        for i in range(
                self.position.x - self.attackRange,
                self.position.x + self.attackRange + 1
        ):
            for j in range(
                    self.position.y - self.attackRange,
                    self.position.y + self.attackRange + 1
            ):
                visible_sectors.add(Point(i, j))

        return visible_sectors

    def get_health(self) -> int:
        return UNITS_CONFIG[self.__class__.__name__]['health']

    def get_armor(self) -> int:
        return UNITS_CONFIG[self.__class__.__name__]['armor']

    def get_damage(self) -> int:
        return UNITS_CONFIG[self.__class__.__name__]['damage']

    def get_movement_range(self) -> int:
        return UNITS_CONFIG[self.__class__.__name__]['movementRange']

    def get_attack_range(self) -> int:
        return UNITS_CONFIG[self.__class__.__name__]['attackRange']

    def calculate_available_buildings(
            self, game
    ) -> List[List[str]]:  # (namespace, type) tuples
        return []

    def _defend(self, attacker: 'Unit', damage: int) -> None:
        self._hurt(damage)

        if self.health > 0:
            if self._check_in_attack_range(attacker.position):
                attacker._hurt(self.damage)

    def _hurt(self, damage: int) -> None:
        self.health -= max(damage - self.armor, 0)

    def _check_in_attack_range(self, target: Point) -> bool:
        if (
                abs(self.position.x - target.x) <= self.attackRange
                and abs(self.position.y - target.y) <= self.attackRange
        ):
            return True

        return False

    def _check_in_movement_range(self, target: Point) -> bool:
        if (
                abs(self.position.x - target.x) <= self.movementRange
                and abs(self.position.y - target.y) <= self.movementRange
        ):
            return True

        return False

    def _sector_free(self, sector: List[Entity]) -> bool:
        for entity in sector:
            if isinstance(entity, Obstacle) or isinstance(entity, Unit):
                return False

        return True

    def _contains_enemy_unit(self, sector: List[Entity]) -> bool:
        for entity in sector:
            if isinstance(entity, Unit) and entity.teamId != self.teamId:
                return True

        return False

    @classmethod
    def get_namespace(cls) -> str:
        return "units"
