from openpyxl import Workbook, load_workbook

from data.basic.handler.xlsx import (
    write as write_xlsx,
    read as read_xlsx
)
from data.basic.handler.my_json import read as read_json
from data.basic.handler.my_json import (
    write_players as write_players_json,
    read_players as read_players_json,
    write_matches as write_matches_json,
    read_matches as read_matches_json,
    write as write_json,
    write_player_match_stats as write_player_match_stats_json,
    read_player_match_stats as read_player_match_stats_json
)
from pathlib import Path
from faker import Faker
import random
from data.basic.model_dataclasses import Player, Match, PlayerMatchStats
from data.basic.handler.csv_list import (write_players,
                                         read_players,
                                         write_matches,
                                         read_matches,
                                         write_player_match_stats,
                                         read_player_match_stats)


output_dir = Path(__file__).resolve().parents[2] / "Output csv"
json_output_dir = Path(__file__).resolve().parents[2] / "Output json"

def generate_Players(
        n: int,
        male_ratio: float = 0.7,
        locale: str = "en_US",
        unique: bool =False,
        min_age: int = 15,
        max_age: int = 40
)->list[Player]:

    assert n > 0
    assert 0 < male_ratio < 1
    assert min_age >= 0

    fake = Faker(locale)
    players = []

    for i in range(n):
        male = random.random() < male_ratio
        generator = fake if not unique else fake.unique

        players.append(
            Player(
                "P-" + str(i).zfill(6),
                generator.name_male() if male else generator.name_female(),
                fake.country(),
                random.randint(1000, 2500),
                round(random.uniform(0.5, 2.0), 2),
                random.randint(0, 100),
                random.randint(0, 100),
                male,
                random.randint(min_age,max_age + 1)
            )
        )

    return players

players = generate_Players(10)
for player in players:
    print(player)


def generate_matches(
        n: int,
        min_score: int = 0,
        max_score: int = 13,
        overtime_ratio: float = 0.2
) -> list[Match]:

    assert n > 0
    assert 0 <= overtime_ratio <= 1
    assert min_score >= 0
    assert max_score >= min_score

    matches = []

    maps = [
        "Mirage", "Inferno", "Dust2", "Nuke",
        "Ancient", "Anubis", "Vertigo"
    ]

    for i in range(n):
        overtime = random.random() < overtime_ratio

        matches.append(
            Match(
                i,
                random.randint(2020, 2026),
                random.choice(maps),
                random.randint(min_score, max_score),
                overtime
            )
        )

    return matches



matches = generate_matches(5, overtime_ratio= 0.8)
for match in matches:
    print(match)
    print("Hosszabítás", match.overtime)


def generate_player_match_stats(
        n: int,
        min_rating: float = 0.3,
        max_rating: float = 3.0,
        unique: bool = False,
        attempts: int | None = None,
) -> list[PlayerMatchStats]:

    assert n > 0
    assert attempts is None or attempts >=n
    stats = []
    tries = 0

    while len(stats) < n and (attempts is None or tries < attempts):
        tries+=1

        kills = random.randint(0,40)
        deaths = random.randint(0, 30)
        assists = random.randint(0,20)
        headshots = random.randint(0, kills)
        rating = round(random.uniform(0.3,3.0),2)

        stat=PlayerMatchStats(
            kills,
            deaths,
            assists,
            headshots,
            round(random.uniform(0,150),1),
            rating
        )

        if headshots <= kills and min_rating <= rating <= max_rating:
            if not unique or stat not in stats:
                stats.append(stat)
    return stats

stats = generate_player_match_stats(
    10,
    min_rating=1.0,
    max_rating=2.0,
    unique=True,
    attempts=20
)

print(len(stats))

for stat in stats:
    print(stat)


write_player_match_stats(
    stats,
    str(output_dir),
    delimiter=";",
    file_name="cs2_player_match_stats.csv"
)

loaded_stats = read_player_match_stats(
    str(output_dir),
    delimiter=";",
    file_name="cs2_player_match_stats.csv"
)

print("Beolvasott statisztikák:", len(loaded_stats))

for stat in loaded_stats:
    print(stat)


players = generate_Players(10)
write_players(
    players,
    str(output_dir),
    delimiter=";",
    file_name="cs2_players.csv"
)

matches = generate_matches(10)

