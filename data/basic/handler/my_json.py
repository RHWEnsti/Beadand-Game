import json
import os
from dataclasses import asdict
from data.basic.model_dataclasses import Player, Match, PlayerMatchStats



def write_players(
        players: list[Player],
        path: str,
        file_name: str | None = "players",
        extension: str | None = ".json",
        pretty: bool = True
):
    if file_name is None:
        file_name = "players"

    if extension is None:
        extension = ".json"

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name + extension), "w",
              encoding="utf-8") as file:

        json.dump(
            [asdict(player) for player in players],
            file,
            indent=4 if pretty else None
        )

def write_matches(
        matches: list[Match],
        path: str,
        file_name: str | None = "matches",
        extension: str | None = ".json",
        pretty: bool = True
):
    if file_name is None:
        file_name = "matches"

    if extension is None:
        extension = ".json"

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name + extension), "w",
              encoding="utf-8") as file:

        json.dump(
            [asdict(match) for match in matches],
            file,
            indent=4 if pretty else None
        )

def write_player_match_stats(
        stats: list[PlayerMatchStats],
        path: str,
        file_name: str | None = "player_match_stats",
        extension: str | None = ".json",
        pretty: bool = True
):
    if file_name is None:
        file_name = "player_match_stats"

    if extension is None:
        extension = ".json"

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name + extension), "w",
              encoding="utf-8") as file:

        json.dump(
            [asdict(stat) for stat in stats],
            file,
            indent=4 if pretty else None
        )

def read_player_match_stats(
        path: str,
        file_name: str | None = "player_match_stats",
        extension: str | None = ".json"
) -> list[PlayerMatchStats]:

    if file_name is None:
        file_name = "player_match_stats"

    if extension is None:
        extension = ".json"

    with open(os.path.join(path, file_name + extension), "r",
              encoding="utf-8") as file:

        data = json.load(file)

    return [PlayerMatchStats(**stat) for stat in data]

def read_matches(
        path: str,
        file_name: str | None = "matches",
        extension: str | None = ".json"
) -> list[Match]:

    if file_name is None:
        file_name = "matches"

    if extension is None:
        extension = ".json"

    with open(os.path.join(path, file_name + extension), "r",
              encoding="utf-8") as file:

        data = json.load(file)

    return [Match(**match) for match in data]

def read_players(
        path: str,
        file_name: str | None = "players",
        extension: str | None = ".json"
) -> list[Player]:

    if file_name is None:
        file_name = "players"

    if extension is None:
        extension = ".json"

    with open(os.path.join(path, file_name + extension), "r",
              encoding="utf-8") as file:

        data = json.load(file)

    return [Player(**player) for player in data]

def write(
        entities: list[object],
        path: str,
        file_name: str | None = None,
        extension: str | None = None,
        pretty: bool = True
):

    if not entities:
        raise ValueError("The entities list cannot be empty")

    if all(isinstance(entity, Player) for entity in entities):
        write_players(entities, path, file_name, extension, pretty)

    elif all(isinstance(entity, Match) for entity in entities):
        write_matches(entities, path, file_name, extension, pretty)

    elif all(isinstance(entity, PlayerMatchStats) for entity in entities):
        write_player_match_stats(entities, path, file_name, extension, pretty)

    else:
        raise TypeError("Unknown entity type")

def read(
        entity_type: type,
        path: str,
        file_name: str | None = None,
        extension: str | None = None
) -> list[object]:

    if entity_type is Player:
        return read_players(path, file_name, extension)

    elif entity_type is Match:
        return read_matches(path, file_name, extension)

    elif entity_type is PlayerMatchStats:
        return read_player_match_stats(path, file_name, extension)

    else:
        raise TypeError("Unknown entity type")