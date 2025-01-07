from entities.entity import Entity


class ResourceCollector(Entity):
    @classmethod
    def get_namespace(cls) -> str:
        return "buildings/resource_collectors"
