import logging

TEAMS_NEUTRAL_ID = "neutral"

REGISTRY_SEARCH_PATHS = [
    "entities/dynamic", "entities/static", "simulation/actions"
]
REGISTRY_BASE_CLASSES = [
    "entities.entity.ConcreteEntity",
    "simulation.actions.action.ConcreteAction"
]

LOG_LEVEL = logging.DEBUG
