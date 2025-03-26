from typing import Optional, Tuple, List

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

from client.client import Client
from consts import TEAMS_NEUTRAL_ID
from entities.entity import Entity
from simulation.consts import GameStates
from simulation.game import Game
from utils.math import Point


class GameEnv(gym.Env):
    """
    A simple Gym environment that uses the provided turn-based game client.
    The agent controls one team; on its turn it selects a reachable move for
    a worker unit.
    After the agent's move, the environment simulates an opponent turn with
    a random policy.
    """

    def __init__(self, max_steps: int = 100):
        super(GameEnv, self).__init__()
        self.client = Client()
        self.max_steps = max_steps
        self.current_step = 0

        # For simplicity, we define dummy observation and action spaces.
        # The observation is a dict containing a "visible_map"
        # (a list of lists of strings)
        # and "reachable_moves" (a list of (x, y) tuples).
        # The action is an integer index into the reachable moves list.
        self.observation_space = spaces.Dict({
            "visible_map": spaces.Box(low=0, high=255, shape=(8, 8, 8),
                                      dtype=np.uint8),
            "reachable_moves": spaces.Box(low=0, high=100, shape=(64, 2),
                                          dtype=np.uint8)
        })
        self.action_space = spaces.Discrete(64)
        self.game: Optional[Game] = None
        self.agent_team_id: Optional[str] = None
        self.opponent_team_id: Optional[str] = None

    def reset(self, *_, **kwargs) -> tuple:
        """Resets the environment and returns the initial observation."""

        super().reset(**kwargs)

        self.current_step = 0
        self.game = self.client.game_create("example_full")
        game_id = self.game.id

        agent_team = self.client.team_create(game_id, "Agent Team")
        opponent_team = self.client.team_create(game_id, "Opponent Team")
        self.agent_team_id = agent_team.id
        self.opponent_team_id = opponent_team.id

        self.client.game_start(game_id)

        game_info = self.client.game_get_info(game_id)
        if game_info.activeTeamId == self.opponent_team_id:
            self._simulate_opponent_turn()

        return self._get_observation(), {}

    def step(self, action: int) -> Tuple[dict, float, bool, bool, dict]:
        """
        Applies the agent's action.

        The action is an integer index into the list of reachable moves
        (for the first worker unit found).
        Returns a tuple (observation, reward, done, info).
        """

        assert self.game is not None
        assert self.agent_team_id is not None
        assert self.opponent_team_id is not None

        game_id = self.game.id

        visible_map = self.client.team_get_visible_map(
            game_id,
            self.agent_team_id
        )
        available_workers = self._find_available_workers(
            visible_map, self.agent_team_id
        )

        if not available_workers:
            done = False
            out_of_bounds = True
            return (
                self._get_observation(),
                -1.0,
                done,
                out_of_bounds,
                {"info": "No available worker"},
            )

        worker_id, worker_position = available_workers[0]
        reachable_moves = self.client.unit_get_reachable_sectors(
            game_id, self.agent_team_id, worker_id
        )

        if not reachable_moves:
            self.client.team_end_turn(game_id, self.agent_team_id)
            reward = 0.0
            done = False
            out_of_bounds = False

            self._simulate_opponent_turn()

            return (
                self._get_observation(),
                reward,
                done,
                out_of_bounds,
                {"info": "No reachable moves"},
            )

        move_index = int(action)
        if move_index < 0 or move_index >= len(reachable_moves):
            move_index = 0

        target_move = reachable_moves[move_index]
        result = self.client.unit_move(
            game_id, self.agent_team_id, worker_id, target_move
        )

        reward = 0.0
        if result.capturedBuilding:
            reward += 1.0
        if result.killedEnemy:
            reward += 0.5
        if result.hurt:
            reward -= 0.5
        if result.died:
            reward -= 1.0

        self.client.team_end_turn(game_id, self.agent_team_id)

        self.current_step += 1
        done = self.current_step >= self.max_steps
        out_of_bounds = False

        game = self.client.game_get_info(game_id)
        if game.state == GameStates.FINISHED:
            if game.winningTeamId == self.agent_team_id:
                reward = 1000.0
            else:
                reward = -1000.0

            done = True
            out_of_bounds = False
            return (
                self._get_observation(),
                reward,
                done,
                out_of_bounds,
                {"info": "Game is over"},
            )

        self._simulate_opponent_turn()

        obs = self._get_observation()
        return obs, reward, done, out_of_bounds, {}

    def render(self, mode: str = "human") -> None:
        """Renders the current visible map in a compact form."""

        assert self.game is not None
        assert self.agent_team_id is not None

        game_id = self.game.id
        visible_map = self.client.team_get_visible_map(
            game_id, self.agent_team_id
        )
        teams = list(self.client.game_get_info(game_id).teams.keys())
        self.client.visualize_map_compact(visible_map, teams)

    def _get_observation(self) -> dict:
        """
        Constructs an observation containing:
         - A compact representation of the visible map.
         - A list of reachable moves (tuples) for the first available worker
           unit.
        """

        assert self.game is not None
        assert self.agent_team_id is not None

        game_id = self.game.id
        visible_map = self.client.team_get_visible_map(
            game_id, self.agent_team_id
        )

        available_workers = self._find_available_workers(
            visible_map, self.agent_team_id
        )

        if available_workers:
            worker_id, worker_position = available_workers[0]
            reachable_moves = self.client.unit_get_reachable_sectors(
                game_id, self.agent_team_id, worker_id
            )
            reachable_moves_list = [
                (move.x, move.y) for move in reachable_moves
            ]
        else:
            reachable_moves_list = []

        teams = list(self.client.game_get_info(game_id).teams.keys())
        teams.insert(0, TEAMS_NEUTRAL_ID)
        out_data: List[List[str]] = [[] for _ in range(len(visible_map))]
        for x, column in enumerate(visible_map):
            new_column = []
            for y, sector in enumerate(column):
                if sector:
                    cell = "".join([
                        f"{entity.type[0]}{teams.index(entity.teamId)}"
                        for entity in sector if entity
                    ])
                elif sector is not None:
                    cell = "_\xff" * 4
                else:
                    cell = "~\xff" * 4
                new_column.append(cell)
            out_data.append(new_column)

        observation = {
            "visible_map": out_data,
            "reachable_moves": reachable_moves_list,
        }
        return observation

    def _find_available_workers(
            self,
            visible_map: List[List[Optional[List[Optional[Entity]]]]],
            team_id: str
    ) -> List[Tuple[str, Point]]:
        """
        Finds all available worker units for the given team.
        """

        available_workers = []
        for x, column in enumerate(visible_map):
            for y, sector in enumerate(column):
                if not sector:
                    continue
                for entity in sector:
                    if (
                            entity
                            and entity.type == "Worker"
                            and entity.teamId == team_id
                    ):
                        available_workers.append((entity.id, entity.position))
        return available_workers

    def _simulate_opponent_turn(self) -> None:
        """
        Simulates a simple opponent turn using a random move.
        """

        assert self.game is not None
        assert self.opponent_team_id is not None

        game_id = self.game.id
        visible_map = self.client.team_get_visible_map(
            game_id, self.opponent_team_id
        )
        available_workers = self._find_available_workers(
            visible_map, self.opponent_team_id
        )
        if not available_workers:
            self.client.team_end_turn(game_id, self.opponent_team_id)
            return

        worker_id, worker_position = available_workers[0]
        reachable_moves = self.client.unit_get_reachable_sectors(
            game_id,
            self.opponent_team_id,
            worker_id
        )
        if reachable_moves:
            target_move = random.choice(reachable_moves)
            self.client.unit_move(
                game_id, self.opponent_team_id, worker_id, target_move
            )
        self.client.team_end_turn(game_id, self.opponent_team_id)
