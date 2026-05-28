from __future__ import annotations

# SINGLE-FILE STREAMLIT DEPLOY BUILD
# All football_sim modules are inlined below to avoid ModuleNotFoundError on Streamlit Cloud.

import json
import math
import random
import time
import uuid
from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime
from html import escape
from textwrap import dedent
from typing import Dict, List, Tuple

import streamlit as st

# ===== Inlined football_sim.data =====
"""Seed team data for the Football Simulator.

Ratings are intentionally editable. They are a practical 1-100 game scale,
not an official ranking. Continental team lists are seeded from 2025/26 UEFA
league-phase line-ups.
"""



@dataclass(frozen=True)
class Team:
    name: str
    country: str
    league: str
    attack: int
    midfield: int
    defence: int
    star_player: str

    @property
    def overall(self) -> int:
        return round((self.attack * 0.34) + (self.midfield * 0.33) + (self.defence * 0.33))

    def to_dict(self) -> dict:
        data = asdict(self)
        data["overall"] = self.overall
        return data


# Editable, game-balanced ratings. Bigger clubs receive higher baseline ratings.
RATINGS: Dict[str, dict] = {
    # England
    "Arsenal": {"country": "England", "league": "Premier League", "attack": 91, "midfield": 91, "defence": 92, "star_player": "Bukayo Saka"},
    "Aston Villa": {"country": "England", "league": "Premier League", "attack": 84, "midfield": 84, "defence": 83, "star_player": "Ollie Watkins"},
    "Chelsea": {"country": "England", "league": "Premier League", "attack": 87, "midfield": 86, "defence": 84, "star_player": "Cole Palmer"},
    "Crystal Palace": {"country": "England", "league": "Premier League", "attack": 81, "midfield": 80, "defence": 80, "star_player": "Eberechi Eze"},
    "Liverpool": {"country": "England", "league": "Premier League", "attack": 91, "midfield": 88, "defence": 87, "star_player": "Mohamed Salah"},
    "Man City": {"country": "England", "league": "Premier League", "attack": 92, "midfield": 93, "defence": 88, "star_player": "Erling Haaland"},
    "Manchester United": {"country": "England", "league": "Premier League", "attack": 82, "midfield": 80, "defence": 78, "star_player": "Bruno Fernandes"},
    "Newcastle": {"country": "England", "league": "Premier League", "attack": 85, "midfield": 84, "defence": 83, "star_player": "Alexander Isak"},
    "Nottingham Forest": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 79, "defence": 80, "star_player": "Morgan Gibbs-White"},
    "Tottenham": {"country": "England", "league": "Premier League", "attack": 85, "midfield": 83, "defence": 80, "star_player": "Son Heung-min"},
    "AFC Bournemouth": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 80, "defence": 79, "star_player": "Antoine Semenyo"},
    "Brentford": {"country": "England", "league": "Premier League", "attack": 79, "midfield": 79, "defence": 78, "star_player": "Bryan Mbeumo"},
    "Brighton": {"country": "England", "league": "Premier League", "attack": 82, "midfield": 82, "defence": 80, "star_player": "Kaoru Mitoma"},
    "Burnley": {"country": "England", "league": "Premier League", "attack": 73, "midfield": 74, "defence": 75, "star_player": "Josh Brownhill"},
    "Everton": {"country": "England", "league": "Premier League", "attack": 78, "midfield": 78, "defence": 79, "star_player": "Jordan Pickford"},
    "Fulham": {"country": "England", "league": "Premier League", "attack": 79, "midfield": 80, "defence": 78, "star_player": "João Palhinha"},
    "Leeds United": {"country": "England", "league": "Premier League", "attack": 76, "midfield": 77, "defence": 76, "star_player": "Ethan Ampadu"},
    "Sunderland": {"country": "England", "league": "Premier League", "attack": 75, "midfield": 76, "defence": 76, "star_player": "Granit Xhaka"},
    "West Ham United": {"country": "England", "league": "Premier League", "attack": 80, "midfield": 80, "defence": 78, "star_player": "Jarrod Bowen"},
    "Wolverhampton Wanderers": {"country": "England", "league": "Premier League", "attack": 77, "midfield": 77, "defence": 77, "star_player": "Matheus Cunha"},

    # Spain
    "Athletic Club": {"country": "Spain", "league": "La Liga", "attack": 82, "midfield": 82, "defence": 83, "star_player": "Nico Williams"},
    "Atlético Madrid": {"country": "Spain", "league": "La Liga", "attack": 87, "midfield": 86, "defence": 88, "star_player": "Antoine Griezmann"},
    "Barcelona": {"country": "Spain", "league": "La Liga", "attack": 91, "midfield": 90, "defence": 85, "star_player": "Lamine Yamal"},
    "Celta": {"country": "Spain", "league": "La Liga", "attack": 78, "midfield": 77, "defence": 76, "star_player": "Iago Aspas"},
    "Real Betis": {"country": "Spain", "league": "La Liga", "attack": 82, "midfield": 82, "defence": 79, "star_player": "Isco"},
    "Real Madrid": {"country": "Spain", "league": "La Liga", "attack": 94, "midfield": 92, "defence": 90, "star_player": "Kylian Mbappé"},
    "Rayo Vallecano": {"country": "Spain", "league": "La Liga", "attack": 77, "midfield": 77, "defence": 77, "star_player": "Álvaro García"},
    "Villarreal": {"country": "Spain", "league": "La Liga", "attack": 83, "midfield": 82, "defence": 79, "star_player": "Gerard Moreno"},

    # Italy
    "AC Milan": {"country": "Italy", "league": "Serie A", "attack": 86, "midfield": 84, "defence": 82, "star_player": "Rafael Leão"},
    "Atalanta": {"country": "Italy", "league": "Serie A", "attack": 85, "midfield": 84, "defence": 83, "star_player": "Ademola Lookman"},
    "Bologna": {"country": "Italy", "league": "Serie A", "attack": 80, "midfield": 81, "defence": 81, "star_player": "Riccardo Orsolini"},
    "Fiorentina": {"country": "Italy", "league": "Serie A", "attack": 81, "midfield": 81, "defence": 80, "star_player": "Moise Kean"},
    "Inter Milan": {"country": "Italy", "league": "Serie A", "attack": 89, "midfield": 89, "defence": 90, "star_player": "Lautaro Martínez"},
    "Juventus": {"country": "Italy", "league": "Serie A", "attack": 84, "midfield": 83, "defence": 84, "star_player": "Dušan Vlahović"},
    "Napoli": {"country": "Italy", "league": "Serie A", "attack": 87, "midfield": 85, "defence": 84, "star_player": "Khvicha Kvaratskhelia"},
    "Roma": {"country": "Italy", "league": "Serie A", "attack": 83, "midfield": 83, "defence": 81, "star_player": "Paulo Dybala"},

    # Germany
    "Bayer Leverkusen": {"country": "Germany", "league": "Bundesliga", "attack": 88, "midfield": 88, "defence": 86, "star_player": "Florian Wirtz"},
    "Bayern Munich": {"country": "Germany", "league": "Bundesliga", "attack": 92, "midfield": 90, "defence": 87, "star_player": "Harry Kane"},
    "Borussia Dortmund": {"country": "Germany", "league": "Bundesliga", "attack": 85, "midfield": 84, "defence": 81, "star_player": "Julian Brandt"},
    "Frankfurt": {"country": "Germany", "league": "Bundesliga", "attack": 82, "midfield": 81, "defence": 80, "star_player": "Omar Marmoush"},
    "Freiburg": {"country": "Germany", "league": "Bundesliga", "attack": 79, "midfield": 80, "defence": 80, "star_player": "Vincenzo Grifo"},
    "Mainz": {"country": "Germany", "league": "Bundesliga", "attack": 78, "midfield": 78, "defence": 79, "star_player": "Jonathan Burkardt"},
    "RB Leipzig": {"country": "Germany", "league": "Bundesliga", "attack": 85, "midfield": 84, "defence": 82, "star_player": "Xavi Simons"},
    "Stuttgart": {"country": "Germany", "league": "Bundesliga", "attack": 82, "midfield": 82, "defence": 80, "star_player": "Deniz Undav"},

    # France
    "Lille": {"country": "France", "league": "Ligue 1", "attack": 82, "midfield": 82, "defence": 82, "star_player": "Jonathan David"},
    "Lyon": {"country": "France", "league": "Ligue 1", "attack": 83, "midfield": 82, "defence": 80, "star_player": "Alexandre Lacazette"},
    "Marseille": {"country": "France", "league": "Ligue 1", "attack": 83, "midfield": 82, "defence": 80, "star_player": "Pierre-Emerick Aubameyang"},
    "Monaco": {"country": "France", "league": "Ligue 1", "attack": 84, "midfield": 83, "defence": 81, "star_player": "Aleksandr Golovin"},
    "Nice": {"country": "France", "league": "Ligue 1", "attack": 80, "midfield": 80, "defence": 82, "star_player": "Terem Moffi"},
    "Paris Saint-Germain": {"country": "France", "league": "Ligue 1", "attack": 94, "midfield": 91, "defence": 89, "star_player": "Ousmane Dembélé"},
    "Strasbourg": {"country": "France", "league": "Ligue 1", "attack": 78, "midfield": 78, "defence": 77, "star_player": "Emanuel Emegha"},

    # Portugal
    "Benfica": {"country": "Portugal", "league": "Liga Portugal", "attack": 86, "midfield": 85, "defence": 83, "star_player": "Ángel Di María"},
    "Braga": {"country": "Portugal", "league": "Liga Portugal", "attack": 81, "midfield": 80, "defence": 78, "star_player": "Ricardo Horta"},
    "Porto": {"country": "Portugal", "league": "Liga Portugal", "attack": 84, "midfield": 83, "defence": 82, "star_player": "Diogo Costa"},
    "Sporting CP": {"country": "Portugal", "league": "Liga Portugal", "attack": 87, "midfield": 85, "defence": 83, "star_player": "Viktor Gyökeres"},
    "Santa Clara": {"country": "Portugal", "league": "Liga Portugal", "attack": 74, "midfield": 74, "defence": 75, "star_player": "Gabriel Silva"},

    # USA / MLS
    "Inter Miami": {"country": "USA", "league": "MLS", "attack": 83, "midfield": 80, "defence": 74, "star_player": "Lionel Messi"},
    "LAFC": {"country": "USA", "league": "MLS", "attack": 78, "midfield": 76, "defence": 75, "star_player": "Denis Bouanga"},
    "LA Galaxy": {"country": "USA", "league": "MLS", "attack": 77, "midfield": 76, "defence": 74, "star_player": "Riqui Puig"},
    "Columbus Crew": {"country": "USA", "league": "MLS", "attack": 77, "midfield": 77, "defence": 75, "star_player": "Cucho Hernández"},
    "Seattle Sounders": {"country": "USA", "league": "MLS", "attack": 76, "midfield": 76, "defence": 76, "star_player": "Jordan Morris"},
    "Atlanta United": {"country": "USA", "league": "MLS", "attack": 75, "midfield": 75, "defence": 72, "star_player": "Thiago Almada"},

    # Saudi Arabia
    "Al Hilal": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 86, "midfield": 84, "defence": 83, "star_player": "Aleksandar Mitrović"},
    "Al Nassr": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 85, "midfield": 82, "defence": 79, "star_player": "Cristiano Ronaldo"},
    "Al Ittihad": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 83, "midfield": 82, "defence": 79, "star_player": "Karim Benzema"},
    "Al Ahli": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 82, "midfield": 81, "defence": 78, "star_player": "Riyad Mahrez"},
    "Al Qadsiah": {"country": "Saudi Arabia", "league": "Saudi Pro League", "attack": 77, "midfield": 77, "defence": 76, "star_player": "Pierre-Emerick Aubameyang"},

    # Brazil
    "Botafogo": {"country": "Brazil", "league": "Brasileirão", "attack": 80, "midfield": 79, "defence": 79, "star_player": "Tiquinho Soares"},
    "Corinthians": {"country": "Brazil", "league": "Brasileirão", "attack": 78, "midfield": 77, "defence": 77, "star_player": "Memphis Depay"},
    "Flamengo": {"country": "Brazil", "league": "Brasileirão", "attack": 83, "midfield": 82, "defence": 81, "star_player": "Pedro"},
    "Fluminense": {"country": "Brazil", "league": "Brasileirão", "attack": 79, "midfield": 79, "defence": 78, "star_player": "Ganso"},
    "Grêmio": {"country": "Brazil", "league": "Brasileirão", "attack": 78, "midfield": 78, "defence": 77, "star_player": "Cristaldo"},
    "Palmeiras": {"country": "Brazil", "league": "Brasileirão", "attack": 82, "midfield": 82, "defence": 82, "star_player": "Raphael Veiga"},
    "São Paulo": {"country": "Brazil", "league": "Brasileirão", "attack": 79, "midfield": 79, "defence": 79, "star_player": "Lucas Moura"},
}

UCL_2025_26 = [
    "Ajax", "Arsenal", "Atalanta", "Athletic Club", "Atlético Madrid", "Borussia Dortmund",
    "Barcelona", "Bayern Munich", "Benfica", "Bodø/Glimt", "Chelsea", "Club Brugge",
    "Copenhagen", "Frankfurt", "Galatasaray", "Inter Milan", "Juventus", "Kairat Almaty",
    "Bayer Leverkusen", "Liverpool", "Man City", "Marseille", "Monaco", "Napoli",
    "Newcastle", "Olympiacos", "Pafos", "Paris Saint-Germain", "PSV Eindhoven", "Qarabağ",
    "Real Madrid", "Slavia Praha", "Sporting CP", "Tottenham", "Union SG", "Villarreal",
]

UEL_2025_26 = [
    "Aston Villa", "Basel", "Bologna", "Braga", "Brann", "Celta", "Celtic", "Crvena Zvezda",
    "FCSB", "Fenerbahçe", "Ferencváros", "Feyenoord", "Freiburg", "Genk", "GNK Dinamo",
    "Go Ahead Eagles", "Lille", "Ludogorets", "Lyon", "Malmö", "Maccabi Tel-Aviv",
    "Midtjylland", "Nice", "Nottingham Forest", "Panathinaikos", "PAOK", "Porto", "Rangers",
    "Real Betis", "Roma", "Salzburg", "Sturm Graz", "Stuttgart", "Utrecht", "Viktoria Plzeň", "Young Boys",
]

UECL_2025_26 = [
    "Noah", "SK Rapid", "Zrinjski", "Rijeka", "AEK Larnaca", "Omonoia", "Sigma Olomouc", "Sparta Praha",
    "Crystal Palace", "KuPS Kuopio", "Strasbourg", "Mainz", "Lincoln Red Imps", "AEK Athens", "Breidablik",
    "Fiorentina", "Drita", "Hamrun Spartans", "AZ Alkmaar", "Shkëndija", "Jagiellonia Białystok",
    "Lech Poznań", "Legia Warszawa", "Raków Częstochowa", "Shamrock Rovers", "Shelbourne",
    "Universitatea Craiova", "Aberdeen", "Slovan Bratislava", "Celje", "Rayo Vallecano", "Häcken",
    "Lausanne-Sport", "Samsunspor", "Dynamo Kyiv", "Shakhtar Donetsk",
]

CONTINENTAL = {
    "Champions League 2025/26": {"teams": UCL_2025_26, "league_rounds": 8, "kind": "uefa"},
    "Europa League 2025/26": {"teams": UEL_2025_26, "league_rounds": 8, "kind": "uefa"},
    "Conference League 2025/26": {"teams": UECL_2025_26, "league_rounds": 6, "kind": "uefa"},
}

PREMIER_LEAGUE_2025_26 = [
    "Arsenal", "Aston Villa", "AFC Bournemouth", "Brentford", "Brighton", "Burnley",
    "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool",
    "Man City", "Manchester United", "Newcastle", "Nottingham Forest", "Sunderland",
    "Tottenham", "West Ham United", "Wolverhampton Wanderers",
]

FA_CUP_SEED_TEAMS = PREMIER_LEAGUE_2025_26 + [
    "Leicester City", "Ipswich Town", "Southampton", "Norwich City", "Coventry City", "Middlesbrough",
    "West Brom", "Sheffield United", "Sheffield Wednesday", "Derby County", "Blackburn Rovers",
    "Stoke City", "Queens Park Rangers", "Portsmouth", "Bristol City", "Watford", "Millwall",
    "Hull City", "Swansea City", "Cardiff City", "Preston North End", "Wrexham", "Plymouth Argyle",
    "Birmingham City", "Bolton Wanderers", "Charlton Athletic", "Reading", "Barnsley", "Blackpool",
    "Peterborough United", "Wigan Athletic", "Rotherham United", "Wycombe Wanderers", "Oxford United",
    "Lincoln City", "Port Vale", "Stockport County", "Bradford City", "Mansfield Town", "Walsall",
    "Doncaster Rovers", "Notts County", "Gillingham", "Tranmere Rovers", "AFC Wimbledon",
    "Swindon Town", "Newport County", "Grimsby Town", "Carlisle United", "Salford City",
    "Harrogate Town", "Accrington Stanley", "Barrow", "Morecambe", "Crewe Alexandra",
    "Chesterfield", "Bromley", "Colchester United", "Cheltenham Town", "Exeter City", "Leyton Orient",
]

DOMESTIC = {
    "Premier League": {
        "teams": PREMIER_LEAGUE_2025_26,
        "kind": "league",
        "format_note": "20 clubs, 38 matchdays, home and away fixtures. Ratings are editable game estimates.",
    },
    "FA Cup": {
        "teams": FA_CUP_SEED_TEAMS[:64],
        "kind": "knockout",
        "format_note": "64-team single-match knockout with random draws, extra time and penalties. Giant-killing is possible but weighted by team strength.",
    },
}

COUNTRY_DEFAULTS = {
    "England": 82, "Spain": 81, "Italy": 81, "Germany": 80, "France": 79, "Portugal": 78,
    "Netherlands": 76, "Turkey": 76, "Scotland": 73, "Belgium": 73, "Brazil": 77, "USA": 74,
    "Saudi Arabia": 78, "Greece": 72, "Switzerland": 71, "Austria": 71, "Czechia": 70, "Ukraine": 72,
}

