from entities.entity import Entity


class Resource(Entity):
    @classmethod
    def get_namespace(cls) -> str:
        return "resources"
