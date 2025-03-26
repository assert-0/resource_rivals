#!/usr/bin/env python3
import curses
from curses import wrapper
from typing import List, Tuple, Optional

from client.client import Client
from utils.math import Point

# Global client instance.
client = Client()


def get_compact_map_str(game_id: str, team_id: str) -> List[str]:
    """
    Retrieves the visible map for the team and returns a list of strings
    representing a compact view of the map.
    """
    visible_map = client.team_get_visible_map(game_id, team_id)
    header_line = "Y\\X  | " + " ".join(
        [f"{str(i):4}" for i in range(len(visible_map))])
    map_lines = [f"{str(i):4} | " for i in range(len(visible_map))]
    for column in visible_map:
        for idx, sector in enumerate(column):
            if sector is None:
                map_lines[idx] += "~    "  # Fog
            elif sector == []:
                map_lines[idx] += "_    "  # Empty sector
            else:
                # Display the first letter of each entity type.
                entities = "".join([e.type[0] for e in sector if e])
                map_lines[idx] += f"{entities:4} "
    map_lines.insert(0, header_line)
    return map_lines


def draw_menu(
        stdscr, menu_items: List[str], title: str,
        header_lines: Optional[List[str]] = None
) -> int:
    """
    Displays a menu and returns the index of the selected item.
    If header_lines is provided, they are displayed at the top of the screen.
    Navigation: use UP/DOWN arrow keys; press Enter to select.
    """
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        y_offset = 1

        # Display title.
        stdscr.addstr(y_offset, 2, title, curses.A_BOLD)
        y_offset += 2

        # Display header lines (e.g. active team and map view) if provided.
        if header_lines:
            for line in header_lines:
                stdscr.addstr(y_offset, 2, line)
                y_offset += 1
            y_offset += 1  # Blank line after header

        # Display menu items.
        for idx, item in enumerate(menu_items):
            x = 4
            y = y_offset + idx
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return current_row


def prompt_user(stdscr, prompt: str) -> str:
    """
    Prompts the user for input.
    """
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    curses.echo()
    input_str = stdscr.getstr(1, 0).decode("utf-8").strip()
    curses.noecho()
    return input_str


