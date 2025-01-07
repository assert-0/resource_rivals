import logging

TEAMS_NEUTRAL_ID = "neutral"
TEAMS_STARTING_POPULATION = 5

UNITS_CONFIG = {
    "Worker": {
        "health": 5,
        "armor": 0,
        "damage": 0,
        "movementRange": 1,
        "attackRange": 0,
    },
    "Soldier": {
        "health": 10,
        "armor": 1,
        "damage": 2,
        "movementRange": 2,
        "attackRange": 1
    },
    "AdvancedSoldier": {
        "health": 15,
        "armor": 2,
        "damage": 3,
        "movementRange": 2,
        "attackRange": 1
    },
    "Ranged": {
        "health": 7,
        "armor": 0,
        "damage": 2,
        "movementRange": 1,
        "attackRange": 2
    },
    "AdvancedRanged": {
        "health": 10,
        "armor": 1,
        "damage": 3,
        "movementRange": 1,
        "attackRange": 3
    },
    "Tank": {
        "health": 15,
        "armor": 3,
        "damage": 2,
        "movementRange": 1,
        "attackRange": 1
    },
    "AdvancedTank": {
        "health": 20,
        "armor": 4,
        "damage": 3,
        "movementRange": 1,
        "attackRange": 2
    },
    "Scout": {
        "health": 3,
        "armor": 0,
        "damage": 1,
        "movementRange": 3,
        "attackRange": 1
    },
    "Calvary": {
        "health": 10,
        "armor": 1,
        "damage": 2,
        "movementRange": 2,
        "attackRange": 1
    },
}

REGISTRY_SEARCH_PATHS = [
    "entities/dynamic", "entities/static", "simulation/actions"
]
REGISTRY_BASE_CLASSES = [
    "entities.entity.ConcreteEntity",
    "simulation.actions.action.ConcreteAction"
]

LOG_LEVEL = logging.DEBUG
