# Football Simulator Pro - Single File Streamlit Build

This deployment build is flattened into one `app.py` so Streamlit Cloud cannot fail with `ModuleNotFoundError: football_sim`.

Upload the contents of this zip directly to the GitHub repo root and set Streamlit main file to `app.py`.

# Football Simulator Pro — Streamlit Game

A polished, mobile-first text-based football simulator and tournament generator built for Streamlit.

## Streamlit Cloud deployment note

This is the cloud-safe build. It intentionally has **no `requirements.txt`** and no direct `pandas`/`numpy` imports. The app uses only Streamlit, Python built-ins and local project files, so Streamlit Community Cloud has nothing extra to install.

If you are replacing an older repo, delete the old `requirements.txt`, `uv.lock`, `Pipfile`, `environment.yml`, or `pyproject.toml` before redeploying. If Streamlit asks for a Python version, choose Python 3.12 or 3.11.


## Features

- **5 starting modes**
  1. Domestic Cups/Leagues: Premier League season or FA Cup knockout
  2. World Cup / EURO: international tournaments with national team ratings and real-player squad cores
  3. Real Continental Tournament: Champions League, Europa League, Conference League
  4. Custom League/Tournament: league, straight knockout, or groups + knockout
  5. Quick Match: pick any two club or national teams
- **Premier League mode**: 20 clubs, 38 matchdays, full home-and-away season
- **FA Cup mode**: 64-team random knockout draw with extra time, penalties and giant-killing chances
- **World Cup 2026-style mode**: 48 teams, 12 groups of four, top two plus eight best third-placed teams qualify for the Round of 32
- **EURO / European Championship mode**: 24 teams, six groups of four, top two plus four best third-placed teams qualify for the Round of 16
- **Real-player squad cores** for national teams and Premier League/selected FA Cup clubs, with editable player positions and rating estimates
- **Custom team creation** with Attack, Midfield, Defence and Star Player
- **Seeded real club database** from England, Spain, Italy, Germany, France, Portugal, USA, Saudi Arabia, Brazil and 2025/26 UEFA competitions
- **Stat-weighted match simulation** using Attack, Midfield, Defence, Overall, player positions, player ratings, star power, squad depth and home/neutral advantage
- **Realistic events**: goals, assists, minutes, yellow/red cards, injuries, xG, extra time and penalties
- **Mobile-first interface** with stacked fixture cards, generated shield badges, small flags, large buttons, collapsed sidebar and responsive spacing
- **Built-in player instructions** on the setup screen, Help tab and sidebar
- **Watch Live mode**: reveals match events one at a time for about 60 seconds before showing results
- **Winner trophy graphic** with animated CSS confetti when a champion is crowned
- **Persistent active tournament state** using Streamlit session state
- **Save/load** active games as JSON
- **League tables, group tables, best third-place qualifiers, brackets, top scorers and top assisters**

## File structure

```text
football-simulator-pro/
├── app.py
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   └── winner-trophy.svg
├── docs/
│   ├── INSTRUCTIONS.md
│   └── MOBILE_UX_NOTES.md
└── football_sim/
    ├── __init__.py
    ├── data.py
    ├── simulator.py
    └── tournaments.py
```

## How to play

1. Open the app.
2. Choose a starting mode: Domestic Cups/Leagues, World Cup / EURO, Real Continental Tournament, Custom League/Tournament, or Quick Match.
3. Press **Watch Live** for the 60-second event reveal or **Quick Sim** for instant results. The game never auto-simulates ahead.
4. Review Results, Tables, Bracket, Stats and Teams after each matchday or knockout round.
5. In international modes, open the Teams tab to view the real-player squad cores and player rating estimates.
6. When the tournament finishes, the champion screen shows a trophy graphic and animated confetti.
7. Use the Save tab to download or reload an active universe.

See `docs/INSTRUCTIONS.md` for the full player guide.

## Mobile-first UX

The app is designed to work well on phones:

- Sidebar starts collapsed.
- Important actions are full-width buttons, with a bottom action menu during active tournaments.
- Fixtures are shown as cards before dense tables.
- Tabs stay short and scroll cleanly on narrow screens.
- The winner screen and generated badge shields use CSS/HTML, so no paid image API or licensed club crests are required.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install streamlit
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload all files from this folder.
3. Go to Streamlit Community Cloud.
4. Select the repo.
5. Set the main file path to:

```text
app.py
```

6. Deploy.

Important: do not upload an old `requirements.txt` from a previous version. This build is designed to run without one.

## Editing team and player ratings

Open `football_sim/data.py`.

Club/custom-style teams use the `RATINGS` dictionary:

```python
"Team Name": {
    "country": "England",
    "league": "Premier League",
    "attack": 90,
    "midfield": 88,
    "defence": 86,
    "star_player": "Star Name",
}
```

Domestic modes use:

- `PREMIER_LEAGUE_2025_26` for the Premier League club list
- `FA_CUP_SEED_TEAMS` for the 64-team FA Cup seed pool
- `CLUB_SQUADS` for Premier League and selected FA Cup player cores
- `DOMESTIC` for domestic competition configuration

National teams use:

- `NATIONAL_RATINGS` for team Attack, Midfield and Defence
- `NATIONAL_SQUADS` for real-player squad cores and player ratings
- `WORLD_CUP_2026_TEAMS` and `EURO_2024_TEAMS` for tournament pools
- `INTERNATIONAL` for group/qualification rules

The app calculates overall automatically.

## Notes

- Ratings are game-balanced estimates, not official rankings or official player-rating data.
- National team squads are representative real-player cores and are easy to edit as final squads change.
- The World Cup mode uses the 48-team modern format but randomises the group draw each time for replayability.
- The UEFA club competitions are seeded from 2025/26 league-phase team lists.
- The UEFA club format is implemented as league phase → knockout play-offs → round of 16 → quarter-finals → semi-finals → final.
- No paid API is required.


## Detailed match stats

Each match now creates a fuller football box score: possession, shots, shots on target, big chances, corners, fouls, pass accuracy and keeper saves. Cards are lower-noise so the timeline is driven more by football actions than constant yellow-card spam.


## Latest mobile UX fixes

This build includes the mobile results fix:

- score cards render cleanly without raw HTML blocks;
- match stats display as compact mobile cards;
- a clear **WHAT TO CLICK NEXT** panel appears during tournaments;
- the Results tab includes a **Continue** button so phone users do not have to scroll back to the top;
- result cards include short football-style match summaries.

Run the built-in check with:

```bash
python tools/fidelity_check.py
```


## V3 domestic and live upgrade

This version adds Premier League, FA Cup, generated team badges, emoji flags, a stronger weighted match engine, late-drama goals, Watch Live mode and mobile contrast fixes for buttons/dropdowns. See `V3_DOMESTIC_LIVE_UPGRADE_REPORT.md`.
