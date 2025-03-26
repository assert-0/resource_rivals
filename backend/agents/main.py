from random import randint

from agents.game_environment import GameEnv


if __name__ == "__main__":
    env = GameEnv()
    obs, _ = env.reset()
    done = False
    total_reward = 0.0

    while not done:
        # For demonstration, choose a random valid action.
        # (In practice your agent would decide the action.)
        if obs["reachable_moves"]:
            action = randint(0, len(obs["reachable_moves"]) - 1)
        else:
            action = 0
        obs, reward, done, out_of_bounds, info = env.step(action)
        total_reward += reward
        env.render()
        print("====================================")
        print(env.current_step)
        print("====================================")

    print(
        f"Episode finished after {env.current_step} steps, "
        f"total reward: {total_reward}"
    )
