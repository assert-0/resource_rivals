from simulation.game import Game


class Server:
    def __init__(self):
        self.games = []

    def create_game(self, *args, **kwargs) -> Game:
        game = Game.new_game(*args, **kwargs)
        self.games.append(game)
        return game

    def get_game(self, game_id: str) -> Game:
        for game in self.games:
            if game.id == game_id:
                return game
        raise ValueError(f"Game with id {game_id} not found")

    def delete_game(self, game_id: str) -> None:
        for game in self.games:
            if game.id == game_id:
                self.games.remove(game)
                return
        raise ValueError(f"Game with id {game_id} not found")


server = Server()
