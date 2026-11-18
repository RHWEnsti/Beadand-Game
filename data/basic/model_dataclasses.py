from dataclasses import dataclass

@dataclass
class Player:
    playerId: str
    name: str
    country: str
    elo: int
    kd: float
    wins: int
    losses: int
    male: bool
    age: int

@dataclass
class Match:
    matchId: int
    date: int
    map: str
    score: int
    overtime: bool


@dataclass
class PlayerMatchStats:
    kills: int
    deaths: int
    assists: int
    headshots: int
    adr: float
    rating: float