TEAM_COUNTRY_HINTS = {
    "Ajax": ("Netherlands", "Eredivisie"), "Bodø/Glimt": ("Norway", "Eliteserien"), "Club Brugge": ("Belgium", "Belgian Pro League"),
    "Copenhagen": ("Denmark", "Superliga"), "Galatasaray": ("Turkey", "Süper Lig"), "Kairat Almaty": ("Kazakhstan", "Premier League"),
    "Olympiacos": ("Greece", "Super League Greece"), "Pafos": ("Cyprus", "First Division"), "PSV Eindhoven": ("Netherlands", "Eredivisie"),
    "Qarabağ": ("Azerbaijan", "Premier League"), "Slavia Praha": ("Czechia", "Czech First League"), "Union SG": ("Belgium", "Belgian Pro League"),
    "Basel": ("Switzerland", "Swiss Super League"), "Brann": ("Norway", "Eliteserien"), "Celtic": ("Scotland", "Scottish Premiership"),
    "Crvena Zvezda": ("Serbia", "Serbian SuperLiga"), "FCSB": ("Romania", "Liga I"), "Fenerbahçe": ("Turkey", "Süper Lig"),
    "Ferencváros": ("Hungary", "NB I"), "Feyenoord": ("Netherlands", "Eredivisie"), "Genk": ("Belgium", "Belgian Pro League"),
    "GNK Dinamo": ("Croatia", "HNL"), "Go Ahead Eagles": ("Netherlands", "Eredivisie"), "Ludogorets": ("Bulgaria", "First League"),
    "Malmö": ("Sweden", "Allsvenskan"), "Maccabi Tel-Aviv": ("Israel", "Premier League"), "Midtjylland": ("Denmark", "Superliga"),
    "Panathinaikos": ("Greece", "Super League Greece"), "PAOK": ("Greece", "Super League Greece"), "Rangers": ("Scotland", "Scottish Premiership"),
    "Salzburg": ("Austria", "Bundesliga"), "Sturm Graz": ("Austria", "Bundesliga"), "Utrecht": ("Netherlands", "Eredivisie"),
    "Viktoria Plzeň": ("Czechia", "Czech First League"), "Young Boys": ("Switzerland", "Swiss Super League"),
    "Noah": ("Armenia", "Premier League"), "SK Rapid": ("Austria", "Bundesliga"), "Zrinjski": ("Bosnia and Herzegovina", "Premier League"),
    "Rijeka": ("Croatia", "HNL"), "AEK Larnaca": ("Cyprus", "First Division"), "Omonoia": ("Cyprus", "First Division"),
    "Sigma Olomouc": ("Czechia", "Czech First League"), "Sparta Praha": ("Czechia", "Czech First League"), "KuPS Kuopio": ("Finland", "Veikkausliiga"),
    "Lincoln Red Imps": ("Gibraltar", "National League"), "AEK Athens": ("Greece", "Super League Greece"), "Breidablik": ("Iceland", "Besta deild karla"),
    "Drita": ("Kosovo", "Superleague"), "Hamrun Spartans": ("Malta", "Premier League"), "AZ Alkmaar": ("Netherlands", "Eredivisie"),
    "Shkëndija": ("North Macedonia", "First League"), "Jagiellonia Białystok": ("Poland", "Ekstraklasa"), "Lech Poznań": ("Poland", "Ekstraklasa"),
    "Legia Warszawa": ("Poland", "Ekstraklasa"), "Raków Częstochowa": ("Poland", "Ekstraklasa"), "Shamrock Rovers": ("Republic of Ireland", "Premier Division"),
    "Shelbourne": ("Republic of Ireland", "Premier Division"), "Universitatea Craiova": ("Romania", "Liga I"), "Aberdeen": ("Scotland", "Scottish Premiership"),
    "Slovan Bratislava": ("Slovakia", "Super Liga"), "Celje": ("Slovenia", "PrvaLiga"), "Häcken": ("Sweden", "Allsvenskan"),
    "Lausanne-Sport": ("Switzerland", "Swiss Super League"), "Samsunspor": ("Turkey", "Süper Lig"), "Dynamo Kyiv": ("Ukraine", "Premier League"),
    "Shakhtar Donetsk": ("Ukraine", "Premier League"),
}


TEAM_COUNTRY_HINTS.update({
    "Leicester City": ("England", "Championship"), "Ipswich Town": ("England", "Championship"),
    "Southampton": ("England", "Championship"), "Norwich City": ("England", "Championship"),
    "Coventry City": ("England", "Championship"), "Middlesbrough": ("England", "Championship"),
    "West Brom": ("England", "Championship"), "Sheffield United": ("England", "Championship"),
    "Sheffield Wednesday": ("England", "Championship"), "Derby County": ("England", "Championship"),
    "Blackburn Rovers": ("England", "Championship"), "Stoke City": ("England", "Championship"),
    "Queens Park Rangers": ("England", "Championship"), "Portsmouth": ("England", "Championship"),
    "Bristol City": ("England", "Championship"), "Watford": ("England", "Championship"),
    "Millwall": ("England", "Championship"), "Hull City": ("England", "Championship"),
    "Swansea City": ("Wales", "Championship"), "Cardiff City": ("Wales", "Championship"),
    "Preston North End": ("England", "Championship"), "Wrexham": ("Wales", "League One"),
    "Plymouth Argyle": ("England", "Championship"), "Birmingham City": ("England", "League One"),
    "Bolton Wanderers": ("England", "League One"), "Charlton Athletic": ("England", "League One"),
    "Reading": ("England", "League One"), "Barnsley": ("England", "League One"),
    "Blackpool": ("England", "League One"), "Peterborough United": ("England", "League One"),
    "Wigan Athletic": ("England", "League One"), "Rotherham United": ("England", "League One"),
    "Wycombe Wanderers": ("England", "League One"), "Oxford United": ("England", "Championship"),
    "Lincoln City": ("England", "League One"), "Port Vale": ("England", "League Two"),
    "Stockport County": ("England", "League One"), "Bradford City": ("England", "League Two"),
    "Mansfield Town": ("England", "League One"), "Walsall": ("England", "League Two"),
    "Doncaster Rovers": ("England", "League Two"), "Notts County": ("England", "League Two"),
    "Gillingham": ("England", "League Two"), "Tranmere Rovers": ("England", "League Two"),
    "AFC Wimbledon": ("England", "League Two"), "Swindon Town": ("England", "League Two"),
    "Newport County": ("Wales", "League Two"), "Grimsby Town": ("England", "League Two"),
    "Carlisle United": ("England", "League Two"), "Salford City": ("England", "League Two"),
    "Harrogate Town": ("England", "League Two"), "Accrington Stanley": ("England", "League Two"),
    "Barrow": ("England", "League Two"), "Morecambe": ("England", "League Two"),
    "Crewe Alexandra": ("England", "League Two"), "Chesterfield": ("England", "League Two"),
    "Bromley": ("England", "League Two"), "Colchester United": ("England", "League Two"),
    "Cheltenham Town": ("England", "League Two"), "Exeter City": ("England", "League One"),
    "Leyton Orient": ("England", "League One"),
})



# ---------------------------------------------------------------------------
# International mode data
# ---------------------------------------------------------------------------
# Player ratings are a game scale only. They are intentionally close-feel,
# editable estimates, not official EA/FC, FIFA, Opta or scouting ratings.
# Squads are representative real-player cores so goals/assists/cards feel real.

def p(name: str, pos: str, rating: int) -> dict:
    return {"name": name, "position": pos, "rating": rating}


# Representative club squad cores for the domestic modes. These are editable game
# estimates so the simulator can pick real-feeling scorers/assisters instead of
# generic generated names for Premier League and FA Cup teams.
CLUB_SQUADS: Dict[str, List[dict]] = {
    "Arsenal": [p("Bukayo Saka", "RW", 89), p("Martin Ødegaard", "AM", 89), p("Kai Havertz", "ST", 84), p("Declan Rice", "DM", 89), p("William Saliba", "CB", 90), p("Gabriel Magalhães", "CB", 87), p("David Raya", "GK", 84), p("Gabriel Martinelli", "LW", 84)],
    "Aston Villa": [p("Ollie Watkins", "ST", 86), p("Morgan Rogers", "AM", 82), p("Youri Tielemans", "CM", 82), p("John McGinn", "CM", 80), p("Pau Torres", "CB", 84), p("Emiliano Martínez", "GK", 88), p("Leon Bailey", "RW", 81), p("Amadou Onana", "DM", 82)],
    "AFC Bournemouth": [p("Antoine Semenyo", "ST", 82), p("Justin Kluivert", "AM", 80), p("Evanilson", "ST", 81), p("Ryan Christie", "CM", 78), p("Lewis Cook", "CM", 78), p("Illia Zabarnyi", "CB", 82), p("Milos Kerkez", "LB", 82), p("Kepa Arrizabalaga", "GK", 81)],
    "Brentford": [p("Bryan Mbeumo", "RW", 84), p("Yoane Wissa", "ST", 82), p("Kevin Schade", "LW", 78), p("Christian Nørgaard", "DM", 80), p("Mikkel Damsgaard", "AM", 78), p("Nathan Collins", "CB", 80), p("Ethan Pinnock", "CB", 78), p("Mark Flekken", "GK", 78)],
    "Brighton": [p("Kaoru Mitoma", "LW", 84), p("João Pedro", "ST", 83), p("Georginio Rutter", "AM", 80), p("Carlos Baleba", "CM", 81), p("Yankuba Minteh", "RW", 79), p("Lewis Dunk", "CB", 80), p("Jan Paul van Hecke", "CB", 79), p("Bart Verbruggen", "GK", 79)],
    "Burnley": [p("Josh Brownhill", "CM", 76), p("Lyle Foster", "ST", 78), p("Zeki Amdouni", "FW", 77), p("Sander Berge", "CM", 80), p("Maxime Estève", "CB", 77), p("James Trafford", "GK", 76), p("Connor Roberts", "RB", 75), p("Jacob Bruun Larsen", "LW", 76)],
    "Chelsea": [p("Cole Palmer", "AM", 89), p("Nicolas Jackson", "ST", 82), p("Christopher Nkunku", "FW", 84), p("Enzo Fernández", "CM", 86), p("Moisés Caicedo", "DM", 86), p("Reece James", "RB", 84), p("Levi Colwill", "CB", 82), p("Robert Sánchez", "GK", 80)],
    "Crystal Palace": [p("Eberechi Eze", "AM", 85), p("Jean-Philippe Mateta", "ST", 82), p("Ismaïla Sarr", "RW", 80), p("Adam Wharton", "CM", 82), p("Jefferson Lerma", "DM", 79), p("Marc Guéhi", "CB", 84), p("Daniel Muñoz", "RB", 80), p("Dean Henderson", "GK", 79)],
    "Everton": [p("Jordan Pickford", "GK", 84), p("Dominic Calvert-Lewin", "ST", 79), p("Dwight McNeil", "LW", 80), p("Iliman Ndiaye", "AM", 80), p("James Tarkowski", "CB", 80), p("Jarrad Branthwaite", "CB", 82), p("Idrissa Gueye", "DM", 79), p("Abdoulaye Doucouré", "CM", 78)],
    "Fulham": [p("Raúl Jiménez", "ST", 79), p("Alex Iwobi", "AM", 80), p("Andreas Pereira", "CM", 80), p("João Palhinha", "DM", 85), p("Emile Smith Rowe", "AM", 80), p("Antonee Robinson", "LB", 81), p("Bernd Leno", "GK", 82), p("Calvin Bassey", "CB", 79)],
    "Leeds United": [p("Ethan Ampadu", "DM", 80), p("Wilfried Gnonto", "LW", 79), p("Joel Piroe", "ST", 78), p("Daniel James", "RW", 78), p("Pascal Struijk", "CB", 78), p("Illan Meslier", "GK", 77), p("Junior Firpo", "LB", 77), p("Brenden Aaronson", "AM", 77)],
    "Liverpool": [p("Mohamed Salah", "RW", 91), p("Darwin Núñez", "ST", 84), p("Luis Díaz", "LW", 86), p("Dominik Szoboszlai", "AM", 87), p("Alexis Mac Allister", "CM", 87), p("Virgil van Dijk", "CB", 90), p("Trent Alexander-Arnold", "RB", 86), p("Alisson", "GK", 89)],
    "Man City": [p("Erling Haaland", "ST", 94), p("Phil Foden", "AM", 88), p("Bernardo Silva", "CM", 88), p("Rodri", "DM", 94), p("Kevin De Bruyne", "CM", 89), p("Rúben Dias", "CB", 88), p("Joško Gvardiol", "CB", 86), p("Ederson", "GK", 88)],
    "Manchester United": [p("Bruno Fernandes", "AM", 88), p("Rasmus Højlund", "ST", 82), p("Marcus Rashford", "LW", 82), p("Alejandro Garnacho", "LW", 81), p("Kobbie Mainoo", "CM", 80), p("Lisandro Martínez", "CB", 84), p("Noussair Mazraoui", "RB", 81), p("André Onana", "GK", 84)],
    "Newcastle": [p("Alexander Isak", "ST", 88), p("Anthony Gordon", "LW", 84), p("Bruno Guimarães", "CM", 86), p("Sandro Tonali", "CM", 84), p("Joelinton", "CM", 82), p("Sven Botman", "CB", 83), p("Kieran Trippier", "RB", 82), p("Nick Pope", "GK", 82)],
    "Nottingham Forest": [p("Morgan Gibbs-White", "AM", 82), p("Chris Wood", "ST", 81), p("Callum Hudson-Odoi", "LW", 79), p("Anthony Elanga", "RW", 80), p("Nicolás Domínguez", "CM", 79), p("Murillo", "CB", 82), p("Nikola Milenković", "CB", 80), p("Matz Sels", "GK", 79)],
    "Sunderland": [p("Granit Xhaka", "DM", 86), p("Jobe Bellingham", "CM", 79), p("Wilson Isidor", "ST", 77), p("Patrick Roberts", "RW", 76), p("Dan Ballard", "CB", 78), p("Anthony Patterson", "GK", 76), p("Trai Hume", "RB", 76), p("Chris Rigg", "CM", 76)],
    "Tottenham": [p("Son Heung-min", "LW", 87), p("James Maddison", "AM", 84), p("Dejan Kulusevski", "RW", 83), p("Dominic Solanke", "ST", 82), p("Rodrigo Bentancur", "CM", 82), p("Cristian Romero", "CB", 86), p("Micky van de Ven", "CB", 84), p("Guglielmo Vicario", "GK", 83)],
    "West Ham United": [p("Jarrod Bowen", "RW", 84), p("Lucas Paquetá", "AM", 84), p("Mohammed Kudus", "RW", 83), p("Tomáš Souček", "CM", 80), p("Edson Álvarez", "DM", 81), p("Max Kilman", "CB", 80), p("Aaron Wan-Bissaka", "RB", 80), p("Alphonse Areola", "GK", 80)],
    "Wolverhampton Wanderers": [p("Matheus Cunha", "FW", 84), p("Jørgen Strand Larsen", "ST", 80), p("Hwang Hee-chan", "LW", 80), p("João Gomes", "CM", 80), p("Mario Lemina", "DM", 79), p("Rayan Aït-Nouri", "LB", 81), p("Toti Gomes", "CB", 78), p("José Sá", "GK", 80)],
    "Leicester City": [p("Jamie Vardy", "ST", 78), p("Stephy Mavididi", "LW", 77), p("Harry Winks", "CM", 77), p("Wout Faes", "CB", 77), p("Mads Hermansen", "GK", 77)],
    "Ipswich Town": [p("Liam Delap", "ST", 78), p("Omari Hutchinson", "RW", 78), p("Leif Davis", "LB", 77), p("Sam Morsy", "CM", 76), p("Arijanet Muric", "GK", 76)],
    "Southampton": [p("Adam Armstrong", "ST", 77), p("Mateus Fernandes", "CM", 77), p("Taylor Harwood-Bellis", "CB", 77), p("Kyle Walker-Peters", "RB", 78), p("Aaron Ramsdale", "GK", 80)],
    "Coventry City": [p("Haji Wright", "ST", 77), p("Ellis Simms", "ST", 76), p("Ben Sheaf", "CM", 76), p("Milan van Ewijk", "RB", 75), p("Bobby Thomas", "CB", 75)],
    "Plymouth Argyle": [p("Morgan Whittaker", "RW", 76), p("Ryan Hardie", "ST", 74), p("Adam Randell", "CM", 73), p("Bali Mumba", "WB", 74), p("Conor Hazard", "GK", 72)],
}


NATIONAL_RATINGS: Dict[str, dict] = {
    "Argentina": {"attack": 93, "midfield": 90, "defence": 88, "star_player": "Lionel Messi", "confederation": "CONMEBOL"},
    "France": {"attack": 94, "midfield": 91, "defence": 91, "star_player": "Kylian Mbappé", "confederation": "UEFA"},
    "England": {"attack": 92, "midfield": 91, "defence": 88, "star_player": "Harry Kane", "confederation": "UEFA"},
    "Spain": {"attack": 91, "midfield": 94, "defence": 89, "star_player": "Lamine Yamal", "confederation": "UEFA"},
    "Brazil": {"attack": 92, "midfield": 88, "defence": 87, "star_player": "Vinícius Júnior", "confederation": "CONMEBOL"},
    "Portugal": {"attack": 91, "midfield": 90, "defence": 88, "star_player": "Cristiano Ronaldo", "confederation": "UEFA"},
    "Netherlands": {"attack": 87, "midfield": 88, "defence": 90, "star_player": "Virgil van Dijk", "confederation": "UEFA"},
    "Germany": {"attack": 89, "midfield": 91, "defence": 87, "star_player": "Jamal Musiala", "confederation": "UEFA"},
    "Belgium": {"attack": 87, "midfield": 88, "defence": 83, "star_player": "Kevin De Bruyne", "confederation": "UEFA"},
    "Italy": {"attack": 84, "midfield": 87, "defence": 88, "star_player": "Gianluigi Donnarumma", "confederation": "UEFA"},
    "Croatia": {"attack": 84, "midfield": 88, "defence": 84, "star_player": "Luka Modrić", "confederation": "UEFA"},
    "Uruguay": {"attack": 86, "midfield": 87, "defence": 86, "star_player": "Federico Valverde", "confederation": "CONMEBOL"},
    "Colombia": {"attack": 86, "midfield": 84, "defence": 82, "star_player": "Luis Díaz", "confederation": "CONMEBOL"},
    "Ecuador": {"attack": 81, "midfield": 82, "defence": 84, "star_player": "Moisés Caicedo", "confederation": "CONMEBOL"},
    "Paraguay": {"attack": 77, "midfield": 78, "defence": 79, "star_player": "Miguel Almirón", "confederation": "CONMEBOL"},
    "Morocco": {"attack": 84, "midfield": 84, "defence": 86, "star_player": "Achraf Hakimi", "confederation": "CAF"},
    "United States": {"attack": 81, "midfield": 82, "defence": 79, "star_player": "Christian Pulisic", "confederation": "CONCACAF"},
    "Mexico": {"attack": 80, "midfield": 80, "defence": 79, "star_player": "Santiago Giménez", "confederation": "CONCACAF"},
    "Canada": {"attack": 80, "midfield": 78, "defence": 77, "star_player": "Alphonso Davies", "confederation": "CONCACAF"},
    "Japan": {"attack": 83, "midfield": 84, "defence": 82, "star_player": "Takefusa Kubo", "confederation": "AFC"},
    "South Korea": {"attack": 82, "midfield": 81, "defence": 81, "star_player": "Son Heung-min", "confederation": "AFC"},
    "Australia": {"attack": 77, "midfield": 77, "defence": 78, "star_player": "Harry Souttar", "confederation": "AFC"},
    "Iran": {"attack": 80, "midfield": 79, "defence": 78, "star_player": "Mehdi Taremi", "confederation": "AFC"},
    "Saudi Arabia": {"attack": 78, "midfield": 77, "defence": 76, "star_player": "Salem Al-Dawsari", "confederation": "AFC"},
    "Qatar": {"attack": 77, "midfield": 76, "defence": 75, "star_player": "Akram Afif", "confederation": "AFC"},
    "Uzbekistan": {"attack": 76, "midfield": 76, "defence": 77, "star_player": "Eldor Shomurodov", "confederation": "AFC"},
    "Jordan": {"attack": 75, "midfield": 74, "defence": 73, "star_player": "Mousa Al-Taamari", "confederation": "AFC"},
    "New Zealand": {"attack": 74, "midfield": 73, "defence": 74, "star_player": "Chris Wood", "confederation": "OFC"},
    "Senegal": {"attack": 84, "midfield": 82, "defence": 84, "star_player": "Sadio Mané", "confederation": "CAF"},
    "Egypt": {"attack": 82, "midfield": 79, "defence": 78, "star_player": "Mohamed Salah", "confederation": "CAF"},
    "Algeria": {"attack": 80, "midfield": 80, "defence": 78, "star_player": "Riyad Mahrez", "confederation": "CAF"},
    "Tunisia": {"attack": 75, "midfield": 76, "defence": 77, "star_player": "Ellyes Skhiri", "confederation": "CAF"},
    "Ghana": {"attack": 78, "midfield": 78, "defence": 76, "star_player": "Mohammed Kudus", "confederation": "CAF"},
    "Cape Verde": {"attack": 73, "midfield": 72, "defence": 72, "star_player": "Ryan Mendes", "confederation": "CAF"},
    "South Africa": {"attack": 74, "midfield": 75, "defence": 76, "star_player": "Lyle Foster", "confederation": "CAF"},
    "Ivory Coast": {"attack": 81, "midfield": 80, "defence": 79, "star_player": "Franck Kessié", "confederation": "CAF"},
    "Cameroon": {"attack": 79, "midfield": 78, "defence": 79, "star_player": "André Onana", "confederation": "CAF"},
    "Austria": {"attack": 82, "midfield": 84, "defence": 82, "star_player": "Marcel Sabitzer", "confederation": "UEFA"},
    "Norway": {"attack": 86, "midfield": 84, "defence": 78, "star_player": "Erling Haaland", "confederation": "UEFA"},
    "Scotland": {"attack": 78, "midfield": 81, "defence": 79, "star_player": "Scott McTominay", "confederation": "UEFA"},
    "Turkey": {"attack": 83, "midfield": 84, "defence": 80, "star_player": "Arda Güler", "confederation": "UEFA"},
    "Czech Republic": {"attack": 79, "midfield": 80, "defence": 80, "star_player": "Patrik Schick", "confederation": "UEFA"},
    "Switzerland": {"attack": 80, "midfield": 84, "defence": 83, "star_player": "Granit Xhaka", "confederation": "UEFA"},
    "Denmark": {"attack": 81, "midfield": 83, "defence": 82, "star_player": "Rasmus Højlund", "confederation": "UEFA"},
    "Poland": {"attack": 80, "midfield": 78, "defence": 77, "star_player": "Robert Lewandowski", "confederation": "UEFA"},
    "Serbia": {"attack": 82, "midfield": 80, "defence": 79, "star_player": "Dušan Vlahović", "confederation": "UEFA"},
    "Iraq": {"attack": 74, "midfield": 73, "defence": 72, "star_player": "Aymen Hussein", "confederation": "AFC"},
    "Panama": {"attack": 74, "midfield": 74, "defence": 73, "star_player": "Adalberto Carrasquilla", "confederation": "CONCACAF"},
    "Curaçao": {"attack": 72, "midfield": 72, "defence": 71, "star_player": "Juninho Bacuna", "confederation": "CONCACAF"},
    "Haiti": {"attack": 73, "midfield": 72, "defence": 71, "star_player": "Duckens Nazon", "confederation": "CONCACAF"},
    "Hungary": {"attack": 80, "midfield": 81, "defence": 78, "star_player": "Dominik Szoboszlai", "confederation": "UEFA"},
    "Albania": {"attack": 75, "midfield": 75, "defence": 76, "star_player": "Armando Broja", "confederation": "UEFA"},
    "Slovenia": {"attack": 78, "midfield": 77, "defence": 79, "star_player": "Benjamin Šeško", "confederation": "UEFA"},
    "Romania": {"attack": 76, "midfield": 77, "defence": 77, "star_player": "Radu Drăgușin", "confederation": "UEFA"},
    "Slovakia": {"attack": 76, "midfield": 78, "defence": 80, "star_player": "Milan Škriniar", "confederation": "UEFA"},
    "Ukraine": {"attack": 81, "midfield": 80, "defence": 79, "star_player": "Artem Dovbyk", "confederation": "UEFA"},
    "Georgia": {"attack": 78, "midfield": 75, "defence": 74, "star_player": "Khvicha Kvaratskhelia", "confederation": "UEFA"},
}

