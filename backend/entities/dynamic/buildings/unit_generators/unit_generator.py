from entities.entity import Entity


class UnitGenerator(Entity):
    @classmethod
    def get_namespace(cls) -> str:
        return "buildings/unit_generators"