def display_message(stdscr, message: str):
    """
    Displays a message until a key is pressed.
    """
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    lines = len(message.split("\n"))
    stdscr.addstr(lines + 1, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()


def move_unit(stdscr, game_id: str, team_id: str):
    """
    Allows the user to select a worker unit and move it to one of its reachable
    sectors.
    """
    try:
        visible_map = client.team_get_visible_map(game_id, team_id)
    except Exception as e:
        display_message(stdscr, f"Error getting visible map: {e}")
        return

    # Find worker units on the visible map.
    friendly_units: List[Tuple[str, Point, str]] = []
    for column in visible_map:
        for sector in column:
            if sector:
                for entity in sector:
                    if (
                            entity
                            and entity.teamId == team_id
                            and "units" in entity.namespace
                    ):
                        friendly_units.append(
                            (entity.id, entity.position, entity.type)
                        )
    if not friendly_units:
        display_message(stdscr, "No units available to move!")
        return

    # Let user select one worker unit.
    menu = [f"{etype} at {pos}" for _, pos, etype in friendly_units]
    choice = draw_menu(
        stdscr, menu, "Select a unit to move:",
        get_compact_map_str(game_id, team_id)
    )
    selected_unit_id, _, __ = friendly_units[choice]

    # Retrieve reachable sectors.
    try:
        reachable_sectors = client.unit_get_reachable_sectors(
            game_id, team_id, selected_unit_id
        )
    except Exception as e:
        display_message(
            stdscr, f"Error retrieving reachable sectors: {e}"
        )
        return

    if not reachable_sectors:
        display_message(stdscr, "No reachable sectors for the selected unit!")
        return

    # Let user select a target sector.
    menu = [f"{sector}" for sector in reachable_sectors]
    choice = draw_menu(
        stdscr, menu, "Select a sector to move to:",
        get_compact_map_str(game_id, team_id)
    )
    target_sector = reachable_sectors[choice]

    # Move the unit.
    try:
        result = client.unit_move(game_id, team_id, selected_unit_id,
                                  target_sector)
        msg = (
            f"Unit {selected_unit_id} "
            f"moved to {target_sector}.\n"
            f"Result: {result}"
        )
    except Exception as e:
        msg = f"Error moving unit: {e}"

    display_message(stdscr, msg)


def build_building(stdscr, game_id: str, team_id: str):
    """
    Allows the user to select a worker unit and build one of its available
    buildings.
    """
    try:
        visible_map = client.team_get_visible_map(game_id, team_id)
    except Exception as e:
        display_message(stdscr, f"Error retrieving visible map: {e}")
        return

    # Find worker units available for building.
    worker_units: List[Tuple[str, Point]] = []
    for column in visible_map:
        for sector in column:
            if sector:
                for entity in sector:
                    if (
                            entity
                            and entity.type == "Worker"
                            and entity.teamId == team_id
                    ):
                        worker_units.append((entity.id, entity.position))
    if not worker_units:
        display_message(stdscr, "No worker units available for building!")
        return

    # Let user select a worker unit.
    menu = [f"Worker {wid} at {pos}" for wid, pos in worker_units]
    choice = draw_menu(
        stdscr, menu, "Select a worker unit to build with:",
        get_compact_map_str(game_id, team_id)
    )
    selected_worker_id, _ = worker_units[choice]

    # Retrieve available building options for the selected unit.
    try:
        available_buildings = client.unit_get_available_buildings(
            game_id,
            team_id,
            selected_worker_id
        )
    except Exception as e:
        display_message(stdscr, f"Error getting available buildings: {e}")
        return

    if not available_buildings:
        display_message(stdscr, "No available buildings for this unit!")
        return

    # Assume available_buildings is a list of [namespace, type] pairs.
    menu = [f"Namespace: {opt[0]}, Type: {opt[1]}" for opt in
            available_buildings]
    choice = draw_menu(stdscr, menu, "Select a building to construct:")
    building_namespace, building_type = available_buildings[choice]

    # Attempt to build the selected building.
    try:
        client.unit_build(game_id, team_id, selected_worker_id, building_type,
                          building_namespace)
        msg = (
            f"Worker {selected_worker_id} built {building_type} "
            f"(namespace: {building_namespace})."
        )
    except Exception as e:
        msg = f"Error building: {e}"

    display_message(stdscr, msg)


def end_turn(stdscr, game_id: str, current_team_id: str, teams: dict) -> str:
    """
    Ends the turn for the current active team and returns the new active
    team's ID.
    """
    try:
        client.team_end_turn(game_id, current_team_id)
        game_info = client.game_get_info(game_id)
        new_team = game_info.activeTeamId
        team_name = teams.get(new_team, new_team)
        message = f"Turn ended. New active team: {team_name} (id: {new_team})"
    except Exception as e:
        message = f"Error ending turn: {e}"
        new_team = current_team_id
    display_message(stdscr, message)
    return new_team


def main(stdscr):
    # Game state variables.
    game_id = None
    teams = {}  # Maps team id to team name.
    active_team_id = None

    while True:
        # Build header lines if game is started and active team is set.
        header_lines: List[str] = []
        if game_id and active_team_id:
            header_lines.append(
                f"Active Team: {teams.get(active_team_id, active_team_id)} "
                f"(id: {active_team_id})"
            )
            try:
                map_lines = get_compact_map_str(game_id, active_team_id)
                header_lines.extend(map_lines)
            except Exception:
                header_lines.append("Error retrieving map view.")

        main_menu = [
            "Create Game",
            "Create Team",
            "Start Game",
            "Show Visible Map",
            "Move Unit",
            "Build Building",
            "End Turn",
            "Quit"
        ]
        choice = draw_menu(stdscr, main_menu, "Turn-Based Strategy Game TUI",
                           header_lines)

        if choice == 0:  # Create Game
            map_name = prompt_user(stdscr,
                                   "Enter map name (leave empty for default):")
            try:
                game = client.game_create(map_name if map_name else None)
                game_id = game.id
                display_message(stdscr, f"Game created with id: {game_id}")
            except Exception as e:
                display_message(stdscr, f"Error creating game: {e}")

        elif choice == 1:  # Create Team
            if not game_id:
                display_message(stdscr, "Please create a game first!")
                continue
            team_name = prompt_user(stdscr, "Enter team name:")
            try:
                team = client.team_create(game_id, team_name)
                teams[team.id] = team_name
                display_message(
                    stdscr,
                    f"Team '{team_name}' created with id: {team.id}"
                )
            except Exception as e:
                display_message(stdscr, f"Error creating team: {e}")

        elif choice == 2:  # Start Game
            if not game_id:
                display_message(stdscr, "Please create a game first!")
                continue
            try:
                client.game_start(game_id)
                game_info = client.game_get_info(game_id)
                active_team_id = game_info.activeTeamId
                display_message(stdscr, "Game started!")
            except Exception as e:
                display_message(stdscr, f"Error starting game: {e}")

        elif choice == 3:  # Show Visible Map
            if not game_id or not teams:
                display_message(stdscr, "Game or teams not set up!")
                continue
            # Allow the user to select a team to view its map.
            team_menu = [f"{name} (id: {tid})" for tid, name in teams.items()]
            team_choice = draw_menu(stdscr, team_menu,
                                    "Select team to view its visible map:")
            team_ids = list(teams.keys())
            selected_team_id = team_ids[team_choice]
            try:
                map_lines = get_compact_map_str(game_id, selected_team_id)
                display_message(
                    stdscr,
                    (
                            f"Visible Map for team "
                            f"{teams.get(selected_team_id, selected_team_id)}:"
                            f"\n"
                    ) + "\n".join(map_lines))
            except Exception as e:
                display_message(stdscr, f"Error displaying map: {e}")

        elif choice == 4:  # Move Unit
            if not game_id or not active_team_id:
                display_message(stdscr,
                                "Game not started or active team not set!")
                continue
            move_unit(stdscr, game_id, active_team_id)

        elif choice == 5:  # Build Building
            if not game_id or not active_team_id:
                display_message(stdscr,
                                "Game not started or active team not set!")
                continue
            build_building(stdscr, game_id, active_team_id)

        elif choice == 6:  # End Turn
            if not game_id or not active_team_id:
                display_message(stdscr,
                                "Game not started or active team not set!")
                continue
            active_team_id = end_turn(stdscr, game_id, active_team_id, teams)

        elif choice == 7:  # Quit
            break


if __name__ == "__main__":
    wrapper(main)
