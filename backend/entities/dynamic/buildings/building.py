from entities.entity import Entity


class Building(Entity):
    @classmethod
    def get_namespace(cls) -> str:
        return "buildings"