write_matches(
    matches,
    str(output_dir),
    delimiter=";",
    file_name="cs2_matches.csv"
)

loaded_matches = read_matches(
    str(output_dir),
    delimiter=";",
    file_name="cs2_matches.csv"
)

print("Beolvasott meccsek:", len(loaded_matches))

for match in loaded_matches:
    print(match)

print("CSV mentési helye:", output_dir / "cs2_players.csv")


loaded_players = read_players(
    str(output_dir),
    file_name="cs2_players.csv"
)

print("Beolvasott játékosok:", len(loaded_players))

for player in loaded_players:
    print(player)


write_players_json(
    players,
    str(json_output_dir),
    file_name="cs2_players",
    extension=".json",
    pretty=True
)

loaded_players_json = read_players_json(
    str(json_output_dir),
    file_name="cs2_players",
    extension=".json"
)

print("JSON-ből beolvasott játékosok:", len(loaded_players_json))

for player in loaded_players_json:
    print(player)

write_matches_json(
    matches,
    str(json_output_dir),
    file_name="cs2_matches",
    extension=".json",
    pretty=True
)

loaded_matches_json = read_matches_json(
    str(json_output_dir),
    file_name="cs2_matches",
    extension=".json"
)

print("JSON-ből beolvasott meccsek:", len(loaded_matches_json))

for match in loaded_matches_json:
    print(match)

write_player_match_stats_json(
    stats,
    str(json_output_dir),
    file_name="cs2_player_match_stats",
    extension=".json",
    pretty=True
)

loaded_stats_json = read_player_match_stats_json(
    str(json_output_dir),
    file_name="cs2_player_match_stats",
    extension=".json"
)

print("JSON-ből beolvasott statisztikák:", len(loaded_stats_json))

for stat in loaded_stats_json:
    print(stat)

players = read_json(
    Player,
    str(json_output_dir),
    "cs2_players",
    ".json"
)

loaded_players = read_json(
    Player,
    str(json_output_dir),
    "cs2_players",
    ".json"
)

print("Közvetítő read() eredménye:")
print("Játékosok száma:", len(loaded_players))

for player in loaded_players:
    print(player)

loaded_matches = read_json(
    Match,
    str(json_output_dir),
    "cs2_matches",
    ".json"
)

loaded_stats = read_json(
    PlayerMatchStats,
    str(json_output_dir),
    "cs2_player_match_stats",
    ".json"
)

print("Meccsek:", len(loaded_matches))
print("Statisztikák:", len(loaded_stats))

write_json(
    players,
    str(json_output_dir),
    file_name="players_test",
    extension=".json",
    pretty=True
)

write_json(
    matches,
    str(json_output_dir),
    file_name="matches_test",
    extension=".json",
    pretty=True
)

write_json(
    stats,
    str(json_output_dir),
    file_name="stats_test",
    extension=".json",
    pretty=True
)

print("Mindhárom típus mentése sikeres!")



xlsx_output_dir = Path(__file__).resolve().parents[2] / "Output xlsx"
xlsx_output_dir.mkdir(parents=True, exist_ok=True)


workbook = Workbook()


workbook.remove(workbook.active)


write_xlsx(
    players,
    workbook,
    sheet_name="Players",
    heading=True
)


write_xlsx(
    matches,
    workbook,
    sheet_name="Matches",
    heading=True
)


write_xlsx(
    stats,
    workbook,
    sheet_name="PlayerMatchStats",
    heading=True
)


xlsx_file = xlsx_output_dir / "cs2_data.xlsx"
workbook.save(xlsx_file)

print("XLSX mentés sikeres:", xlsx_file)



loaded_workbook = load_workbook(xlsx_file)

loaded_players_xlsx = read_xlsx(
    Player,
    loaded_workbook,
    sheet_name="Players"
)

loaded_matches_xlsx = read_xlsx(
    Match,
    loaded_workbook,
    sheet_name="Matches"
)

loaded_stats_xlsx = read_xlsx(
    PlayerMatchStats,
    loaded_workbook,
    sheet_name="PlayerMatchStats"
)

print("XLSX visszaolvasás eredménye:")
print("Játékosok:", len(loaded_players_xlsx))
print("Meccsek:", len(loaded_matches_xlsx))
print("Statisztikák:", len(loaded_stats_xlsx))

loaded_workbook.close()