NATIONAL_SQUADS: Dict[str, List[dict]] = {
    "Argentina": [p("Lionel Messi", "RW", 94), p("Lautaro Martínez", "ST", 89), p("Julián Álvarez", "ST", 86), p("Alexis Mac Allister", "CM", 87), p("Enzo Fernández", "CM", 86), p("Rodrigo De Paul", "CM", 85), p("Cristian Romero", "CB", 87), p("Emiliano Martínez", "GK", 88)],
    "France": [p("Kylian Mbappé", "ST", 95), p("Antoine Griezmann", "AM", 88), p("Ousmane Dembélé", "RW", 88), p("Aurélien Tchouaméni", "DM", 88), p("Eduardo Camavinga", "CM", 87), p("William Saliba", "CB", 90), p("Theo Hernández", "LB", 87), p("Mike Maignan", "GK", 89)],
    "England": [p("Harry Kane", "ST", 92), p("Jude Bellingham", "AM", 93), p("Bukayo Saka", "RW", 89), p("Phil Foden", "AM", 88), p("Declan Rice", "DM", 89), p("Cole Palmer", "AM", 88), p("John Stones", "CB", 86), p("Jordan Pickford", "GK", 84)],
    "Spain": [p("Lamine Yamal", "RW", 90), p("Pedri", "CM", 88), p("Nico Williams", "LW", 86), p("Rodri", "DM", 94), p("Dani Olmo", "AM", 86), p("Dani Carvajal", "RB", 86), p("Marc Cucurella", "LB", 84), p("Unai Simón", "GK", 85)],
    "Brazil": [p("Vinícius Júnior", "LW", 92), p("Rodrygo", "RW", 88), p("Neymar", "AM", 88), p("Raphinha", "RW", 87), p("Bruno Guimarães", "CM", 86), p("Casemiro", "DM", 84), p("Marquinhos", "CB", 87), p("Alisson", "GK", 89)],
    "Portugal": [p("Cristiano Ronaldo", "ST", 89), p("Bernardo Silva", "AM", 88), p("Bruno Fernandes", "AM", 88), p("Vitinha", "CM", 88), p("Rafael Leão", "LW", 86), p("João Félix", "FW", 83), p("Rúben Dias", "CB", 90), p("Diogo Costa", "GK", 86)],
    "Netherlands": [p("Virgil van Dijk", "CB", 90), p("Frenkie de Jong", "CM", 88), p("Cody Gakpo", "LW", 85), p("Memphis Depay", "ST", 83), p("Xavi Simons", "AM", 84), p("Ryan Gravenberch", "CM", 85), p("Matthijs de Ligt", "CB", 85), p("Bart Verbruggen", "GK", 82)],
    "Germany": [p("Jamal Musiala", "AM", 91), p("Florian Wirtz", "AM", 91), p("Kai Havertz", "ST", 85), p("Joshua Kimmich", "DM", 88), p("Leroy Sané", "RW", 86), p("Antonio Rüdiger", "CB", 88), p("Nico Schlotterbeck", "CB", 84), p("Marc-André ter Stegen", "GK", 87)],
    "Belgium": [p("Kevin De Bruyne", "CM", 91), p("Romelu Lukaku", "ST", 86), p("Jérémy Doku", "LW", 84), p("Youri Tielemans", "CM", 83), p("Amadou Onana", "DM", 84), p("Loïs Openda", "ST", 84), p("Thibaut Courtois", "GK", 90), p("Arthur Theate", "CB", 81)],
    "Italy": [p("Gianluigi Donnarumma", "GK", 89), p("Nicolò Barella", "CM", 88), p("Alessandro Bastoni", "CB", 88), p("Federico Chiesa", "RW", 84), p("Sandro Tonali", "CM", 86), p("Federico Dimarco", "LB", 86), p("Mateo Retegui", "ST", 82), p("Davide Frattesi", "CM", 82)],
    "Croatia": [p("Luka Modrić", "CM", 87), p("Mateo Kovačić", "CM", 86), p("Joško Gvardiol", "CB", 88), p("Ivan Perišić", "LW", 82), p("Andrej Kramarić", "FW", 83), p("Marcelo Brozović", "DM", 84), p("Dominik Livaković", "GK", 82), p("Lovro Majer", "AM", 81)],
    "Uruguay": [p("Federico Valverde", "CM", 91), p("Darwin Núñez", "ST", 85), p("Ronald Araújo", "CB", 88), p("Rodrigo Bentancur", "CM", 84), p("Manuel Ugarte", "DM", 84), p("Nicolás de la Cruz", "CM", 82), p("José Giménez", "CB", 84), p("Sergio Rochet", "GK", 80)],
    "Colombia": [p("Luis Díaz", "LW", 88), p("James Rodríguez", "AM", 84), p("Jefferson Lerma", "DM", 81), p("Jhon Durán", "ST", 83), p("Davinson Sánchez", "CB", 82), p("Daniel Muñoz", "RB", 82), p("Juan Cuadrado", "RW", 80), p("Camilo Vargas", "GK", 80)],
    "Ecuador": [p("Moisés Caicedo", "DM", 86), p("Piero Hincapié", "CB", 84), p("Pervis Estupiñán", "LB", 82), p("Willian Pacho", "CB", 83), p("Kendry Páez", "AM", 80), p("Enner Valencia", "ST", 80), p("Gonzalo Plata", "RW", 78), p("Alexander Domínguez", "GK", 76)],
    "Paraguay": [p("Miguel Almirón", "AM", 80), p("Julio Enciso", "FW", 80), p("Ramón Sosa", "LW", 78), p("Omar Alderete", "CB", 78), p("Gustavo Gómez", "CB", 80), p("Mathías Villasanti", "CM", 78), p("Diego Gómez", "CM", 79), p("Roberto Fernández", "GK", 74)],
    "Morocco": [p("Achraf Hakimi", "RB", 88), p("Yassine Bounou", "GK", 86), p("Hakim Ziyech", "RW", 83), p("Azzedine Ounahi", "CM", 82), p("Youssef En-Nesyri", "ST", 83), p("Sofyan Amrabat", "DM", 82), p("Noussair Mazraoui", "FB", 84), p("Nayef Aguerd", "CB", 82)],
    "United States": [p("Christian Pulisic", "LW", 86), p("Weston McKennie", "CM", 82), p("Giovanni Reyna", "AM", 81), p("Tyler Adams", "DM", 80), p("Yunus Musah", "CM", 79), p("Folarin Balogun", "ST", 81), p("Sergiño Dest", "RB", 80), p("Matt Turner", "GK", 78)],
    "Mexico": [p("Edson Álvarez", "DM", 82), p("Santiago Giménez", "ST", 83), p("Raúl Jiménez", "ST", 80), p("Hirving Lozano", "RW", 81), p("Alexis Vega", "LW", 78), p("César Montes", "CB", 79), p("Jorge Sánchez", "RB", 77), p("Guillermo Ochoa", "GK", 78)],
    "Canada": [p("Alphonso Davies", "LB", 86), p("Jonathan David", "ST", 84), p("Tajon Buchanan", "RW", 79), p("Stephen Eustáquio", "CM", 79), p("Cyle Larin", "ST", 78), p("Ismaël Koné", "CM", 78), p("Moïse Bombito", "CB", 77), p("Maxime Crépeau", "GK", 76)],
    "Japan": [p("Takefusa Kubo", "RW", 85), p("Kaoru Mitoma", "LW", 84), p("Takumi Minamino", "AM", 81), p("Wataru Endo", "DM", 82), p("Daichi Kamada", "AM", 81), p("Takehiro Tomiyasu", "CB", 84), p("Junya Ito", "RW", 80), p("Zion Suzuki", "GK", 78)],
    "South Korea": [p("Son Heung-min", "LW", 88), p("Lee Kang-in", "AM", 83), p("Kim Min-jae", "CB", 88), p("Hwang Hee-chan", "FW", 81), p("Hwang In-beom", "CM", 80), p("Cho Gue-sung", "ST", 78), p("Seol Young-woo", "FB", 77), p("Jo Hyeon-woo", "GK", 77)],
    "Australia": [p("Harry Souttar", "CB", 78), p("Jackson Irvine", "CM", 78), p("Craig Goodwin", "LW", 76), p("Conor Metcalfe", "CM", 75), p("Mitchell Duke", "ST", 75), p("Aziz Behich", "LB", 75), p("Mathew Ryan", "GK", 78), p("Keanu Baccus", "CM", 75)],
    "Iran": [p("Mehdi Taremi", "ST", 83), p("Sardar Azmoun", "ST", 81), p("Alireza Jahanbakhsh", "RW", 79), p("Ali Gholizadeh", "AM", 77), p("Saeid Ezatolahi", "DM", 77), p("Hossein Hosseini", "GK", 76), p("Alireza Beiranvand", "GK", 77), p("Sadegh Moharrami", "RB", 76)],
    "Saudi Arabia": [p("Salem Al-Dawsari", "LW", 80), p("Firas Al-Buraikan", "ST", 77), p("Mohamed Kanno", "CM", 77), p("Salman Al-Faraj", "CM", 76), p("Mohammed Al-Owais", "GK", 76), p("Sultan Al-Ghannam", "RB", 76), p("Hassan Tambakti", "CB", 76), p("Saleh Al-Shehri", "ST", 75)],
    "Qatar": [p("Akram Afif", "LW", 80), p("Almoez Ali", "ST", 78), p("Hassan Al-Haydos", "AM", 76), p("Pedro Miguel", "RB", 75), p("Meshaal Barsham", "GK", 76), p("Bassam Al-Rawi", "CB", 75), p("Abdulaziz Hatem", "CM", 75), p("Tarek Salman", "CB", 74)],
    "Uzbekistan": [p("Eldor Shomurodov", "ST", 79), p("Abdukodir Khusanov", "CB", 80), p("Abbosbek Fayzullaev", "AM", 78), p("Jaloliddin Masharipov", "LW", 76), p("Oston Urunov", "AM", 75), p("Utkir Yusupov", "GK", 74), p("Odiljon Khamrobekov", "DM", 74), p("Sherzod Nasrullayev", "LB", 74)],
    "Jordan": [p("Mousa Al-Taamari", "RW", 79), p("Yazan Al-Naimat", "ST", 77), p("Nizar Al-Rashdan", "CM", 75), p("Noor Al-Rawabdeh", "DM", 74), p("Yazid Abu Laila", "GK", 74), p("Ali Olwan", "FW", 74), p("Baha Faisal", "ST", 73), p("Salim Obaid", "CB", 72)],
    "New Zealand": [p("Chris Wood", "ST", 81), p("Sarpreet Singh", "AM", 75), p("Matthew Garbett", "CM", 74), p("Liberato Cacace", "LB", 75), p("Joe Bell", "CM", 74), p("Michael Boxall", "CB", 73), p("Tyler Bindon", "CB", 74), p("Max Crocombe", "GK", 73)],
    "Senegal": [p("Sadio Mané", "LW", 86), p("Kalidou Koulibaly", "CB", 86), p("Édouard Mendy", "GK", 82), p("Pape Matar Sarr", "CM", 82), p("Nicolas Jackson", "ST", 83), p("Idrissa Gueye", "DM", 80), p("Ismaïla Sarr", "RW", 81), p("Iliman Ndiaye", "AM", 80)],
    "Egypt": [p("Mohamed Salah", "RW", 91), p("Omar Marmoush", "ST", 85), p("Trézéguet", "LW", 78), p("Mohamed Elneny", "DM", 77), p("Mostafa Mohamed", "ST", 78), p("Ahmed Hegazy", "CB", 78), p("Mohamed El Shenawy", "GK", 78), p("Hamdi Fathi", "CM", 77)],
    "Algeria": [p("Riyad Mahrez", "RW", 84), p("Houssem Aouar", "CM", 80), p("Ismaël Bennacer", "CM", 83), p("Amine Gouiri", "FW", 80), p("Ramy Bensebaini", "CB", 79), p("Youcef Atal", "RB", 77), p("Aïssa Mandi", "CB", 77), p("Baghdad Bounedjah", "ST", 77)],
    "Tunisia": [p("Youssef Msakni", "LW", 77), p("Ellyes Skhiri", "DM", 81), p("Aïssa Laïdouni", "CM", 77), p("Montassar Talbi", "CB", 78), p("Bechir Ben Saïd", "GK", 75), p("Naïm Sliti", "AM", 75), p("Mohamed Dräger", "RB", 74), p("Seifeddine Jaziri", "ST", 74)],
    "Ghana": [p("Mohammed Kudus", "AM", 85), p("Thomas Partey", "DM", 84), p("Iñaki Williams", "ST", 82), p("Jordan Ayew", "FW", 78), p("Antoine Semenyo", "ST", 80), p("Tariq Lamptey", "RB", 78), p("Mohammed Salisu", "CB", 79), p("Alexander Djiku", "CB", 78)],
    "Cape Verde": [p("Ryan Mendes", "LW", 76), p("Bebé", "FW", 75), p("Garry Rodrigues", "RW", 75), p("Vozinha", "GK", 73), p("Stopira", "LB", 72), p("Logan Costa", "CB", 77), p("Jovane Cabral", "LW", 75), p("Jamiro Monteiro", "CM", 74)],
    "South Africa": [p("Lyle Foster", "ST", 78), p("Percy Tau", "RW", 77), p("Ronwen Williams", "GK", 79), p("Teboho Mokoena", "CM", 77), p("Themba Zwane", "AM", 76), p("Mothobi Mvala", "CB", 75), p("Khuliso Mudau", "RB", 75), p("Aubrey Modiba", "LB", 75)],
    "Ivory Coast": [p("Sébastien Haller", "ST", 81), p("Simon Adingra", "LW", 80), p("Franck Kessié", "CM", 84), p("Seko Fofana", "CM", 82), p("Ibrahim Sangaré", "DM", 81), p("Serge Aurier", "RB", 77), p("Ousmane Diomande", "CB", 81), p("Yahia Fofana", "GK", 76)],
    "Cameroon": [p("André Onana", "GK", 84), p("André-Frank Zambo Anguissa", "CM", 84), p("Bryan Mbeumo", "RW", 84), p("Vincent Aboubakar", "ST", 80), p("Eric Maxim Choupo-Moting", "FW", 78), p("Nouhou Tolo", "LB", 76), p("Jean-Charles Castelletto", "CB", 78), p("Georges-Kévin Nkoudou", "LW", 77)],
    "Austria": [p("David Alaba", "CB", 84), p("Marcel Sabitzer", "CM", 84), p("Marko Arnautović", "ST", 78), p("Christoph Baumgartner", "AM", 80), p("Konrad Laimer", "CM", 82), p("Nicolas Seiwald", "DM", 79), p("Kevin Danso", "CB", 81), p("Patrick Pentz", "GK", 77)],
    "Norway": [p("Erling Haaland", "ST", 94), p("Martin Ødegaard", "AM", 90), p("Alexander Sørloth", "ST", 84), p("Oscar Bobb", "RW", 80), p("Sander Berge", "CM", 80), p("Kristoffer Ajer", "CB", 78), p("Julian Ryerson", "RB", 80), p("Ørjan Nyland", "GK", 76)],
    "Scotland": [p("Scott McTominay", "CM", 82), p("Andrew Robertson", "LB", 85), p("John McGinn", "CM", 80), p("Billy Gilmour", "CM", 79), p("Kieran Tierney", "CB", 81), p("Ché Adams", "ST", 77), p("Callum McGregor", "CM", 79), p("Angus Gunn", "GK", 76)],
    "Turkey": [p("Hakan Çalhanoğlu", "CM", 87), p("Arda Güler", "AM", 84), p("Kenan Yıldız", "LW", 82), p("Kerem Aktürkoğlu", "LW", 81), p("Zeki Çelik", "RB", 77), p("Merih Demiral", "CB", 80), p("Orkun Kökçü", "CM", 82), p("Mert Günok", "GK", 77)],
    "Czech Republic": [p("Patrik Schick", "ST", 82), p("Tomáš Souček", "CM", 82), p("Vladimír Coufal", "RB", 79), p("Adam Hložek", "FW", 79), p("Ladislav Krejčí", "CB", 79), p("Antonín Barák", "AM", 78), p("Jindřich Staněk", "GK", 76), p("David Jurásek", "LB", 76)],
    "Switzerland": [p("Granit Xhaka", "DM", 87), p("Manuel Akanji", "CB", 86), p("Yann Sommer", "GK", 85), p("Breel Embolo", "ST", 80), p("Dan Ndoye", "RW", 79), p("Ruben Vargas", "LW", 79), p("Denis Zakaria", "DM", 81), p("Remo Freuler", "CM", 80)],
    "Denmark": [p("Christian Eriksen", "CM", 82), p("Rasmus Højlund", "ST", 82), p("Pierre-Emile Højbjerg", "DM", 84), p("Andreas Christensen", "CB", 84), p("Kasper Schmeichel", "GK", 80), p("Mikkel Damsgaard", "AM", 78), p("Joakim Mæhle", "WB", 80), p("Jannik Vestergaard", "CB", 79)],
    "Poland": [p("Robert Lewandowski", "ST", 88), p("Piotr Zieliński", "CM", 83), p("Jakub Kiwior", "CB", 79), p("Nicola Zalewski", "WB", 78), p("Sebastian Szymański", "AM", 80), p("Matty Cash", "RB", 79), p("Karol Świderski", "ST", 77), p("Łukasz Skorupski", "GK", 79)],
    "Serbia": [p("Dušan Vlahović", "ST", 84), p("Aleksandar Mitrović", "ST", 83), p("Sergej Milinković-Savić", "CM", 85), p("Dušan Tadić", "AM", 82), p("Filip Kostić", "WB", 81), p("Strahinja Pavlović", "CB", 80), p("Nikola Milenković", "CB", 80), p("Predrag Rajković", "GK", 79)],
    "Iraq": [p("Aymen Hussein", "ST", 77), p("Ali Jasim", "LW", 76), p("Zidane Iqbal", "CM", 76), p("Mohanad Ali", "ST", 74), p("Bashar Resan", "AM", 74), p("Amir Al-Ammari", "CM", 73), p("Jalal Hassan", "GK", 73), p("Hussein Ali", "RB", 72)],
    "Panama": [p("Adalberto Carrasquilla", "CM", 77), p("Yoel Bárcenas", "RW", 75), p("José Fajardo", "ST", 74), p("Aníbal Godoy", "DM", 74), p("Michael Murillo", "RB", 76), p("Fidel Escobar", "CB", 74), p("Orlando Mosquera", "GK", 73), p("Éric Davis", "LB", 73)],
    "Curaçao": [p("Juninho Bacuna", "CM", 76), p("Leandro Bacuna", "CM", 74), p("Jürgen Locadia", "ST", 75), p("Kenji Gorré", "LW", 73), p("Eloy Room", "GK", 73), p("Sherel Floranus", "RB", 73), p("Rangelo Janga", "ST", 72), p("Cuco Martina", "CB", 72)],
    "Haiti": [p("Duckens Nazon", "ST", 76), p("Frantzdy Pierrot", "ST", 75), p("Jean-Ricner Bellegarde", "CM", 78), p("Danley Jean Jacques", "DM", 75), p("Derrick Etienne Jr", "LW", 73), p("Johny Placide", "GK", 72), p("Wilde-Donald Guerrier", "LB", 72), p("Ricardo Adé", "CB", 73)],
    "Hungary": [p("Dominik Szoboszlai", "AM", 87), p("Roland Sallai", "RW", 80), p("Willi Orbán", "CB", 82), p("Péter Gulácsi", "GK", 81), p("Milos Kerkez", "LB", 82), p("Ádám Nagy", "DM", 77), p("Barnabás Varga", "ST", 78), p("Dénes Dibusz", "GK", 76)],
    "Albania": [p("Armando Broja", "ST", 78), p("Jasir Asani", "RW", 76), p("Nedim Bajrami", "AM", 77), p("Elseid Hysaj", "RB", 77), p("Berat Djimsiti", "CB", 80), p("Ylber Ramadani", "DM", 76), p("Thomas Strakosha", "GK", 77), p("Rey Manaj", "ST", 76)],
    "Slovenia": [p("Benjamin Šeško", "ST", 83), p("Jan Oblak", "GK", 90), p("Jaka Bijol", "CB", 80), p("Sandi Lovrić", "CM", 77), p("Adam Gnezda Čerin", "CM", 77), p("Timi Max Elšnik", "CM", 76), p("Petar Stojanović", "RB", 75), p("Jan Mlakar", "FW", 75)],
    "Romania": [p("Radu Drăgușin", "CB", 82), p("Nicolae Stanciu", "AM", 78), p("Dennis Man", "RW", 78), p("Valentin Mihăilă", "LW", 77), p("Marius Marin", "DM", 76), p("Ianis Hagi", "AM", 76), p("Florin Niță", "GK", 76), p("Andrei Burcă", "CB", 76)],
    "Slovakia": [p("Milan Škriniar", "CB", 84), p("Stanislav Lobotka", "CM", 85), p("Martin Dúbravka", "GK", 79), p("Dávid Hancko", "CB", 82), p("Lukáš Haraslín", "LW", 78), p("Tomáš Suslov", "AM", 76), p("Róbert Boženík", "ST", 75), p("Juraj Kucka", "CM", 75)],
    "Ukraine": [p("Artem Dovbyk", "ST", 84), p("Viktor Tsygankov", "RW", 82), p("Mykhailo Mudryk", "LW", 80), p("Oleksandr Zinchenko", "CM", 82), p("Georgiy Sudakov", "AM", 81), p("Illia Zabarnyi", "CB", 82), p("Anatoliy Trubin", "GK", 82), p("Roman Yaremchuk", "ST", 78)],
    "Georgia": [p("Khvicha Kvaratskhelia", "LW", 88), p("Giorgi Mamardashvili", "GK", 85), p("Georges Mikautadze", "ST", 81), p("Giorgi Chakvetadze", "AM", 77), p("Giorgi Kochorashvili", "CM", 76), p("Otar Kiteishvili", "CM", 76), p("Guram Kashia", "CB", 75), p("Solomon Kverkvelia", "CB", 74)],
}

