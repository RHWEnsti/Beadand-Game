
import csv
import os
from dataclasses import fields
from data.basic.model_dataclasses import Player, Match, PlayerMatchStats


def write_players(
        players: list[Player],
        path: str,
        delimiter: str = ";",
        file_name: str = "players.csv"
):
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name), "w",
              newline="", encoding="utf-8") as file:

        csv_writer = csv.writer(file, delimiter=delimiter)

        player_fields = fields(Player)

        csv_writer.writerow([field.name for field in player_fields])

        for player in players:
            csv_writer.writerow(
                [getattr(player, field.name) for field in player_fields]
            )



def read_players(
        path: str,
        delimiter: str = ";",
        file_name: str = "players.csv"
) -> list[Player]:

    players = []

    with open(os.path.join(path, file_name), "r",
              newline="", encoding="utf-8") as file:

        csv_reader = csv.reader(file, delimiter=delimiter)

        next(csv_reader)

        for row in csv_reader:
            players.append(
                Player(
                    row[0],
                    row[1],
                    row[2],
                    int(row[3]),
                    float(row[4]),
                    int(row[5]),
                    int(row[6]),
                    row[7].lower() == "true",
                    int(row[8])
                )
            )

    return players

def write_matches(
        matches: list[Match],
        path: str,
        delimiter: str = ";",
        file_name: str = "matches.csv"
):
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name), "w",
              newline="", encoding="utf-8") as file:

        csv_writer = csv.writer(file, delimiter=delimiter)

        match_fields = fields(Match)

        csv_writer.writerow([field.name for field in match_fields])

        for match in matches:
            csv_writer.writerow(
                [getattr(match, field.name) for field in match_fields]
            )

def read_matches(
        path: str,
        delimiter: str = ";",
        file_name: str = "matches.csv"
) -> list[Match]:

    matches = []

    with open(os.path.join(path, file_name), "r",
              newline="", encoding="utf-8") as file:

        csv_reader = csv.reader(file, delimiter=delimiter)

        next(csv_reader)

        for row in csv_reader:
            matches.append(
                Match(
                    int(row[0]),
                    int(row[1]),
                    row[2],
                    int(row[3]),
                    row[4].lower() == "true"
                )
            )

    return matches

def write_player_match_stats(
        stats: list[PlayerMatchStats],
        path: str,
        delimiter: str = ";",
        file_name: str = "player_match_stats.csv"
):
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, file_name), "w",
              newline="", encoding="utf-8") as file:

        csv_writer = csv.writer(file, delimiter=delimiter)

        stat_fields = fields(PlayerMatchStats)

        csv_writer.writerow([field.name for field in stat_fields])

        for stat in stats:
            csv_writer.writerow(
                [getattr(stat, field.name) for field in stat_fields]
            )

def read_player_match_stats(
        path: str,
        delimiter: str = ";",
        file_name: str = "player_match_stats.csv"
) -> list[PlayerMatchStats]:

    stats = []

    with open(os.path.join(path, file_name), "r",
              newline="", encoding="utf-8") as file:

        csv_reader = csv.reader(file, delimiter=delimiter)

        next(csv_reader)

        for row in csv_reader:
            stats.append(
                PlayerMatchStats(
                    int(row[0]),
                    int(row[1]),
                    int(row[2]),
                    int(row[3]),
                    float(row[4]),
                    float(row[5])
                )
            )

    return stats