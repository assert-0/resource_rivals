from client.client import Client
from utils.logger import get_logger

logger = get_logger("examples.basic_game")
client = Client()


def perform_turn(game_id: str, team_id: str):
    logger.info(f"Performing turn for team {team_id}")
    teams = client.game_get_info(game_id).teams

    visible_map = client.team_get_visible_map(game_id, team_id)
    client.visualize_map_compact(visible_map, list(teams.keys()))

    available_workers = []

    for x, column in enumerate(visible_map):
        for y, sector in enumerate(column):
            if not sector:
                continue

            logger.info(f"Sector {x}, {y} is visible")
            logger.debug(f"Entities in sector: {sector}")

            for entity in sector:
                if (
                        entity.type == "Worker"
                        and entity.teamId == team_id
                ):
                    logger.info(f"Friendly worker unit found at {x}, {y}")
                    logger.debug(f"Entity: {entity}")
                    available_workers.append(
                        [entity.id, entity.position]
                    )

    if not available_workers:
        raise ValueError("No worker unit found to move")

    for selected_worker_id, worker_position in available_workers:
        logger.info(
            f"Moving worker unit {selected_worker_id} at {worker_position}"
        )

        reachable_sectors = client.unit_get_reachable_sectors(
            game_id, team_id, selected_worker_id
        )
        logger.info(f"Reachable sectors: {reachable_sectors}")

        if not reachable_sectors:
            logger.info("No reachable sectors found. Trying next worker")
            continue

        selected_sector = reachable_sectors[0]

        client.unit_move(game_id, team_id, selected_worker_id, selected_sector)

        logger.info(f"Unit moved to {selected_sector}")

    client.team_end_turn(game_id, team_id)

    logger.info("Turn ended")


def main():
    logger.info("Starting example")

    logger.info("Creating game")
    game_id = client.game_create("example").id

    logger.info("Creating teams")
    team_1_id = client.team_create(game_id, "Team 1").id
    team_2_id = client.team_create(game_id, "Team 2").id

    logger.info("Starting game")
    client.game_start(game_id)

    game_info = client.game_get_info(game_id)
    first_team = game_info.activeTeamId
    other_team = team_2_id if first_team == team_1_id else team_1_id

    for i in range(5):
        logger.debug("================================")
        perform_turn(game_id, first_team)
        logger.debug("================================")
        logger.debug("================================")
        perform_turn(game_id, other_team)
        logger.debug("================================")


if __name__ == "__main__":
    main()
