from simulation.actions.action import Action


class GameAction(Action):
    @classmethod
    def get_namespace(cls) -> str:
        return "game"
