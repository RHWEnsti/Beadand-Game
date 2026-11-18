
from dataclasses import fields
from typing import Type, get_type_hints
from openpyxl import Workbook

from data.basic.model_dataclasses import Player, Match, PlayerMatchStats



def _write_entities(
        entities: list,
        workbook: Workbook,
        entity_type: type,
        sheet_name: str | None,
        heading: bool,
        default_name: str
):
    if sheet_name is None:
        sheet_name = default_name

    if sheet_name in workbook.sheetnames:
        del workbook[sheet_name]

    worksheet = workbook.create_sheet(title=sheet_name)

    entity_fields = fields(entity_type)

    if heading:
        worksheet.append([field.name for field in entity_fields])

    for entity in entities:
        worksheet.append(
            [getattr(entity, field.name) for field in entity_fields]
        )



def write_players(
        players: list[Player],
        workbook: Workbook,
        sheet_name: str | None = "players",
        heading: bool = True
):
    _write_entities(
        players, workbook, Player, sheet_name, heading, "players"
    )



def read_players(
        workbook: Workbook,
        sheet_name: str | None = "players",
        heading: bool = True
) -> list[Player]:
    return _read_entities(Player, workbook, sheet_name, heading, "players")



def write_matches(
        matches: list[Match],
        workbook: Workbook,
        sheet_name: str | None = "matches",
        heading: bool = True
):
    _write_entities(
        matches, workbook, Match, sheet_name, heading, "matches"
    )



def read_matches(
        workbook: Workbook,
        sheet_name: str | None = "matches",
        heading: bool = True
) -> list[Match]:
    return _read_entities(Match, workbook, sheet_name, heading, "matches")



def write_player_match_stats(
        stats: list[PlayerMatchStats],
        workbook: Workbook,
        sheet_name: str | None = "player_match_stats",
        heading: bool = True
):
    _write_entities(
        stats, workbook, PlayerMatchStats,
        sheet_name, heading, "player_match_stats"
    )



def read_player_match_stats(
        workbook: Workbook,
        sheet_name: str | None = "player_match_stats",
        heading: bool = True
) -> list[PlayerMatchStats]:
    return _read_entities(
        PlayerMatchStats, workbook,
        sheet_name, heading, "player_match_stats"
    )



def _convert_value(value, target_type):
    if value is None:
        return None

    if target_type is bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("true", "1", "yes")

    if target_type is int:
        return int(value)

    if target_type is float:
        return float(value)

    if target_type is str:
        return str(value)

    return value



def _read_entities(
        entity_type: type,
        workbook: Workbook,
        sheet_name: str | None,
        heading: bool,
        default_name: str
) -> list:

    if sheet_name is None:
        sheet_name = default_name

    worksheet = workbook[sheet_name]

    rows = worksheet.iter_rows(values_only=True)

    if heading:
        headers = next(rows, None)

        if headers is None:
            return []

        column_names = headers
    else:
        column_names = [field.name for field in fields(entity_type)]

    type_hints = get_type_hints(entity_type)
    entities = []

    for row in rows:
        if all(value is None for value in row):
            continue

        row_data = dict(zip(column_names, row))

        values = {}

        for field in fields(entity_type):
            value = row_data.get(field.name)
            values[field.name] = _convert_value(
                value, type_hints[field.name]
            )

        entities.append(entity_type(**values))

    return entities



def write(
        entities: list[object],
        workbook: Workbook,
        sheet_name: str | None = None,
        heading: bool = True
):

    if not entities:
        raise TypeError("Cannot determine entity type from an empty list")

    entity_type = type(entities[0])

    if not all(type(entity) is entity_type for entity in entities):
        raise TypeError("Mixed entity types are not supported in one worksheet")

    if entity_type is Player:
        write_players(entities, workbook, sheet_name, heading)

    elif entity_type is Match:
        write_matches(entities, workbook, sheet_name, heading)

    elif entity_type is PlayerMatchStats:
        write_player_match_stats(entities, workbook, sheet_name, heading)

    else:
        raise TypeError("Unknown entity type")



def read(
        entity_type: Type[object],
        workbook: Workbook,
        sheet_name: str | None = None,
        heading: bool = True
) -> list[object]:

    if entity_type is Player:
        return read_players(workbook, sheet_name, heading)

    elif entity_type is Match:
        return read_matches(workbook, sheet_name, heading)

    elif entity_type is PlayerMatchStats:
        return read_player_match_stats(workbook, sheet_name, heading)

    else:
        raise TypeError("Unknown entity type")
