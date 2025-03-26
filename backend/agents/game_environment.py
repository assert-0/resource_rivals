from gymnasium import Env


class GameEnvironment(Env):
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 0

    def step(self, action):
        self.state += 1
        return self.state, 0, False, {}

    def render(self):
        print(f"Current state: {self.state}")