WORLD_CUP_2026_TEAMS = [
    "Canada", "Mexico", "United States", "Japan", "New Zealand", "Iran", "Argentina", "Uzbekistan",
    "South Korea", "Jordan", "Australia", "Brazil", "Ecuador", "Uruguay", "Paraguay", "Colombia",
    "Morocco", "Tunisia", "Egypt", "Algeria", "Ghana", "Cape Verde", "South Africa", "Senegal",
    "Ivory Coast", "Cameroon", "England", "France", "Spain", "Portugal", "Netherlands", "Belgium",
    "Germany", "Croatia", "Austria", "Norway", "Scotland", "Turkey", "Czech Republic", "Switzerland",
    "Denmark", "Poland", "Iraq", "Qatar", "Saudi Arabia", "Panama", "Curaçao", "Haiti",
]

EURO_2024_TEAMS = [
    "Germany", "Scotland", "Hungary", "Switzerland", "Spain", "Croatia", "Italy", "Albania",
    "Slovenia", "Denmark", "Serbia", "England", "Poland", "Netherlands", "Austria", "France",
    "Belgium", "Slovakia", "Romania", "Ukraine", "Turkey", "Georgia", "Portugal", "Czech Republic",
]

INTERNATIONAL = {
    "World Cup 2026-style": {
        "teams": WORLD_CUP_2026_TEAMS,
        "groups": 12,
        "advance_top": 2,
        "best_thirds": 8,
        "format_note": "48 teams, 12 groups of four, top two plus eight best third-placed teams reach the Round of 32.",
    },
    "EURO / European Championship": {
        "teams": EURO_2024_TEAMS,
        "groups": 6,
        "advance_top": 2,
        "best_thirds": 4,
        "format_note": "24 teams, six groups of four, top two plus four best third-placed teams reach the Round of 16.",
    },
}


def national_team(name: str) -> dict:
    rating = NATIONAL_RATINGS[name]
    team = Team(
        name=name,
        country=name,
        league="International",
        attack=rating["attack"],
        midfield=rating["midfield"],
        defence=rating["defence"],
        star_player=rating["star_player"],
    ).to_dict()
    team["id"] = _slug(name)
    team["confederation"] = rating.get("confederation", "International")
    team["players"] = NATIONAL_SQUADS.get(name, [])
    team["is_national_team"] = True
    return enrich_team(team)


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


COUNTRY_FLAGS = {
    "England": "🏴", "Wales": "🏴", "Scotland": "🏴", "Republic of Ireland": "🇮🇪",
    "Spain": "🇪🇸", "Italy": "🇮🇹", "Germany": "🇩🇪", "France": "🇫🇷", "Portugal": "🇵🇹",
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Brazil": "🇧🇷", "USA": "🇺🇸", "United States": "🇺🇸",
    "Saudi Arabia": "🇸🇦", "Turkey": "🇹🇷", "Greece": "🇬🇷", "Switzerland": "🇨🇭", "Austria": "🇦🇹",
    "Czechia": "🇨🇿", "Czech Republic": "🇨🇿", "Ukraine": "🇺🇦", "Norway": "🇳🇴", "Denmark": "🇩🇰",
    "Sweden": "🇸🇪", "Poland": "🇵🇱", "Romania": "🇷🇴", "Serbia": "🇷🇸", "Croatia": "🇭🇷",
    "Argentina": "🇦🇷", "Canada": "🇨🇦", "Mexico": "🇲🇽", "Japan": "🇯🇵", "New Zealand": "🇳🇿",
    "Iran": "🇮🇷", "Uzbekistan": "🇺🇿", "South Korea": "🇰🇷", "Jordan": "🇯🇴", "Australia": "🇦🇺",
    "Ecuador": "🇪🇨", "Uruguay": "🇺🇾", "Paraguay": "🇵🇾", "Colombia": "🇨🇴", "Morocco": "🇲🇦",
    "Tunisia": "🇹🇳", "Egypt": "🇪🇬", "Algeria": "🇩🇿", "Ghana": "🇬🇭", "Cape Verde": "🇨🇻",
    "South Africa": "🇿🇦", "Senegal": "🇸🇳", "Ivory Coast": "🇨🇮", "Cameroon": "🇨🇲", "Iraq": "🇮🇶",
    "Qatar": "🇶🇦", "Panama": "🇵🇦", "Curaçao": "🇨🇼", "Haiti": "🇭🇹", "Hungary": "🇭🇺",
    "Albania": "🇦🇱", "Slovenia": "🇸🇮", "Slovakia": "🇸🇰", "Georgia": "🇬🇪", "World": "🏳️",
}

TEAM_COLOURS = {
    "Arsenal": ("#dc2626", "#ffffff"), "Liverpool": ("#b91c1c", "#facc15"), "Man City": ("#38bdf8", "#ffffff"),
    "Manchester United": ("#dc2626", "#111827"), "Chelsea": ("#1d4ed8", "#ffffff"), "Tottenham": ("#f8fafc", "#0f172a"),
    "Newcastle": ("#111827", "#f8fafc"), "Aston Villa": ("#7f1d1d", "#60a5fa"), "Everton": ("#2563eb", "#ffffff"),
    "West Ham United": ("#7f1d1d", "#93c5fd"), "Brighton": ("#2563eb", "#ffffff"), "Crystal Palace": ("#1d4ed8", "#ef4444"),
    "Real Madrid": ("#f8fafc", "#facc15"), "Barcelona": ("#7f1d1d", "#1d4ed8"), "Bayern Munich": ("#dc2626", "#ffffff"),
    "Paris Saint-Germain": ("#1e3a8a", "#ef4444"), "Inter Milan": ("#1d4ed8", "#111827"), "AC Milan": ("#dc2626", "#111827"),
}


def _abbr(name: str) -> str:
    words = [w for w in name.replace("AFC", "").replace("FC", "").replace("United", "Utd").split() if w]
    if len(words) == 1:
        return words[0][:3].upper()
    return "".join(w[0] for w in words[:3]).upper()[:3]


def _colour_pair(name: str) -> tuple[str, str]:
    if name in TEAM_COLOURS:
        return TEAM_COLOURS[name]
    palette = [
        ("#16a34a", "#f8fafc"), ("#0ea5e9", "#f8fafc"), ("#9333ea", "#f8fafc"),
        ("#f97316", "#111827"), ("#e11d48", "#f8fafc"), ("#facc15", "#111827"),
        ("#14b8a6", "#0f172a"), ("#64748b", "#f8fafc"),
    ]
    return palette[sum(ord(c) for c in name) % len(palette)]


def enrich_team(team: dict) -> dict:
    primary, secondary = _colour_pair(team["name"])
    team["flag"] = COUNTRY_FLAGS.get(team.get("country"), COUNTRY_FLAGS.get(team.get("name"), "🏳️"))
    team["abbr"] = _abbr(team["name"])
    team["crest_primary"] = primary
    team["crest_secondary"] = secondary
    return team


def default_team(name: str) -> Team:
    country, league = TEAM_COUNTRY_HINTS.get(name, ("World", "Custom / Other"))
    base = COUNTRY_DEFAULTS.get(country, 68)
    # Small deterministic wobble so generic teams don't all feel identical.
    wobble = (sum(ord(c) for c in name) % 7) - 3
    overall = max(55, min(88, base + wobble))
    return Team(
        name=name,
        country=country,
        league=league,
        attack=max(50, min(99, overall + ((len(name) % 5) - 2))),
        midfield=max(50, min(99, overall + ((len(name) % 3) - 1))),
        defence=max(50, min(99, overall - ((len(name) % 4) - 1))),
        star_player=f"{name} Star",
    )


def build_team_database() -> List[dict]:
    names = set(RATINGS.keys()) | set(UCL_2025_26) | set(UEL_2025_26) | set(UECL_2025_26) | set(PREMIER_LEAGUE_2025_26) | set(FA_CUP_SEED_TEAMS)
    built: List[dict] = []
    for name in sorted(names):
        if name in RATINGS:
            t = Team(name=name, **RATINGS[name])
        else:
            t = default_team(name)
        team = t.to_dict() | {"id": _slug(t.name), "is_national_team": False, "players": CLUB_SQUADS.get(t.name, [])}
        built.append(enrich_team(team))
    for name in sorted(NATIONAL_RATINGS.keys()):
        built.append(national_team(name))
    return built


def team_lookup() -> Dict[str, dict]:
    return {t["name"]: t for t in build_team_database()}


TEAMS = build_team_database()

# ===== Inlined football_sim.simulator =====
"""Football simulation engine."""



