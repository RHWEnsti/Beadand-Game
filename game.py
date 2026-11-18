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

    def __init__(self, playerId: str, name: str, country: str, elo: int, kd: float, wins: int, losses: int, male: bool, age: int):
        self.playerId = playerId
        self.name = name
        self.country = country
        self.elo = elo
        self.kd = kd
        self.wins = wins
        self.losses = losses
        self.male = male
        self.age = age

    def __str__(self):
        return f"{self.playerId} ({self.name}), '{self.country}', Elo:{self.elo}, kd:[{self.kd},W:{self.wins}, L:{self.losses}]"
    def __eq__(self, other)->bool:
        return isinstance(other,Player) and self.name == other.name
    def __ne__(self, other)->bool:
        return not self.__eq__(other)
    def __hash__(self)->int:
        return self.name.__hash__()

@dataclass
class Match:
    matchId: int
    date: int
    map: str
    score: int


    def __init__(self, matchId: int, date: int, map: str, score: int):
        self.matchId = matchId
        self.date = date
        self.map = map
        self.score = score

    def __str__(self):
        return f"{self.map}, {self.score}, [{self.date}, ID:{self.matchId}]"
    def __eq__(self, other)->bool:
        return isinstance(other, Match) and self.matchId == other.matchId
    def __ne__(self, other)->bool:
        return not self.__eq__(other)
    def __hash__(self)->int:
        return self.matchId.__hash__()



@dataclass
class PlayerMatchStats:
    kills: int
    deaths: int
    assists: int
    headshots: int
    adr: float
    rating: float

    def __init__(self, kills: int, deaths: int, assists: int, headshots: int, adr: float, rating: float):
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.headshots = headshots
        self.adr = adr
        self.rating = rating

    def __str__(self):
        return f"KDA:{self.kills}/{self.deaths}/{self.assists}  HS:{self.headshots}%, ADR:{self.adr} Rating:{self.rating}"
    def __eq__(self, other)->bool:
        return isinstance(other,PlayerMatchStats) and self.rating ==other.rating
    def __ne__(self, other)->bool:
        return not self.__eq__(other)
    def __hash__(self)->int:
        return self.rating.__hash__()



