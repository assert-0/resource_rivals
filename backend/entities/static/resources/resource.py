from consts import TEAMS_NEUTRAL_ID
from entities.entity import Entity


class Resource(Entity):
    teamId: str = TEAMS_NEUTRAL_ID

    @classmethod
    def get_namespace(cls) -> str:
        return "resources"