FIRST_NAMES = [
    "Alex", "Ben", "Carlos", "Diego", "Ethan", "Felix", "Gabriel", "Hugo", "Ivan", "Jamal",
    "Kai", "Leo", "Mateo", "Nico", "Oscar", "Rafael", "Sam", "Theo", "Victor", "Yusuf",
]
LAST_NAMES = [
    "Adams", "Costa", "Silva", "Fernandes", "Martínez", "Kovač", "Wilson", "Garcia", "Mbaye", "Rossi",
    "Walker", "Mendes", "Nakamura", "Petrov", "Santos", "Diallo", "Bennett", "Khan", "Schmidt", "Romero",
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def poisson(lam: float) -> int:
    """Small pure-Python Poisson sampler for football goals."""
    lam = clamp(lam, 0.05, 5.0)
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= random.random()
    return k - 1


def player_pool(team: dict) -> List[dict]:
    """Return a weighted player pool.

    National teams ship with real-player cores and ratings. Club/custom teams fall
    back to deterministic generated depth so every team can still produce scorers,
    assists, cards and injuries.
    """
    players = team.get("players") or []
    if players:
        return players

    random.seed(team["name"])
    generated = [{"name": team.get("star_player") or f"{team['name']} Star", "position": "ST", "rating": team.get("overall", 75) + 3}]
    while len(generated) < 13:
        generated.append({
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "position": random.choice(["ST", "LW", "RW", "AM", "CM", "DM", "CB", "FB", "GK"]),
            "rating": max(55, min(94, int(random.gauss(team.get("overall", 74), 4)))),
        })
    random.seed()
    return generated


def _attacking_weight(player: dict) -> float:
    pos = player.get("position", "CM")
    base = max(1, player.get("rating", 75) - 58)
    pos_bonus = {"ST": 2.8, "FW": 2.5, "LW": 2.2, "RW": 2.2, "AM": 1.9, "CM": 1.1, "DM": .65, "WB": .55, "FB": .45, "CB": .28, "GK": .05}
    return base * pos_bonus.get(pos, 1.0)


def _assist_weight(player: dict) -> float:
    pos = player.get("position", "CM")
    base = max(1, player.get("rating", 75) - 58)
    pos_bonus = {"AM": 2.6, "CM": 2.0, "RW": 2.1, "LW": 2.1, "DM": 1.2, "ST": 1.0, "FW": 1.1, "WB": 1.4, "FB": 1.3, "CB": .35, "GK": .02}
    return base * pos_bonus.get(pos, 1.0)


def pick_goal_scorer(team: dict) -> str:
    pool = player_pool(team)
    weights = [_attacking_weight(p) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def pick_assister(team: dict, scorer: str) -> str:
    pool = [p for p in player_pool(team) if p["name"] != scorer]
    if not pool:
        return scorer
    weights = [_assist_weight(p) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def pick_card_or_injury_player(team: dict) -> str:
    pool = player_pool(team)
    weights = []
    for player in pool:
        pos = player.get("position", "CM")
        rating = player.get("rating", 75)
        contact_bonus = {"CB": 2.2, "DM": 2.0, "FB": 1.7, "WB": 1.5, "CM": 1.25, "ST": 1.0, "FW": 1.0, "LW": .9, "RW": .9, "AM": .9, "GK": .25}.get(pos, 1.0)
        weights.append(max(1, rating - 60) * contact_bonus)
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def team_power(team: dict) -> float:
    """Weighted team strength used by the winner model.

    Ratings matter strongly, but the match engine still leaves room for
    pressure swings, red-hot finishing and late cup upsets.
    """
    players = player_pool(team)
    star = max((p.get("rating", team.get("overall", 75)) for p in players), default=team.get("overall", 75))
    depth = sum(p.get("rating", 75) for p in players[:8]) / max(1, min(8, len(players)))
    return (
        team.get("attack", 75) * 0.34
        + team.get("midfield", 75) * 0.26
        + team.get("defence", 75) * 0.24
        + team.get("overall", 75) * 0.10
        + star * 0.04
        + depth * 0.02
    )


def expected_goals(home: dict, away: dict, neutral: bool = False) -> Tuple[float, float]:
    home_adv = 0.22 if not neutral else 0.0
    hp = team_power(home)
    ap = team_power(away)
    home_quality = (home["attack"] * 0.54 + home["midfield"] * 0.28 - away["defence"] * 0.40 - away["midfield"] * 0.12)
    away_quality = (away["attack"] * 0.54 + away["midfield"] * 0.28 - home["defence"] * 0.40 - home["midfield"] * 0.12)
    strength_edge = (hp - ap) / 46
    # Keep randomness, but not so much that ratings feel meaningless.
    home_xg = 1.22 + home_adv + (home_quality / 58) + strength_edge + random.gauss(0, 0.14)
    away_xg = 1.05 + (away_quality / 58) - strength_edge + random.gauss(0, 0.14)
    return clamp(home_xg, 0.12, 4.7), clamp(away_xg, 0.12, 4.4)


def _yellow_card_count() -> int:
    """Low-noise card model: realistic enough, but not cards everywhere."""
    return random.choices([0, 1, 2, 3], weights=[42, 38, 17, 3], k=1)[0]


def _team_match_numbers(team: dict, opponent: dict, xg: float, goals: int, possession: int) -> dict:
    """Create believable football box-score stats from team quality and xG."""
    quality_edge = (team.get("attack", 75) + team.get("midfield", 75) - opponent.get("defence", 75) - opponent.get("midfield", 75)) / 25
    shots = int(round(clamp((xg * 4.3) + random.gauss(4.9 + quality_edge, 1.7), 2, 24)))
    shots_on_target = int(round(clamp(goals + random.gauss(max(1.2, xg * 1.6), 1.05), goals, min(shots, 13))))
    big_chances = int(clamp(round(xg + goals + random.choice([-1, 0, 0, 1])), 0, 8))
    corners = int(clamp(round((shots * 0.28) + random.gauss(1.5, 1.2)), 0, 13))
    fouls = int(clamp(round(random.gauss(9.4, 2.8) + max(0, opponent.get("midfield", 75) - team.get("midfield", 75)) / 18), 4, 22))
    pass_accuracy = int(clamp(round(73 + (team.get("midfield", 75) - 70) * 0.42 + (possession - 50) * 0.18 + random.gauss(0, 2.5)), 62, 93))
    keeper_saves = 0  # Filled after both sides are known.
    return {
        "possession": possession,
        "shots": shots,
        "shots_on_target": shots_on_target,
        "big_chances": big_chances,
        "corners": corners,
        "fouls": fouls,
        "pass_accuracy": pass_accuracy,
        "keeper_saves": keeper_saves,
    }


def _build_match_stats(home: dict, away: dict, home_xg: float, away_xg: float, home_goals: int, away_goals: int) -> dict:
    midfield_edge = home.get("midfield", 75) - away.get("midfield", 75)
    overall_edge = home.get("overall", 75) - away.get("overall", 75)
    home_possession = int(clamp(round(50 + midfield_edge * 0.38 + overall_edge * 0.13 + random.gauss(0, 3.8)), 34, 66))
    away_possession = 100 - home_possession
    home_stats = _team_match_numbers(home, away, home_xg, home_goals, home_possession)
    away_stats = _team_match_numbers(away, home, away_xg, away_goals, away_possession)
    home_stats["keeper_saves"] = max(0, away_stats["shots_on_target"] - away_goals)
    away_stats["keeper_saves"] = max(0, home_stats["shots_on_target"] - home_goals)
    return {home["name"]: home_stats, away["name"]: away_stats}


def _pick_outfield_player(team: dict) -> str:
    pool = [p for p in player_pool(team) if p.get("position") != "GK"] or player_pool(team)
    weights = [max(1, p.get("rating", 75) - 58) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def _pick_goalkeeper(team: dict) -> str:
    keepers = [p for p in player_pool(team) if p.get("position") == "GK"]
    if keepers:
        return max(keepers, key=lambda p: p.get("rating", 0))["name"]
    return f"{team.get('name', 'Team')} goalkeeper"


def _add_open_play_details(event_objects: list, team: dict, opponent: dict, team_stats: dict, opponent_stats: dict, team_goals: int, opponent_goals: int) -> None:
    """Add useful match detail without flooding the feed with card events."""
    team_name = team["name"]
    opponent_name = opponent["name"]
    attacking_player = _pick_outfield_player(team)
    goalkeeper = _pick_goalkeeper(opponent)

    if team_stats["shots_on_target"] > team_goals:
        minute = random.randint(15, 82)
        event_objects.append({
            "minute": minute,
            "text": f"🧤 {minute}' {opponent_name}: {goalkeeper} makes an important save from {attacking_player}",
            "type": "save",
        })
    if team_stats["big_chances"] >= 2 and random.random() < 0.55:
        minute = random.randint(20, 86)
        event_objects.append({
            "minute": minute,
            "text": f"🔥 {minute}' {team_name}: big chance for {attacking_player}, but the finish is just off target",
            "type": "chance",
        })
    if team_stats["corners"] >= 5 and random.random() < 0.45:
        defender = pick_card_or_injury_player(opponent)
        minute = random.randint(25, 88)
        event_objects.append({
            "minute": minute,
            "text": f"🚩 {minute}' {team_name}: spell of corner pressure, {defender} clears under pressure",
            "type": "pressure",
        })
    if team_stats["possession"] >= 57 and random.random() < 0.55:
        minute = random.randint(12, 72)
        event_objects.append({
            "minute": minute,
            "text": f"🎛️ {minute}' {team_name}: controlling midfield with {team_stats['possession']}% possession",
            "type": "control",
        })
    if abs(team_goals - opponent_goals) <= 1 and random.random() < 0.40:
        minute = random.randint(70, 90)
        event_objects.append({
            "minute": minute,
            "text": f"⏳ {minute}' {team_name}: late pressure as the game opens up",
            "type": "late",
        })


def minute_label(minute: int) -> str:
    if 91 <= minute <= 99:
        return f"90+{minute - 90}"
    if minute == 121:
        return "Pens"
    return str(minute)


def add_goal_event(goal_events: list, team: dict, minute: int, tag: str = "") -> None:
    scorer = pick_goal_scorer(team)
    assister = pick_assister(team, scorer) if random.random() < 0.76 else None
    goal_events.append((minute, team["name"], scorer, assister, tag))


def simulate_match(home: dict, away: dict, knockout: bool = False, neutral: bool = False) -> dict:
    home_xg, away_xg = expected_goals(home, away, neutral)
    home_goals = poisson(home_xg)
    away_goals = poisson(away_xg)

    scorer_counts: Dict[str, int] = {}
    assister_counts: Dict[str, int] = {}
    card_log = []
    injury_log = []
    event_objects = []

    goal_events = []
    for _ in range(home_goals):
        add_goal_event(goal_events, home, random.randint(2, 89))
    for _ in range(away_goals):
        add_goal_event(goal_events, away, random.randint(2, 89))

    # Late drama model. Strong teams are still favoured, but the last 15 minutes
    # can produce realistic pressure swings and rare underdog/cup upsets.
    hp = team_power(home)
    ap = team_power(away)
    gap = abs(hp - ap)
    favourite = home if hp >= ap else away
    underdog = away if favourite is home else home
    fav_goals = home_goals if favourite is home else away_goals
    dog_goals = away_goals if favourite is home else home_goals
    if dog_goals <= fav_goals and random.random() < clamp(0.19 - (gap * 0.006), 0.045, 0.18):
        minute = random.randint(78, 95)
        add_goal_event(goal_events, underdog, minute, "late_underdog")
        if underdog is home:
            home_goals += 1
        else:
            away_goals += 1
    if dog_goals == fav_goals and random.random() < clamp(0.09 - (gap * 0.004), 0.025, 0.085):
        minute = random.randint(87, 95)
        add_goal_event(goal_events, underdog, minute, "stoppage_upset")
        if underdog is home:
            home_goals += 1
        else:
            away_goals += 1
    elif abs(home_goals - away_goals) == 1 and random.random() < 0.09:
        # The trailing team throws everything forward late on.
        chaser = home if home_goals < away_goals else away
        minute = random.randint(84, 95)
        add_goal_event(goal_events, chaser, minute, "late_pressure")
        if chaser is home:
            home_goals += 1
        else:
            away_goals += 1

    for minute, team_name, scorer, assister, tag in sorted(goal_events, key=lambda item: item[0]):
        label = minute_label(minute)
        prefix = "⚽"
        if tag == "late_underdog":
            prefix = "⚽🔥"
        elif tag == "stoppage_upset":
            prefix = "⚽💥"
        elif tag == "late_pressure":
            prefix = "⚽⏳"
        if assister:
            text = f"{prefix} {label}' {team_name}: {scorer} (assist: {assister})"
            assister_counts[f"{assister} — {team_name}"] = assister_counts.get(f"{assister} — {team_name}", 0) + 1
        else:
            text = f"{prefix} {label}' {team_name}: {scorer}"
        event_objects.append({"minute": minute, "text": text, "type": "goal", "team": team_name, "player": scorer, "assist": assister, "tag": tag})
        scorer_counts[f"{scorer} — {team_name}"] = scorer_counts.get(f"{scorer} — {team_name}", 0) + 1

    match_stats = _build_match_stats(home, away, home_xg, away_xg, home_goals, away_goals)
    _add_open_play_details(event_objects, home, away, match_stats[home["name"]], match_stats[away["name"]], home_goals, away_goals)
    _add_open_play_details(event_objects, away, home, match_stats[away["name"]], match_stats[home["name"]], away_goals, home_goals)

    for team in [home, away]:
        yellows = _yellow_card_count()
        for _ in range(yellows):
            minute = random.randint(12, 90)
            player = pick_card_or_injury_player(team)
            card_log.append({"team": team["name"], "player": player, "minute": minute, "card": "Yellow"})
            # Reds are deliberately rare so matches are not dominated by discipline.
            if random.random() < 0.004:
                red_minute = min(90, minute + random.randint(6, 28))
                card_log.append({"team": team["name"], "player": player, "minute": red_minute, "card": "Red"})
        if random.random() < 0.07:
            minute = random.randint(18, 88)
            player = pick_card_or_injury_player(team)
            severity = random.choice(["minor knock", "hamstring strain", "ankle injury", "shoulder injury"])
            injury_log.append({"team": team["name"], "player": player, "minute": minute, "injury": severity})

    for c in card_log:
        icon = "🟨" if c["card"] == "Yellow" else "🟥"
        event_objects.append({
            "minute": c["minute"],
            "text": f"{icon} {c['minute']}' {c['team']}: {c['player']} {c['card'].lower()} card",
            "type": "card",
        })
    for i in injury_log:
        event_objects.append({
            "minute": i["minute"],
            "text": f"🚑 {i['minute']}' {i['team']}: {i['player']} — {i['injury']}",
            "type": "injury",
        })

    extra = None
    penalties = None
    winner = None
    if knockout:
        if home_goals > away_goals:
            winner = home["name"]
        elif away_goals > home_goals:
            winner = away["name"]
        else:
            # Extra time first, then penalties if needed.
            et_home = poisson(0.35 + (home["overall"] - away["overall"]) / 180)
            et_away = poisson(0.35 + (away["overall"] - home["overall"]) / 180)
            home_goals += et_home
            away_goals += et_away
            extra = {"home": et_home, "away": et_away}
            if et_home or et_away:
                event_objects.append({
                    "minute": 105,
                    "text": f"⏱️ Extra time: {home['name']} {et_home}–{et_away} {away['name']}",
                    "type": "extra_time",
                })
            if home_goals > away_goals:
                winner = home["name"]
            elif away_goals > home_goals:
                winner = away["name"]
            else:
                hp = random.randint(3, 5)
                ap = random.randint(3, 5)
                while hp == ap:
                    hp = random.randint(3, 7)
                    ap = random.randint(3, 7)
                penalties = {"home": hp, "away": ap}
                winner = home["name"] if hp > ap else away["name"]
                event_objects.append({
                    "minute": 121,
                    "text": f"🥅 Penalties: {home['name']} {hp}–{ap} {away['name']} — {winner} advance",
                    "type": "penalties",
                })

    # Keep box-score stats consistent after extra time goals.
    for team_name, goals in [(home["name"], home_goals), (away["name"], away_goals)]:
        team_stats = match_stats[team_name]
        team_stats["shots_on_target"] = max(team_stats["shots_on_target"], goals)
        team_stats["shots"] = max(team_stats["shots"], team_stats["shots_on_target"])

    timeline = sorted(event_objects, key=lambda x: (x["minute"], x["text"]))
    events = [item["text"] for item in timeline]
    if not events:
        events.append("Tense tactical battle with no major goals — both sides cancelled each other out.")
        timeline.append({"minute": 90, "text": events[0], "type": "full_time"})

    return {
        "id": str(uuid.uuid4()),
        "home": home["name"],
        "away": away["name"],
        "home_goals": home_goals,
        "away_goals": away_goals,
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "match_stats": match_stats,
        "events": events,
        "timeline": timeline,
        "home_power": round(team_power(home), 1),
        "away_power": round(team_power(away), 1),
        "cards": card_log,
        "injuries": injury_log,
        "scorers": scorer_counts,
        "assisters": assister_counts,
        "winner": winner,
        "extra_time": extra,
        "penalties": penalties,
        "played_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def empty_standing(team: str) -> dict:
    return {"Team": team, "P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}


def update_standings(standings: Dict[str, dict], result: dict) -> None:
    h, a = result["home"], result["away"]
    hg, ag = result["home_goals"], result["away_goals"]
    for team in [h, a]:
        standings.setdefault(team, empty_standing(team))
    standings[h]["P"] += 1
    standings[a]["P"] += 1
    standings[h]["GF"] += hg
    standings[h]["GA"] += ag
    standings[a]["GF"] += ag
    standings[a]["GA"] += hg
    if hg > ag:
        standings[h]["W"] += 1
        standings[a]["L"] += 1
        standings[h]["Pts"] += 3
    elif ag > hg:
        standings[a]["W"] += 1
        standings[h]["L"] += 1
        standings[a]["Pts"] += 3
    else:
        standings[h]["D"] += 1
        standings[a]["D"] += 1
        standings[h]["Pts"] += 1
        standings[a]["Pts"] += 1
    for team in [h, a]:
        standings[team]["GD"] = standings[team]["GF"] - standings[team]["GA"]


def sorted_table(standings: Dict[str, dict]) -> List[dict]:
    return sorted(standings.values(), key=lambda r: (r["Pts"], r["GD"], r["GF"], r["W"], r["Team"]), reverse=True)


def merge_counter(target: Dict[str, int], source: Dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def top_list(counter: Dict[str, int], limit: int = 10) -> List[dict]:
    rows = [{"Player": k, "Total": v} for k, v in counter.items()]
    return sorted(rows, key=lambda r: r["Total"], reverse=True)[:limit]


def dumps_state(state: dict) -> str:
    return json.dumps(state, ensure_ascii=False, indent=2)


def loads_state(text: str) -> dict:
    return json.loads(text)

# ===== Inlined football_sim.tournaments =====
"""Tournament construction and progression helpers."""




def make_match(home: str, away: str) -> dict:
    return {"id": str(uuid.uuid4()), "home": home, "away": away, "played": False, "result": None}


def round_robin_schedule(team_names: List[str], double_round: bool = False) -> List[List[dict]]:
    teams = team_names[:]
    if len(teams) % 2:
        teams.append("BYE")
    n = len(teams)
    rounds = []
    rotation = teams[:]
    for round_idx in range(n - 1):
        matches = []
        for i in range(n // 2):
            home = rotation[i]
            away = rotation[n - 1 - i]
            if home == "BYE" or away == "BYE":
                continue
            if round_idx % 2:
                home, away = away, home
            matches.append(make_match(home, away))
        rounds.append(matches)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
    if double_round:
        reverse = [[make_match(m["away"], m["home"]) for m in md] for md in rounds]
        rounds += reverse
    return rounds


def swiss_like_schedule(team_names: List[str], matchdays: int = 8) -> List[List[dict]]:
    """Create unique pairings per matchday.

    This is game-friendly rather than a complete UEFA draw engine. It keeps the
    user experience faithful: one league table, 36 teams, 8/6 matchdays, then
    knockout play-offs and round of 16.
    """
    base = team_names[:]
    random.shuffle(base)
    all_rounds = round_robin_schedule(base, double_round=False)
    return all_rounds[:matchdays]


def knockout_pairs(teams: List[str], seeded: bool = True) -> List[dict]:
    names = teams[:]
    if seeded:
        left = names[: len(names) // 2]
        right = names[len(names) // 2 :][::-1]
        pairs = zip(left, right)
    else:
        random.shuffle(names)
        pairs = zip(names[::2], names[1::2])
    return [make_match(a, b) for a, b in pairs]


def init_state(name: str, teams: List[dict], schedule: List[List[dict]], mode: str, config: dict | None = None) -> dict:
    team_names = [t["name"] for t in teams]
    return {
        "name": name,
        "mode": mode,
        "config": config or {},
        "teams": teams,
        "team_names": team_names,
        "team_lookup": {t["name"]: t for t in teams},
        "stage": "league" if schedule else "knockout",
        "matchday_index": 0,
        "schedule": schedule,
        "knockout_rounds": [],
        "standings": {name: empty_standing(name) for name in team_names},
        "top_scorers": {},
        "top_assisters": {},
        "history": [],
        "champion": None,
    }


def create_uefa_tournament(competition: str) -> dict:
    lookup = team_lookup()
    cfg = CONTINENTAL[competition]
    teams = [deepcopy(lookup[name]) for name in cfg["teams"]]
    schedule = swiss_like_schedule([t["name"] for t in teams], cfg["league_rounds"])
    return init_state(competition, teams, schedule, "uefa", {"league_rounds": cfg["league_rounds"], "source": "UEFA 2025/26 seed"})


def create_league(name: str, teams: List[dict], double_round: bool = False) -> dict:
    schedule = round_robin_schedule([t["name"] for t in teams], double_round=double_round)
    return init_state(name, teams, schedule, "league", {"double_round": double_round})


def create_premier_league() -> dict:
    lookup = team_lookup()
    cfg = DOMESTIC["Premier League"]
    teams = [deepcopy(lookup[name]) for name in cfg["teams"]]
    schedule = round_robin_schedule([t["name"] for t in teams], double_round=True)
    return init_state("Premier League", teams, schedule, "premier_league", {"double_round": True, "format_note": cfg.get("format_note", "")})


def fa_cup_round_name(team_count: int) -> str:
    return {
        64: "FA Cup Third Round",
        32: "FA Cup Fourth Round",
        16: "FA Cup Fifth Round",
        8: "Quarter-finals",
        4: "Semi-finals",
        2: "Final",
    }.get(team_count, f"Last {team_count}")


def create_fa_cup() -> dict:
    lookup = team_lookup()
    cfg = DOMESTIC["FA Cup"]
    teams = [deepcopy(lookup[name]) for name in cfg["teams"]]
    state = init_state("FA Cup", teams, [], "fa_cup", {"format_note": cfg.get("format_note", ""), "random_draws": True})
    state["stage"] = "knockout"
    names = [t["name"] for t in teams]
    state["knockout_rounds"] = [{"name": fa_cup_round_name(len(names)), "matches": knockout_pairs(names, seeded=False), "complete": False}]
    return state


def create_knockout(name: str, teams: List[dict]) -> dict:
    state = init_state(name, teams, [], "knockout", {})
    state["stage"] = "knockout"
    state["knockout_rounds"] = [{"name": round_name(len(teams)), "matches": knockout_pairs([t["name"] for t in teams], seeded=False), "complete": False}]
    return state


def create_cup(name: str, teams: List[dict], groups: int = 4) -> dict:
    random.shuffle(teams)
    group_map: Dict[str, List[dict]] = {chr(65 + i): [] for i in range(groups)}
    for idx, team in enumerate(teams):
        group_map[chr(65 + (idx % groups))].append(team)
    schedule = []
    group_tables = {}
    for group_name, group_teams in group_map.items():
        group_tables[group_name] = {t["name"]: empty_standing(t["name"]) for t in group_teams}
        for md_idx, md in enumerate(round_robin_schedule([t["name"] for t in group_teams], double_round=False)):
            while len(schedule) <= md_idx:
                schedule.append([])
            for match in md:
                match["group"] = group_name
                schedule[md_idx].append(match)
    state = init_state(name, teams, schedule, "cup", {"groups": groups})
    state["group_tables"] = group_tables
    return state



def create_group_knockout(name: str, teams: List[dict], groups: int, advance_top: int = 2, best_thirds: int = 0, mode: str = "international", config: dict | None = None) -> dict:
    """Create a group stage followed by knockout rounds.

    Used by the World Cup and EURO modes. Group draw is shuffled at creation so
    every save feels replayable. The qualification rules support top-N plus best
    third-placed teams, matching modern international tournament formats.
    """
    teams = deepcopy(teams)
    random.shuffle(teams)
    group_map: Dict[str, List[dict]] = {chr(65 + i): [] for i in range(groups)}
    for idx, team in enumerate(teams):
        group_map[chr(65 + (idx % groups))].append(team)

    schedule: List[List[dict]] = []
    group_tables = {}
    for group_name, group_teams in group_map.items():
        group_tables[group_name] = {t["name"]: empty_standing(t["name"]) for t in group_teams}
        for md_idx, md in enumerate(round_robin_schedule([t["name"] for t in group_teams], double_round=False)):
            while len(schedule) <= md_idx:
                schedule.append([])
            for match in md:
                match["group"] = group_name
                schedule[md_idx].append(match)

    cfg = {"groups": groups, "advance_top": advance_top, "best_thirds": best_thirds}
    if config:
        cfg.update(config)
    state = init_state(name, teams, schedule, mode, cfg)
    state["group_tables"] = group_tables
    return state


def create_international_tournament(competition: str) -> dict:
    lookup = team_lookup()
    cfg = INTERNATIONAL[competition]
    teams = [deepcopy(lookup[name]) for name in cfg["teams"]]
    return create_group_knockout(
        competition,
        teams,
        groups=cfg["groups"],
        advance_top=cfg.get("advance_top", 2),
        best_thirds=cfg.get("best_thirds", 0),
        mode="international",
        config={"format_note": cfg.get("format_note", "")},
    )

def round_name(team_count: int) -> str:
    return {
        64: "Round of 64",
        32: "Round of 32",
        24: "Knockout Play-offs",
        16: "Round of 16",
        8: "Quarter-finals",
        4: "Semi-finals",
        2: "Final",
    }.get(team_count, f"Last {team_count}")


def simulate_matchday(state: dict, team_db: Dict[str, dict]) -> Tuple[dict, List[dict]]:
    if state["stage"] != "league" or state["matchday_index"] >= len(state["schedule"]):
        return state, []
    matchday = state["schedule"][state["matchday_index"]]
    results = []
    for match in matchday:
        if match["played"]:
            continue
        result = simulate_match(team_db[match["home"]], team_db[match["away"]], knockout=False)
        match["played"] = True
        match["result"] = result
        if state["mode"] in ("cup", "international") and "group" in match:
            update_standings(state["group_tables"][match["group"]], result)
        else:
            update_standings(state["standings"], result)
        merge_counter(state["top_scorers"], result["scorers"])
        merge_counter(state["top_assisters"], result["assisters"])
        state["history"].append(result)
        results.append(result)
    state["matchday_index"] += 1
    if state["matchday_index"] >= len(state["schedule"]):
        prepare_knockout_after_league(state)
    return state, results


def prepare_knockout_after_league(state: dict) -> None:
    if state["mode"] in ("league", "premier_league"):
        state["stage"] = "complete"
        table = sorted_table(state["standings"])
        state["champion"] = table[0]["Team"] if table else None
        return

    if state["mode"] in ("cup", "international"):
        qualifiers = []
        third_place_rows = []
        advance_top = state.get("config", {}).get("advance_top", 2) if state["mode"] == "international" else 2
        best_thirds = state.get("config", {}).get("best_thirds", 0) if state["mode"] == "international" else 0
        for group_name, table in state.get("group_tables", {}).items():
            sorted_group = sorted_table(table)
            qualifiers.extend([row["Team"] for row in sorted_group[:advance_top]])
            if len(sorted_group) > advance_top:
                third = sorted_group[advance_top].copy()
                third["Group"] = group_name
                third_place_rows.append(third)
        if best_thirds:
            best = sorted(third_place_rows, key=lambda r: (r["Pts"], r["GD"], r["GF"], r["W"], r["Team"]), reverse=True)[:best_thirds]
            qualifiers.extend([row["Team"] for row in best])
            state["config"]["best_thirds_qualified"] = best
        state["stage"] = "knockout"
        state["knockout_rounds"].append({"name": round_name(len(qualifiers)), "matches": knockout_pairs(qualifiers, seeded=True), "complete": False})
        return

    if state["mode"] == "uefa":
        table = sorted_table(state["standings"])
        top8 = [r["Team"] for r in table[:8]]
        playoff = [r["Team"] for r in table[8:24]]
        state["stage"] = "knockout"
        state["config"]["top8_waiting"] = top8
        state["knockout_rounds"].append({"name": "Knockout Play-offs", "matches": knockout_pairs(playoff, seeded=True), "complete": False})


def simulate_knockout_round(state: dict, team_db: Dict[str, dict]) -> Tuple[dict, List[dict]]:
    if state["stage"] != "knockout" or not state["knockout_rounds"]:
        return state, []
    current = state["knockout_rounds"][-1]
    if current.get("complete"):
        return state, []
    results = []
    winners = []
    for match in current["matches"]:
        if match["played"]:
            continue
        neutral = current["name"] == "Final" or (state.get("mode") == "fa_cup" and current["name"] in ("Semi-finals", "Final"))
        result = simulate_match(team_db[match["home"]], team_db[match["away"]], knockout=True, neutral=neutral)
        match["played"] = True
        match["result"] = result
        merge_counter(state["top_scorers"], result["scorers"])
        merge_counter(state["top_assisters"], result["assisters"])
        state["history"].append(result)
        results.append(result)
        winners.append(result["winner"])
    current["complete"] = True

    if len(winners) == 1:
        state["stage"] = "complete"
        state["champion"] = winners[0]
        return state, results

    if state["mode"] == "uefa" and current["name"] == "Knockout Play-offs":
        next_teams = state["config"].get("top8_waiting", []) + winners
        # Top 8 are treated as seeded; playoff winners are drawn against them.
        next_round = {"name": "Round of 16", "matches": knockout_pairs(next_teams, seeded=True), "complete": False}
    elif state.get("mode") == "fa_cup":
        next_round = {"name": fa_cup_round_name(len(winners)), "matches": knockout_pairs(winners, seeded=False), "complete": False}
    else:
        next_round = {"name": round_name(len(winners)), "matches": knockout_pairs(winners, seeded=True), "complete": False}
    state["knockout_rounds"].append(next_round)
    return state, results


def upcoming_matches(state: dict) -> List[dict]:
    if state["stage"] == "league" and state["matchday_index"] < len(state["schedule"]):
        return state["schedule"][state["matchday_index"]]
    if state["stage"] == "knockout" and state["knockout_rounds"]:
        return [m for m in state["knockout_rounds"][-1]["matches"] if not m["played"]]
    return []

# ===== Streamlit app =====
st.set_page_config(
    page_title="Football Simulator Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
:root {
    --bg-card: rgba(15, 23, 42, 0.88);
    --bg-card-strong: rgba(2, 6, 23, 0.92);
    --border: rgba(148, 163, 184, 0.25);
    --text-soft: #e2e8f0;
    --text-muted: #cbd5e1;
    --accent: #22c55e;
    --accent-2: #38bdf8;
    --gold: #facc15;
}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,.22), transparent 28%),
        radial-gradient(circle at top right, rgba(56,189,248,.20), transparent 30%),
        linear-gradient(135deg, #020617 0%, #08111f 48%, #0f172a 100%);
    color: #f8fafc;
}

.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp span,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p {
    color: #f8fafc !important;
}
.card, .instruction-card, .mode-card, .fixture-card, .result-card {
    color: #f8fafc !important;
}
.card p, .instruction-card p, .mode-card p, .fixture-card p, .result-card p {
    color: #e2e8f0 !important;
}
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] * {
    color: #f8fafc !important;
}
[data-testid="stTable"] table,
[data-testid="stTable"] th,
[data-testid="stTable"] td {
    color: #f8fafc !important;
}
.block-container {
    max-width: 1100px;
    padding: 1.15rem 1rem 5rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(2,6,23,.98), rgba(15,23,42,.96));
    border-right: 1px solid rgba(148,163,184,.18);
}
.hero {
    position: relative;
    overflow: hidden;
    padding: 1.45rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(34,197,94,.18), rgba(56,189,248,.12)), rgba(15,23,42,.74);
    border: 1px solid rgba(148, 163, 184, .25);
    box-shadow: 0 22px 70px rgba(0,0,0,.32);
    margin-bottom: 1rem;
}
.hero:after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    right: -70px;
    top: -70px;
    border-radius: 999px;
    background: rgba(250,204,21,.12);
    border: 1px solid rgba(250,204,21,.18);
}
.hero h1 {
    font-size: clamp(2.05rem, 8vw, 3.1rem);
    line-height: .96;
    margin: 0 0 .7rem 0;
    letter-spacing: -.055em;
}
.hero p { color: var(--text-soft); font-size: clamp(.98rem, 2.8vw, 1.08rem); max-width: 880px; }
.card, .instruction-card, .mode-card, .fixture-card, .result-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1rem;
    box-shadow: 0 12px 42px rgba(0,0,0,.25);
    margin-bottom: .85rem;
}
.instruction-grid, .mode-grid, .fixture-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .8rem;
}
.mode-card {
    min-height: 148px;
    background: linear-gradient(145deg, rgba(15,23,42,.95), rgba(30,41,59,.70));
}
.mode-card h3, .instruction-card h4 { margin-top: 0; margin-bottom: .35rem; }
.mode-card p, .instruction-card p, .fixture-card p, .result-card p { color: var(--text-soft); margin-bottom: .25rem; }
.fixture-card { padding: .9rem; }
.fixture-vs {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .6rem;
    font-weight: 800;
}
.fixture-vs span { flex: 1; }
.fixture-vs .away { text-align: right; }
.vs-pill {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 30px;
    border-radius: 999px;
    background: rgba(56,189,248,.13);
    border: 1px solid rgba(56,189,248,.24);
    color: #bae6fd;
    font-size: .78rem;
}
.scoreline {
    font-size: clamp(1.12rem, 5.4vw, 1.45rem);
    font-weight: 900;
    letter-spacing: -.03em;
    color: #f8fafc;
}
.pill {
    display: inline-block;
    padding: .22rem .6rem;
    border-radius: 999px;
    background: rgba(34,197,94,.14);
    color: #bbf7d0;
    border: 1px solid rgba(34,197,94,.24);
    font-size: .82rem;
    margin: .15rem .18rem .15rem 0;
    white-space: nowrap;
}
.danger-pill { background: rgba(239,68,68,.14); color: #fecaca; border-color: rgba(239,68,68,.25); }
.info-pill { background: rgba(56,189,248,.14); color: #bae6fd; border-color: rgba(56,189,248,.25); }
.gold-pill { background: rgba(250,204,21,.14); color: #fef08a; border-color: rgba(250,204,21,.26); }
.stButton>button {
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,.22);
    font-weight: 800;
    min-height: 48px;
    width: 100%;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #0ea5e9);
    border: 0;
}
[data-testid="stMetric"] {
    background: rgba(15,23,42,.74);
    border: 1px solid rgba(148,163,184,.2);
    border-radius: 18px;
    padding: .85rem;
}
hr { border-color: rgba(148,163,184,.16); }
.winner-card {
    position: relative;
    overflow: hidden;
    border-radius: 32px;
    padding: 1.6rem 1.1rem;
    min-height: 270px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background:
        radial-gradient(circle at top, rgba(250,204,21,.36), transparent 32%),
        radial-gradient(circle at bottom left, rgba(34,197,94,.25), transparent 35%),
        linear-gradient(145deg, rgba(15,23,42,.97), rgba(30,41,59,.86));
    border: 1px solid rgba(250,204,21,.34);
    box-shadow: 0 26px 80px rgba(0,0,0,.42);
    margin: 1rem 0;
}
.trophy {
    font-size: clamp(4rem, 22vw, 7.5rem);
    line-height: .95;
    filter: drop-shadow(0 18px 34px rgba(250,204,21,.22));
    animation: trophy-pop 900ms ease-out both, trophy-glow 2.8s ease-in-out infinite;
}
.winner-card h2 {
    margin: .4rem 0 .15rem;
    font-size: clamp(1.75rem, 8vw, 3.4rem);
    line-height: .95;
    letter-spacing: -.055em;
}
.winner-card p { color: var(--text-soft); margin: .3rem auto; max-width: 680px; }
.confetti {
    position: absolute;
    width: 9px;
    height: 15px;
    border-radius: 3px;
    opacity: .9;
    animation: fall 3.6s linear infinite;
}
.confetti.c1 { left: 8%; top: -20px; background: #22c55e; animation-delay: .1s; }
.confetti.c2 { left: 21%; top: -25px; background: #38bdf8; animation-delay: .9s; }
.confetti.c3 { left: 38%; top: -25px; background: #facc15; animation-delay: .35s; }
.confetti.c4 { left: 53%; top: -35px; background: #fb7185; animation-delay: 1.25s; }
.confetti.c5 { left: 69%; top: -30px; background: #a78bfa; animation-delay: .65s; }
.confetti.c6 { left: 86%; top: -30px; background: #34d399; animation-delay: 1.6s; }
@keyframes fall {
    0% { transform: translateY(-20px) rotate(0deg); }
    100% { transform: translateY(360px) rotate(420deg); }
}
@keyframes trophy-pop {
    0% { transform: scale(.72); opacity: 0; }
    70% { transform: scale(1.08); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes trophy-glow {
    0%, 100% { filter: drop-shadow(0 18px 34px rgba(250,204,21,.18)); }
    50% { filter: drop-shadow(0 22px 48px rgba(250,204,21,.42)); }
}
.mobile-note {
    background: rgba(56,189,248,.10);
    border: 1px solid rgba(56,189,248,.22);
    color: #dbeafe;
    border-radius: 18px;
    padding: .75rem .9rem;
    margin-bottom: .9rem;
}

.next-action-card {
    background: linear-gradient(135deg, rgba(34,197,94,.18), rgba(56,189,248,.10)), rgba(15,23,42,.9);
    border: 1px solid rgba(34,197,94,.32);
    border-radius: 22px;
    padding: 1rem;
    margin: .95rem 0;
    box-shadow: 0 12px 42px rgba(0,0,0,.24);
}
.next-action-card h3 {
    margin: 0 0 .35rem;
    color: #ffffff !important;
    letter-spacing: -.02em;
}
.next-action-card p, .next-action-card li {
    color: #e2e8f0 !important;
    margin: .2rem 0;
}
.next-action-card .next-label {
    display: inline-block;
    margin-bottom: .35rem;
    padding: .22rem .58rem;
    border-radius: 999px;
    background: rgba(250,204,21,.16);
    color: #fef9c3 !important;
    border: 1px solid rgba(250,204,21,.32);
    font-size: .82rem;
    font-weight: 900;
}
.result-story {
    margin-top: .6rem;
    color: #e2e8f0 !important;
    font-size: .96rem;
    line-height: 1.35;
}

.mini-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .45rem;
    margin-top: .7rem;
}
.mini-stat {
    background: rgba(2, 6, 23, .42);
    border: 1px solid rgba(148, 163, 184, .22);
    border-radius: 14px;
    padding: .55rem .62rem;
    color: #f8fafc !important;
}
.mini-stat b {
    display: block;
    font-size: .74rem;
    color: #e2e8f0 !important;
    opacity: .96;
    margin-bottom: .16rem;
}
.mini-stat span {
    color: #ffffff !important;
    font-weight: 900;
    letter-spacing: -.02em;
}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] * {
    color: #f8fafc !important;
}
.stSelectbox label,
.stMultiSelect label,
.stRadio label,
.stCheckbox label,
.stSlider label,
.stTextInput label,
.stFileUploader label {
    color: #f8fafc !important;
}


.team-chip {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    min-width: 0;
}
.crest {
    width: 30px;
    height: 30px;
    border-radius: 10px 10px 13px 13px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .72rem;
    font-weight: 950;
    border: 1px solid rgba(255,255,255,.28);
    box-shadow: inset 0 -8px 12px rgba(0,0,0,.15), 0 6px 18px rgba(0,0,0,.22);
    flex: 0 0 auto;
}
.team-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.live-card {
    background: linear-gradient(135deg, rgba(250,204,21,.14), rgba(34,197,94,.12)), rgba(15,23,42,.94);
    border: 1px solid rgba(250,204,21,.30);
    border-radius: 22px;
    padding: 1rem;
    margin: .85rem 0;
    box-shadow: 0 16px 52px rgba(0,0,0,.30);
}
.live-minute { color: #fef08a !important; font-weight: 950; font-size: .92rem; }
.live-event { color: #ffffff !important; font-weight: 850; font-size: 1.05rem; margin: .22rem 0 .45rem; }
.score-strip {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .45rem;
    margin-top: .7rem;
}
.score-tile {
    border: 1px solid rgba(148,163,184,.22);
    background: rgba(2,6,23,.48);
    border-radius: 14px;
    padding: .48rem .55rem;
    color: #f8fafc !important;
    font-weight: 850;
    font-size: .88rem;
}
.mobile-action-bar {
    position: sticky;
    bottom: .35rem;
    z-index: 10;
    background: rgba(2,6,23,.92);
    border: 1px solid rgba(56,189,248,.28);
    border-radius: 20px;
    padding: .72rem;
    margin: .85rem 0;
    box-shadow: 0 18px 58px rgba(0,0,0,.42);
    backdrop-filter: blur(10px);
}
.mobile-action-bar b { color: #ffffff !important; }
.mobile-action-bar span { color: #e2e8f0 !important; }
.stButton>button,
.stDownloadButton>button,
button[kind="secondary"],
button[kind="primary"] {
    background: linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.94)) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148,163,184,.32) !important;
}
.stButton>button:hover,
.stButton>button:focus,
.stButton>button:active,
.stDownloadButton>button:hover,
.stDownloadButton>button:focus,
.stDownloadButton>button:active {
    background: linear-gradient(135deg, #16a34a, #0ea5e9) !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,.26) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.22) !important;
}
.stButton>button[kind="primary"], button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #0ea5e9) !important;
    color: #ffffff !important;
    border: 0 !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span,
div[data-baseweb="popover"],
div[role="listbox"],
div[role="option"],
ul[role="listbox"] li {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}
div[role="option"]:hover,
ul[role="listbox"] li:hover {
    background-color: #1e293b !important;
    color: #ffffff !important;
}
.stRadio div[role="radiogroup"] label,
.stRadio div[role="radiogroup"] span {
    color: #f8fafc !important;
}


.watch-panel {
    background: linear-gradient(135deg, rgba(56,189,248,.14), rgba(34,197,94,.12)), rgba(15,23,42,.92);
    border: 1px solid rgba(56,189,248,.30);
    border-radius: 22px;
    padding: 1rem;
    margin: .8rem 0;
    box-shadow: 0 12px 42px rgba(0,0,0,.24);
}
.watch-panel h3 { margin: .1rem 0 .25rem; color: #ffffff !important; line-height: 1.12; }
.watch-panel p { color: #e2e8f0 !important; margin: 0; }
.fixture-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}
.fixture-readable {
    min-height: 138px;
    padding: 1rem;
}
.fixture-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: .75rem;
    align-items: center;
    padding: .35rem 0;
}
.fixture-row.away-row {
    border-top: 1px solid rgba(148,163,184,.13);
    margin-top: .25rem;
    padding-top: .55rem;
}
.fixture-side {
    font-size: .74rem;
    font-weight: 900;
    letter-spacing: .04em;
    text-transform: uppercase;
    color: #bae6fd !important;
    background: rgba(56,189,248,.12);
    border: 1px solid rgba(56,189,248,.22);
    padding: .18rem .45rem;
    border-radius: 999px;
    white-space: nowrap;
}
.fixture-separator {
    width: 34px;
    height: 25px;
    margin: .12rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    color: #ffffff !important;
    background: rgba(56,189,248,.16);
    border: 1px solid rgba(56,189,248,.24);
    font-size: .76rem;
    font-weight: 950;
}
.fixture-meta { margin-top: .3rem; }
.team-chip {
    max-width: 100%;
    font-size: .98rem;
    line-height: 1.18;
}
.team-name {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    word-break: normal;
}
.result-readable {
    padding: 1.05rem;
}
.result-score-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: .75rem;
    align-items: center;
    margin-bottom: .65rem;
}
.result-team {
    min-width: 0;
}
.result-team .team-chip {
    width: 100%;
    font-size: 1.05rem;
    font-weight: 950;
}
.away-result .team-chip {
    justify-content: flex-end;
    text-align: right;
}
.big-score {
    color: #ffffff !important;
    font-size: clamp(2rem, 10vw, 3.1rem);
    line-height: .95;
    font-weight: 1000;
    letter-spacing: -.05em;
    white-space: nowrap;
    text-shadow: 0 10px 32px rgba(56,189,248,.18);
}
.result-pills { margin: .45rem 0 .2rem; }
.live-stage {
    position: relative;
    padding: 1rem;
}
.match-clock {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: .75rem;
    align-items: center;
    margin-bottom: .8rem;
}
.match-clock strong {
    color: #fef08a !important;
    font-size: 1.45rem;
    line-height: 1;
    display: block;
}
.match-clock span {
    display: block;
    color: #e2e8f0 !important;
    font-size: .78rem;
    font-weight: 800;
}
.clock-track {
    height: 12px;
    width: 100%;
    background: rgba(15,23,42,.82);
    border: 1px solid rgba(148,163,184,.25);
    border-radius: 999px;
    overflow: hidden;
}
.clock-fill {
    height: 100%;
    background: linear-gradient(90deg, #22c55e, #38bdf8, #facc15);
    border-radius: 999px;
    transition: width .45s ease;
}
.live-event-big {
    display: flex;
    gap: .55rem;
    align-items: flex-start;
    color: #ffffff !important;
    font-size: clamp(1.05rem, 4.8vw, 1.35rem);
    font-weight: 950;
    line-height: 1.2;
    background: rgba(2,6,23,.40);
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 16px;
    padding: .75rem;
}
.live-event-big span {
    flex: 0 0 auto;
}
.recent-events {
    margin-top: .75rem;
    border-top: 1px solid rgba(148,163,184,.16);
    padding-top: .65rem;
}
.recent-events b {
    display: block;
    color: #ffffff !important;
    margin-bottom: .35rem;
}
.recent-line {
    color: #e2e8f0 !important;
    font-size: .9rem;
    line-height: 1.25;
    padding: .18rem 0;
}
.recent-line span {
    color: #fef08a !important;
    font-weight: 950;
    margin-right: .35rem;
}
.score-strip {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}
.score-tile {
    font-size: .82rem;
    line-height: 1.2;
}
.score-tile strong {
    display: inline-block;
    color: #ffffff !important;
    font-size: 1.22rem;
    margin: .2rem 0;
}

@media (max-width: 760px) {
    .block-container { padding: .75rem .65rem 5.5rem; }
    .hero { padding: 1.05rem; border-radius: 22px; }
    .instruction-grid, .mode-grid, .fixture-grid { grid-template-columns: 1fr; gap: .65rem; }
    .mini-stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .48rem; }
    .mode-card, .instruction-card, .fixture-card, .result-card { border-radius: 18px; padding: .88rem; min-height: auto; }
    [data-testid="stHorizontalBlock"] { gap: .55rem; }
    [data-testid="stMetric"] { padding: .72rem; }
    .stTabs [data-baseweb="tab-list"] { gap: .25rem; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { padding: .45rem .7rem; }
    .winner-card { min-height: 245px; border-radius: 24px; padding: 1.15rem .8rem; }
    .fixture-grid { grid-template-columns: 1fr !important; }
    .fixture-readable { min-height: auto; padding: .95rem; }
    .team-chip { font-size: 1rem; }
    .crest { width: 34px; height: 34px; font-size: .74rem; }
    .result-score-grid { grid-template-columns: 1fr; text-align: left; gap: .45rem; }
    .away-result .team-chip { justify-content: flex-start !important; text-align: left !important; }
    .big-score { font-size: 3rem; text-align: left; padding: .25rem 0; }
    .score-strip { grid-template-columns: 1fr; }
    .score-tile { font-size: .92rem; }
    .match-clock { grid-template-columns: 1fr; gap: .45rem; }
    .mobile-action-bar { bottom: .2rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def h(value: object) -> str:
    """Escape dynamic values before inserting them into unsafe HTML blocks."""
    return escape(str(value), quote=True)


def compact_markup(markup: str) -> str:
    """Flatten custom HTML so Streamlit/Markdown never treats indented tags as code."""
    return " ".join(line.strip() for line in dedent(markup).strip().splitlines())


def render_html(markup: str) -> None:
    """Render custom HTML safely without Markdown turning indented tags into code blocks."""
    st.markdown(compact_markup(markup), unsafe_allow_html=True)


def init() -> None:
    if "team_db" not in st.session_state:
        st.session_state.team_db = {team["name"]: deepcopy(team) for team in TEAMS}
    if "game" not in st.session_state:
        st.session_state.game = None
    if "last_results" not in st.session_state:
        st.session_state.last_results = []
    if "quick_match_result" not in st.session_state:
        st.session_state.quick_match_result = None
    if "start_mode" not in st.session_state:
        st.session_state.start_mode = "🏴 Domestic Cups/Leagues"
    if "show_inline_results" not in st.session_state:
        st.session_state.show_inline_results = False
    if "last_watch_teams" not in st.session_state:
        st.session_state.last_watch_teams = []


def hero() -> None:
    render_html(
        """
        <div class="hero">
            <h1>⚽ Football Simulator Pro</h1>
            <p>
            A mobile-first text football universe. Create teams, run the Premier League, FA Cup, World Cups, EUROs, leagues, cups and European club tournaments,
            then simulate one matchday or knockout round at a time with stat-weighted winners, real-player scorers,
            late-drama upsets, live 60-second play mode, assists, detailed match stats, injuries, tables and trophy celebrations.
            </p>
            <span class="pill">📱 Mobile-first</span>
            <span class="pill info-pill">One command at a time</span>
            <span class="pill">Real-player squads</span>
            <span class="pill gold-pill">Trophy winner graphic</span>
            <span class="pill info-pill">🎬 Watch Live mode</span>
        </div>
        """
    )


def instructions_panel(compact: bool = False) -> None:
    title = "How to play" if not compact else "Quick instructions"
    st.markdown(f"### {title}")
    render_html(
        """
        <div class="instruction-grid">
            <div class="instruction-card">
                <h4>1. Choose a mode</h4>
                <p>Start with the World Cup, EURO, a real continental club tournament, your own competition, or a quick match.</p>
            </div>
            <div class="instruction-card">
                <h4>2. Simulate safely</h4>
                <p>The game never runs ahead. Press one button to simulate the next matchday or knockout round only.</p>
            </div>
            <div class="instruction-card">
                <h4>3. Review the world</h4>
                <p>Open results, tables, brackets, player stats, teams and save/load from the tabs after each command.</p>
            </div>
        </div>
        """
    )
    if not compact:
        render_html(
            """
            <div class="mobile-note">
                <strong>Phone tip:</strong> the sidebar starts closed. Use the top-left arrow only when you want reset,
                database filtering, or save guidance. Main controls stay in the page so it feels app-like on mobile.
            </div>
            """
        )


def winner_graphic(champion: str | None, competition: str) -> None:
    if not champion:
        return
    render_html(
        f"""
        <div class="winner-card">
            <div class="confetti c1"></div><div class="confetti c2"></div><div class="confetti c3"></div>
            <div class="confetti c4"></div><div class="confetti c5"></div><div class="confetti c6"></div>
            <div>
                <div class="trophy">🏆</div>
                <span class="pill gold-pill">Champions crowned</span>
                <h2>{h(champion)}</h2>
                <p>{h(champion)} have won <strong>{h(competition)}</strong>. Save this universe or start a new competition.</p>
            </div>
        </div>
        """
    )


def get_teams_by_names(names: List[str]) -> List[dict]:
    return [deepcopy(st.session_state.team_db[n]) for n in names if n in st.session_state.team_db]


def teams_table_rows(teams: List[dict]) -> List[dict]:
    rows = []
    for t in teams:
        rows.append({
            "Flag": t.get("flag", ""),
            "Team": t.get("name"),
            "Badge": t.get("abbr", ""),
            "Country": t.get("country"),
            "League": t.get("league"),
            "OVR": t.get("overall"),
            "ATT": t.get("attack"),
            "MID": t.get("midfield"),
            "DEF": t.get("defence"),
            "Star Player": t.get("star_player"),
            "Squad": len(t.get("players") or []),
        })
    return rows


def team_chip_html(team_name: str, align: str = "left") -> str:
    team = st.session_state.team_db.get(team_name, {})
    flag = team.get("flag", "🏳️")
    abbr = team.get("abbr", team_name[:3].upper())
    primary = team.get("crest_primary", "#334155")
    secondary = team.get("crest_secondary", "#f8fafc")
    name = h(team_name)
    if align == "right":
        return (
            f"<span class='team-chip' style='justify-content:flex-end'>"
            f"<span class='team-name'>{name}</span><span>{h(flag)}</span>"
            f"<span class='crest' style='background:{h(primary)};color:{h(secondary)}'>{h(abbr)}</span></span>"
        )
    return (
        f"<span class='team-chip'><span class='crest' style='background:{h(primary)};color:{h(secondary)}'>{h(abbr)}</span>"
        f"<span>{h(flag)}</span><span class='team-name'>{name}</span></span>"
    )


def fixture_cards(fixtures: List[dict], title: str | None = None, limit: int = 12) -> None:
    if not fixtures:
        st.info("No fixtures waiting.")
        return
    if title:
        st.markdown(title)

    cards: List[str] = []
    for match in fixtures[:limit]:
        group = match.get("group")
        group_html = f"<span class='pill info-pill'>Group {h(group)}</span>" if group else ""
        cards.append(
            "<div class='fixture-card fixture-readable'>"
            f"<div class='fixture-row'><div>{team_chip_html(match['home'])}</div><span class='fixture-side'>Home</span></div>"
            "<div class='fixture-separator'>v</div>"
            f"<div class='fixture-row away-row'><div>{team_chip_html(match['away'])}</div><span class='fixture-side'>Away</span></div>"
            f"<div class='fixture-meta'>{group_html}</div>"
            "</div>"
        )

    render_html("<div class='fixture-grid'>" + "".join(cards) + "</div>")
    if len(fixtures) > limit:
        st.caption(f"Showing {limit} of {len(fixtures)} fixtures. Full fixture table is below.")
        st.dataframe(
            [{"Home": m["home"], "Away": m["away"], "Group": m.get("group", "—")} for m in fixtures],
            hide_index=True,
            use_container_width=True,
        )


def watch_selector_panel(fixtures: List[dict], key_prefix: str) -> List[str]:
    """Mobile-friendly selector for 1-3 teams to focus the live broadcast."""
    if not fixtures:
        return []
    options: List[str] = []
    for match in fixtures:
        for name in (match["home"], match["away"]):
            if name not in options:
                options.append(name)
    default = st.session_state.get(f"{key_prefix}_watch_defaults")
    if not default:
        default = [fixtures[0]["home"]]
        st.session_state[f"{key_prefix}_watch_defaults"] = default
    selected = st.multiselect(
        "Pick 1, 2 or 3 teams to watch live",
        options,
        default=[name for name in default if name in options][:3],
        key=f"{key_prefix}_watch_teams",
        help="Watch Live focuses on these teams so the phone screen is easier to follow. The other fixtures are still simulated and shown after.",
    )
    if len(selected) > 3:
        st.warning("Watch mode is limited to 3 teams so the live feed stays readable. I’ll use the first 3 you selected.")
        selected = selected[:3]
    watched = [m for m in fixtures if m["home"] in selected or m["away"] in selected]
    if selected:
        render_html(
            "<div class='watch-panel'>"
            "<span class='next-label'>WATCH FOCUS</span>"
            f"<h3>{h(', '.join(selected))}</h3>"
            "<p>🎬 Watch Live will follow these teams first. Full matchday results appear after the live feed.</p>"
            "</div>"
        )
        fixture_cards(watched[:3], title="#### Watched fixtures", limit=3)
    else:
        st.info("Pick at least one team for Watch Live, or use Quick Sim for the whole matchday.")
    return selected


def match_stats_rows(result: dict) -> List[dict]:
    stats = result.get("match_stats") or {}
    home_stats = stats.get(result.get("home"), {})
    away_stats = stats.get(result.get("away"), {})
    labels = [
        ("Possession", "possession", "%"),
        ("Shots", "shots", ""),
        ("Shots on target", "shots_on_target", ""),
        ("Big chances", "big_chances", ""),
        ("Corners", "corners", ""),
        ("Fouls", "fouls", ""),
        ("Pass accuracy", "pass_accuracy", "%"),
        ("Keeper saves", "keeper_saves", ""),
    ]
    rows = []
    for label, key, suffix in labels:
        h_value = home_stats.get(key, "—")
        a_value = away_stats.get(key, "—")
        if h_value != "—" and suffix:
            h_value = f"{h_value}{suffix}"
        if a_value != "—" and suffix:
            a_value = f"{a_value}{suffix}"
        rows.append({"Stat": label, result.get("home", "Home"): h_value, result.get("away", "Away"): a_value})
    return rows


def match_summary_html(result: dict) -> str:
    stats = result.get("match_stats") or {}
    home = result.get("home")
    away = result.get("away")
    home_stats = stats.get(home, {})
    away_stats = stats.get(away, {})
    if not home_stats or not away_stats:
        return ""
    return (
        "<div class='mini-stat-grid'>"
        f"<div class='mini-stat'><b>Possession</b><span>{h(home_stats.get('possession', '—'))}%–{h(away_stats.get('possession', '—'))}%</span></div>"
        f"<div class='mini-stat'><b>Shots</b><span>{h(home_stats.get('shots', '—'))}–{h(away_stats.get('shots', '—'))}</span></div>"
        f"<div class='mini-stat'><b>On target</b><span>{h(home_stats.get('shots_on_target', '—'))}–{h(away_stats.get('shots_on_target', '—'))}</span></div>"
        f"<div class='mini-stat'><b>Corners</b><span>{h(home_stats.get('corners', '—'))}–{h(away_stats.get('corners', '—'))}</span></div>"
        "</div>"
    )


def match_story(result: dict) -> str:
    stats = result.get("match_stats") or {}
    home = result.get("home")
    away = result.get("away")
    home_stats = stats.get(home, {})
    away_stats = stats.get(away, {})
    if not home_stats or not away_stats:
        return ""
    home_shots = home_stats.get("shots", 0)
    away_shots = away_stats.get("shots", 0)
    home_poss = home_stats.get("possession", 0)
    away_poss = away_stats.get("possession", 0)
    if result.get("home_goals", 0) > result.get("away_goals", 0):
        winner = home
    elif result.get("away_goals", 0) > result.get("home_goals", 0):
        winner = away
    else:
        winner = None
    if winner:
        if abs(home_shots - away_shots) >= 5:
            dominant = home if home_shots > away_shots else away
            return f"{dominant} created the greater volume of chances, while {winner} made the scoreboard count."
        if abs(home_poss - away_poss) >= 10:
            controller = home if home_poss > away_poss else away
            return f"{controller} controlled long spells of possession, but {winner} found the decisive moments."
        return "A tight game decided by finishing quality and key moments in both boxes."
    return "A balanced contest with both teams having spells of pressure but neither side doing enough to win it."


def _score_tiles(scores: dict, results: List[dict], limit: int = 6) -> str:
    tiles = []
    for r in results[:limit]:
        sc = scores.get(r["id"], {"home": 0, "away": 0})
        tiles.append(
            f"<div class='score-tile'>{team_chip_html(r['home'])}<br><strong>{sc['home']}–{sc['away']}</strong><br>{team_chip_html(r['away'])}</div>"
        )
    return "<div class='score-strip'>" + "".join(tiles) + "</div>"


def _live_feed(results: List[dict]) -> List[dict]:
    feed: List[dict] = []
    for r in results:
        feed.append({"minute": 0, "result_id": r["id"], "text": f"Kick-off: {r['home']} v {r['away']}", "type": "kickoff"})
        for ev in r.get("timeline", []):
            feed.append({"minute": int(ev.get("minute", 0)), "result_id": r["id"], "text": ev.get("text", ""), "type": ev.get("type", "event"), "team": ev.get("team")})
        feed.append({"minute": 45, "result_id": r["id"], "text": f"Half-time: {r['home']} v {r['away']}", "type": "half_time"})
        feed.append({"minute": 96, "result_id": r["id"], "text": f"Full-time: {r['home']} {r['home_goals']}–{r['away_goals']} {r['away']}", "type": "full_time"})
    return sorted(feed, key=lambda e: (e["minute"], e["result_id"], e["text"]))


def _focus_results(results: List[dict], watch_teams: List[str] | None = None) -> List[dict]:
    if not watch_teams:
        return results[:3]
    focused = [r for r in results if r["home"] in watch_teams or r["away"] in watch_teams]
    return focused[:3] if focused else results[:3]


def _ordered_results(results: List[dict], watch_teams: List[str] | None = None) -> List[dict]:
    if not watch_teams:
        return results
    focused = [r for r in results if r["home"] in watch_teams or r["away"] in watch_teams]
    rest = [r for r in results if r not in focused]
    return focused + rest


def _event_icon(event_type: str) -> str:
    return {
        "goal": "⚽",
        "save": "🧤",
        "chance": "🔥",
        "pressure": "🚩",
        "control": "🎛️",
        "late": "⏳",
        "card": "🟨",
        "injury": "🚑",
        "full_time": "✅",
        "half_time": "☕",
        "kickoff": "▶️",
        "penalties": "🥅",
        "extra_time": "⏱️",
    }.get(event_type, "•")


def live_broadcast(results: List[dict], seconds: int = 60, watch_teams: List[str] | None = None) -> None:
    if not results:
        st.info("No live events to show.")
        return
    focused_results = _focus_results(results, watch_teams)
    watch_label = ", ".join(watch_teams or []) if watch_teams else "featured matches"
    st.markdown("### 🎬 Live match centre")
    st.caption(f"Watching {watch_label}. The rest of the matchday is simulated quietly and shown after the live feed.")

    stage = st.empty()
    progress = st.progress(0)
    feed = _live_feed(focused_results)
    scores = {r["id"]: {"home": 0, "away": 0} for r in focused_results}
    result_lookup = {r["id"]: r for r in focused_results}
    recent: List[str] = []
    delay = max(0.55, min(2.8, seconds / max(1, len(feed))))

    for idx, ev in enumerate(feed, start=1):
        r = result_lookup[ev["result_id"]]
        if ev.get("type") == "goal":
            if ev.get("team") == r["home"]:
                scores[r["id"]]["home"] += 1
            elif ev.get("team") == r["away"]:
                scores[r["id"]]["away"] += 1
        minute = ev.get("minute", 0)
        label = "90+" + str(minute - 90) if 91 <= minute <= 99 else ("FT" if minute >= 96 else str(minute) + "'")
        clock_pct = min(100, max(0, int(minute / 96 * 100)))
        icon = _event_icon(ev.get("type", "event"))
        event_line = f"<div class='recent-line'><span>{h(label)}</span> {h(ev['text'])}</div>"
        recent.append(event_line)
        recent_html = "".join(recent[-5:])
        stage.markdown(
            compact_markup(
                f"""
                <div class='live-card live-stage'>
                    <div class='match-clock'>
                        <div><strong>{h(label)}</strong><span>Match clock</span></div>
                        <div class='clock-track'><div class='clock-fill' style='width:{clock_pct}%'></div></div>
                    </div>
                    <div class='live-event-big'><span>{h(icon)}</span>{h(ev['text'])}</div>
                    {_score_tiles(scores, focused_results, limit=3)}
                    <div class='recent-events'><b>Latest movements</b>{recent_html}</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
        progress.progress(min(100, int(idx / len(feed) * 100)))
        if idx < len(feed):
            time.sleep(delay)
    st.success("Live simulation complete. Watched results are below, followed by the rest of the matchday.")


def play_next(game: dict, live: bool, key_note: str = "", watch_teams: List[str] | None = None) -> None:
    if game.get("stage") == "league":
        new_game, results = simulate_matchday(game, st.session_state.team_db)
    elif game.get("stage") == "knockout":
        new_game, results = simulate_knockout_round(game, st.session_state.team_db)
    else:
        return
    st.session_state.last_watch_teams = watch_teams or []
    if live:
        live_broadcast(results, seconds=60, watch_teams=watch_teams)
        st.session_state.game = new_game
        st.session_state.last_results = results
        st.session_state.show_inline_results = True
        show_results(results, focus_teams=watch_teams)
        st.info("Tables/brackets are updated in the saved state. Tap any tab or Refresh after live mode to redraw the full page.")
        if st.button("🔄 Refresh updated tables", key=f"refresh_after_live_{key_note}"):
            st.rerun()
    else:
        st.session_state.game = new_game
        st.session_state.last_results = results
        st.session_state.show_inline_results = True
        st.rerun()


def action_buttons(game: dict, key_prefix: str, sticky: bool = False, watch_teams: List[str] | None = None) -> None:
    if game.get("stage") not in ("league", "knockout"):
        return
    if sticky:
        render_html("<div class='mobile-action-bar'><b>Bottom menu</b><br><span>Watch selected teams, quick sim the next stage, or show result cards.</span></div>")
    c1, c2, c3 = st.columns(3)
    with c1:
        live_label = "🎬 Watch selected" if watch_teams else "🎬 Watch Live"
        if st.button(live_label, type="primary", key=f"{key_prefix}_watch_live"):
            play_next(game, live=True, key_note=key_prefix, watch_teams=watch_teams)
    with c2:
        label = "⚡ Quick Sim"
        if game.get("stage") == "league":
            label = f"⚡ Matchday {game.get('matchday_index', 0) + 1}"
        elif game.get("stage") == "knockout":
            label = "⚡ Round"
        if st.button(label, key=f"{key_prefix}_quick_sim"):
            play_next(game, live=False, key_note=key_prefix, watch_teams=watch_teams)
    with c3:
        if st.button("📋 Show Results", key=f"{key_prefix}_show_results"):
            st.session_state.show_inline_results = True



def next_action_panel(game: dict, context: str = "top") -> None:
    stage = game.get("stage")
    if stage == "league":
        title = f"Next: simulate matchday {game.get('matchday_index', 0) + 1}"
        body = "Use 🎬 Watch Live for a 60-second event feed, or ⚡ Quick Sim for instant results. The game pauses again after this matchday."
    elif stage == "knockout":
        current = game.get("knockout_rounds", [{}])[-1].get("name", "knockout round")
        title = f"Next: simulate {current}"
        body = "Use 🎬 Watch Live for a dramatic round reveal, or ⚡ Quick Sim for instant results. The game pauses before the next round."
    elif stage == "complete":
        title = "Tournament complete"
        body = "The champion has been crowned. Save your universe or start a new game."
    else:
        title = "Next step"
        body = "Choose a mode, then create a competition."
    render_html(
        f'''
        <div class="next-action-card">
            <span class="next-label">WHAT TO CLICK NEXT</span>
            <h3>{h(title)}</h3>
            <p>{h(body)}</p>
            <p><strong>Mobile tip:</strong> results are shown below as cards. Open View match details for timeline and full stats.</p>
        </div>
        '''
    )


def continue_button(game: dict, key: str) -> None:
    # Backwards-compatible wrapper used by older UI locations/tests.
    action_buttons(game, key_prefix=key, watch_teams=st.session_state.get("last_watch_teams", []))


def show_results(results: List[dict], focus_teams: List[str] | None = None) -> None:
    if not results:
        st.info("No results yet. Simulate the next matchday or round when you are ready.")
        return
    ordered = _ordered_results(results, focus_teams)
    for idx, r in enumerate(ordered):
        focused = bool(focus_teams and (r["home"] in focus_teams or r["away"] in focus_teams))
        focus_badge = "<span class='pill gold-pill'>Watched game</span>" if focused else ""
        winner = f"<span class='pill gold-pill'>Winner: {h(r['winner'])}</span>" if r.get("winner") else ""
        penalties = ""
        if r.get("penalties"):
            penalties = f"<span class='pill info-pill'>Pens {r['penalties']['home']}–{r['penalties']['away']}</span>"
        summary = match_summary_html(r)
        render_html(
            f"""
            <div class="result-card result-readable">
                <div class="result-score-grid">
                    <div class="result-team">{team_chip_html(r['home'])}</div>
                    <div class="big-score">{h(r['home_goals'])}–{h(r['away_goals'])}</div>
                    <div class="result-team away-result">{team_chip_html(r['away'], align='right')}</div>
                </div>
                <div class="result-pills">
                    {focus_badge}
                    <span class="pill info-pill">xG {r['home_xg']}–{r['away_xg']}</span>
                    <span class="pill info-pill">Power {r.get('home_power', '—')}–{r.get('away_power', '—')}</span>
                    <span class="pill">{h(r['played_at'])}</span>
                    {winner}{penalties}
                </div>
                {summary}
                <p class="result-story">{h(match_story(r))}</p>
            </div>
            """
        )
        with st.expander(f"View match details: {r['home']} v {r['away']}", expanded=(idx == 0 and len(results) == 1)):
            stat_rows = match_stats_rows(r)
            if r.get("match_stats"):
                st.markdown("#### Match stats")
                st.dataframe(stat_rows, hide_index=True, use_container_width=True)
            st.markdown("#### Timeline")
            for event in r["events"]:
                st.write(event)


def show_tables(game: dict) -> None:
    if game["mode"] in ("cup", "international") and game.get("group_tables"):
        tabs = st.tabs([f"Group {g}" for g in sorted(game["group_tables"].keys())])
        for tab, group_name in zip(tabs, sorted(game["group_tables"].keys())):
            with tab:
                st.dataframe(sorted_table(game["group_tables"][group_name]), hide_index=True, use_container_width=True)
        best_thirds = game.get("config", {}).get("best_thirds_qualified")
        if best_thirds:
            st.markdown("### Best third-placed qualifiers")
            st.dataframe(best_thirds, hide_index=True, use_container_width=True)
    else:
        table = sorted_table(game["standings"])
        if table:
            st.dataframe(table, hide_index=True, use_container_width=True)
        else:
            st.info("No league table yet.")


def show_bracket(game: dict) -> None:
    if not game.get("knockout_rounds"):
        st.info("No knockout bracket yet. Finish the league/group stage first or create a knockout tournament.")
        return
    for rnd in game["knockout_rounds"]:
        st.markdown(f"### {rnd['name']}")
        rows = []
        for m in rnd["matches"]:
            if m["played"] and m.get("result"):
                r = m["result"]
                score = f"{r['home_goals']}–{r['away_goals']}"
                winner = r.get("winner") or "—"
            else:
                score = "v"
                winner = "Pending"
            rows.append({"Home": m["home"], "Score": score, "Away": m["away"], "Winner": winner})
        st.dataframe(rows, hide_index=True, use_container_width=True)


def show_stats(game: dict) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Top scorers")
        scorer_rows = top_list(game.get("top_scorers", {}), 12)
        if scorer_rows:
            st.dataframe(scorer_rows, hide_index=True, use_container_width=True)
        else:
            st.caption("No goals yet.")
    with c2:
        st.markdown("### Top assisters")
        assister_rows = top_list(game.get("top_assisters", {}), 12)
        if assister_rows:
            st.dataframe(assister_rows, hide_index=True, use_container_width=True)
        else:
            st.caption("No assists yet.")



def show_squad_browser(teams: List[dict]) -> None:
    national = [t for t in teams if t.get("players")]
    if not national:
        st.caption("No detailed squads for these teams yet. Custom and club teams use generated depth players around their star player.")
        return
    selected = st.selectbox("View player squad", [t["name"] for t in national])
    team = next(t for t in national if t["name"] == selected)
    st.markdown(f"### {selected} squad core")
    st.caption("Player ratings are editable game estimates used for weighted scorers, assists, match details, lower-noise cards and injury events.")
    st.dataframe(team.get("players", []), hide_index=True, use_container_width=True)


def setup_domestic() -> None:
    st.markdown("## 🏴 Domestic Cups/Leagues")
    competition = st.selectbox("Choose domestic competition", list(DOMESTIC.keys()))
    cfg = DOMESTIC[competition]
    st.caption(cfg.get("format_note", "Domestic competition."))
    preview = get_teams_by_names(cfg["teams"])
    with st.expander("Preview teams, flags, ratings and badge initials", expanded=True):
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
    with st.expander("Preview player cores"):
        show_squad_browser(preview)
    if st.button(f"Create {competition}", type="primary"):
        if competition == "Premier League":
            st.session_state.game = create_premier_league()
        else:
            st.session_state.game = create_fa_cup()
        st.session_state.last_results = []
        st.session_state.show_inline_results = False
        st.success(f"Created {competition}. Use Watch Live or Quick Sim one stage at a time.")
        st.rerun()


def setup_international() -> None:
    st.markdown("## 🌍 World Cup / EURO")
    competition = st.selectbox("Choose international tournament", list(INTERNATIONAL.keys()))
    cfg = INTERNATIONAL[competition]
    st.caption(cfg.get("format_note", "Group stage followed by knockout football."))
    preview = get_teams_by_names(cfg["teams"])
    with st.expander("Preview national teams, ratings and squad sizes", expanded=True):
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
    with st.expander("Preview real-player squad cores"):
        show_squad_browser(preview)
    if st.button("Create international tournament", type="primary"):
        st.session_state.game = create_international_tournament(competition)
        st.session_state.last_results = []
        st.success(f"Created {competition}. Simulate one group matchday at a time.")
        st.rerun()

def setup_real_continental() -> None:
    st.markdown("## 🏆 Real Continental Tournament")
    competition = st.selectbox("Choose competition", list(CONTINENTAL.keys()))
    st.caption("Seeded with 2025/26 league-phase club teams. The game format uses league phase → play-offs → round of 16 → final.")
    preview = get_teams_by_names(CONTINENTAL[competition]["teams"])
    with st.expander("Preview teams and ratings"):
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
    if st.button("Create continental tournament", type="primary"):
        st.session_state.game = create_uefa_tournament(competition)
        st.session_state.last_results = []
        st.success(f"Created {competition}. Simulate one matchday at a time.")
        st.rerun()


def setup_custom() -> None:
    st.markdown("## 🛠️ Create a Custom League/Tournament")
    all_names = sorted(st.session_state.team_db.keys())
    name = st.text_input("Competition name", value="My Custom Football Universe")
    fmt = st.selectbox("Format", ["Standard League", "Straight Knockout", "Cup: Groups + Knockout"])
    selected = st.multiselect("Select real or custom teams", all_names, default=all_names[:8])

    st.markdown("### Add a custom team")
    with st.form("custom_team_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            team_name = st.text_input("Team name")
            country = st.text_input("Country", value="Custom")
            league = st.text_input("League", value="Custom League")
            star = st.text_input("Star player", value="Generated Hero")
        with c2:
            attack = st.slider("Attack", 50, 99, 75)
            midfield = st.slider("Midfield", 50, 99, 75)
            defence = st.slider("Defence", 50, 99, 75)
        submitted = st.form_submit_button("Add custom team")
        if submitted and team_name:
            overall = round((attack * .34) + (midfield * .33) + (defence * .33))
            st.session_state.team_db[team_name] = {
                "id": team_name.lower().replace(" ", "-"),
                "name": team_name,
                "country": country,
                "league": league,
                "attack": attack,
                "midfield": midfield,
                "defence": defence,
                "overall": overall,
                "star_player": star,
            }
            st.success(f"Added {team_name}. Select it from the team list above.")

    teams = get_teams_by_names(selected)
    if selected:
        with st.expander(f"Selected teams ({len(teams)})", expanded=False):
            st.dataframe(teams_table_rows(teams), hide_index=True, use_container_width=True)

    min_teams = 2 if fmt == "Straight Knockout" else 3
    if fmt == "Cup: Groups + Knockout":
        groups = st.slider("Number of groups", 2, 8, 4)
    else:
        groups = 0
    double_round = st.checkbox("Double round-robin", value=False, disabled=(fmt != "Standard League"))

    if st.button("Create custom competition", type="primary"):
        if len(teams) < min_teams:
            st.error(f"Pick at least {min_teams} teams.")
        elif fmt == "Straight Knockout" and len(teams) & (len(teams) - 1) != 0:
            st.error("Straight knockout works best with 2, 4, 8, 16 or 32 teams.")
        elif fmt == "Cup: Groups + Knockout" and len(teams) < groups * 2:
            st.error("Use at least two teams per group.")
        else:
            if fmt == "Standard League":
                game = create_league(name, teams, double_round=double_round)
            elif fmt == "Straight Knockout":
                game = create_knockout(name, teams)
            else:
                game = create_cup(name, teams, groups=groups)
            st.session_state.game = game
            st.session_state.last_results = []
            st.success(f"Created {name}.")
            st.rerun()


def quick_match() -> None:
    st.markdown("## ⚡ Quick Match")
    names = sorted(st.session_state.team_db.keys())
    c1, c2 = st.columns(2)
    with c1:
        home = st.selectbox("Home team", names, index=names.index("Arsenal") if "Arsenal" in names else 0)
    with c2:
        away_default = names.index("Real Madrid") if "Real Madrid" in names else min(1, len(names) - 1)
        away = st.selectbox("Away team", names, index=away_default)
    knockout = st.checkbox("Use knockout rules: extra time and penalties if level", value=False)
    c1, c2 = st.columns(2)
    with c1:
        quick_clicked = st.button("⚡ Simulate quick match", type="primary")
    with c2:
        live_clicked = st.button("🎬 Watch quick match live")
    if quick_clicked or live_clicked:
        if home == away:
            st.error("Pick two different teams.")
        else:
            result = simulate_match(st.session_state.team_db[home], st.session_state.team_db[away], knockout=knockout)
            st.session_state.quick_match_result = result
            if live_clicked:
                live_broadcast([result], seconds=60)
    if st.session_state.quick_match_result:
        show_results([st.session_state.quick_match_result])
        if st.session_state.quick_match_result.get("winner"):
            winner_graphic(st.session_state.quick_match_result.get("winner"), "Quick Match")


def setup_screen() -> None:
    hero()
    instructions_panel()
    st.markdown("## Choose your starting mode")
    render_html(
        """
        <div class="mode-grid">
            <div class="mode-card"><h3>🏴 Domestic Cups/Leagues</h3><p>Premier League season or FA Cup knockout with flags, generated crest badges and player cores.</p></div>
            <div class="mode-card"><h3>🌍 World Cup / EURO</h3><p>International tournaments with national team ratings and real-player squad cores.</p></div>
            <div class="mode-card"><h3>🏆 Real Continental</h3><p>Champions League, Europa League or Conference League.</p></div>
            <div class="mode-card"><h3>🛠️ Custom Competition</h3><p>Create leagues, cups and knockout brackets with real, national or fictional teams.</p></div>
            <div class="mode-card"><h3>⚡ Quick Match</h3><p>Pick any two teams for an instant or live 60-second simulation.</p></div>
        </div>
        """
    )
    mode = st.radio(
        "Start mode",
        ["🏴 Domestic Cups/Leagues", "🌍 World Cup / EURO", "🏆 Real Continental Tournament", "🛠️ Custom League/Tournament", "⚡ Quick Match"],
        key="start_mode",
        label_visibility="collapsed",
    )
    if mode.startswith("🏴"):
        setup_domestic()
    elif mode.startswith("🌍"):
        setup_international()
    elif mode.startswith("🏆"):
        setup_real_continental()
    elif mode.startswith("🛠️"):
        setup_custom()
    else:
        quick_match()


def play_screen(game: dict) -> None:
    hero()
    st.markdown(f"## {game['name']}")
    if game.get("config", {}).get("format_note"):
        st.caption(game["config"]["format_note"])
    status = game["stage"].replace("_", " ").title()
    m_remaining = len(upcoming_matches(game))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stage", status)
    c2.metric("Teams", len(game["teams"]))
    c3.metric("Next fixtures", m_remaining)
    c4.metric("Champion", game.get("champion") or "TBD")

    next_action_panel(game)
    active_watch_teams: List[str] = []

    if game["stage"] == "league":
        st.markdown(f"### Upcoming Matchday {game['matchday_index'] + 1}")
        fixtures = upcoming_matches(game)
        watch_teams = watch_selector_panel(fixtures, key_prefix="league")
        active_watch_teams = watch_teams
        fixture_cards(fixtures, title="#### Full matchday fixtures")
        action_buttons(game, key_prefix="top_next_matchday", watch_teams=watch_teams)
        st.caption("Watch Live focuses on your selected teams for about 60 seconds. Quick Sim instantly simulates the full matchday. Neither option runs ahead without another tap.")
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))

    elif game["stage"] == "knockout":
        current = game["knockout_rounds"][-1]
        st.markdown(f"### Upcoming {current['name']}")
        fixtures = upcoming_matches(game)
        watch_teams = watch_selector_panel(fixtures, key_prefix="knockout")
        active_watch_teams = watch_teams
        fixture_cards(fixtures, title="#### Full round fixtures")
        action_buttons(game, key_prefix="top_next_knockout", watch_teams=watch_teams)
        st.caption("Watch Live focuses on your selected teams dramatically. Quick Sim is instant. The app pauses again before the next round.")
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))

    elif game["stage"] == "complete":
        winner_graphic(game.get("champion"), game["name"])
        if st.button("Start a new game"):
            st.session_state.game = None
            st.session_state.last_results = []
            st.rerun()

    st.markdown("---")
    tab_results, tab_table, tab_bracket, tab_stats, tab_teams, tab_save, tab_help = st.tabs(
        ["Results", "Tables", "Bracket", "Stats", "Teams", "Save", "Help"]
    )
    with tab_results:
        st.markdown("### Latest results")
        show_results(st.session_state.last_results or game.get("history", [])[-12:], focus_teams=st.session_state.get("last_watch_teams", []))
        if game.get("stage") in ("league", "knockout"):
            st.markdown("### Continue")
            st.caption("You can continue from here on mobile, so you do not need to scroll back to the top.")
            action_buttons(game, key_prefix="results_continue", watch_teams=active_watch_teams)
    with tab_table:
        show_tables(game)
    with tab_bracket:
        show_bracket(game)
    with tab_stats:
        show_stats(game)
    with tab_teams:
        st.dataframe(teams_table_rows(game["teams"]), hide_index=True, use_container_width=True)
        show_squad_browser(game["teams"])
    with tab_save:
        save_text = dumps_state(game)
        st.download_button("Download save file", save_text, file_name="football_simulator_save.json", mime="application/json")
        uploaded = st.file_uploader("Load save file", type=["json"])
        if uploaded is not None:
            try:
                st.session_state.game = loads_state(uploaded.read().decode("utf-8"))
                st.session_state.last_results = []
                st.success("Save loaded. Use the buttons above to continue.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not load save: {exc}")
    with tab_help:
        instructions_panel(compact=True)
        st.markdown(
            """
            **Game rules**

            - League/group stage: 3 points for a win, 1 for a draw.
            - Knockout games: draws go to extra time and then penalties.
            - Match results are weighted by Attack, Midfield, Defence, Overall, player ratings, squad profile and home advantage.
            - Match details include possession, shots, shots on target, big chances, corners, fouls, pass accuracy and saves.
            - Yellow cards are lower-noise now, so the timeline is driven more by football actions than discipline.
            - National-team scorers and assisters are chosen from real-player squad cores using position/rating weights.
            - You control the pace. The app pauses after every matchday or knockout round.
            - The domestic modes add Premier League and FA Cup, with generated shield badges instead of official crests.
            - Watch Live mode takes about 60 seconds and reveals events one at a time.
            """
        )

    if game.get("stage") in ("league", "knockout"):
        st.markdown("---")
        action_buttons(game, key_prefix="bottom_menu", sticky=True, watch_teams=active_watch_teams)
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))


def sidebar() -> None:
    st.sidebar.title("⚽ Simulator Control")
    st.sidebar.caption("Designed for mobile: keep this closed unless you need admin controls.")
    if st.sidebar.button("Reset active game"):
        st.session_state.game = None
        st.session_state.last_results = []
        st.session_state.quick_match_result = None
        st.rerun()
    st.sidebar.markdown("---")
    with st.sidebar.expander("How to play", expanded=False):
        st.write("1. Pick a mode.")
        st.write("2. Simulate one matchday or round.")
        st.write("3. Check results, tables, bracket and stats.")
        st.write("4. Download a save file anytime.")
    st.sidebar.markdown("### Team database")
    countries = sorted({t["country"] for t in st.session_state.team_db.values()})
    country = st.sidebar.selectbox("Filter by country", ["All"] + countries)
    teams = list(st.session_state.team_db.values())
    if country != "All":
        teams = [t for t in teams if t["country"] == country]
    st.sidebar.caption(f"{len(teams)} teams available")
    st.sidebar.dataframe(teams_table_rows(teams[:10]), hide_index=True, use_container_width=True)


def main() -> None:
    init()
    sidebar()
    if st.session_state.game is None:
        setup_screen()
    else:
        play_screen(st.session_state.game)


if __name__ == "__main__":
    main()
