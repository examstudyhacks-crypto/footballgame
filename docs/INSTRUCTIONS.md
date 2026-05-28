# Football Simulator Pro — Player Instructions

## Starting the game

Open the app and choose one of the four starting modes:

1. **World Cup / EURO**
   - Choose World Cup 2026-style or EURO / European Championship.
   - These use national teams with real-player squad cores and stat-weighted player events.
   - World Cup mode uses 48 teams, 12 groups, top two plus eight best third-placed teams.
   - EURO mode uses 24 teams, six groups, top two plus four best third-placed teams.

2. **Real Continental Tournament**
   - Choose Champions League, Europa League or Conference League.
   - The tournament starts with a league phase and progresses into knockout rounds.

3. **Custom League/Tournament**
   - Choose the competition name.
   - Select the format: Standard League, Straight Knockout, or Cup with Groups + Knockout.
   - Pick real clubs, national teams, add custom teams, or mix them all.

4. **Quick Match**
   - Pick any two teams.
   - Toggle knockout rules if you want extra time and penalties.

## Playing a tournament

The simulator never runs ahead automatically.

- In a league or group stage, press **Quick Simulate Matchday**.
- In a knockout stage, press **Simulate Knockout Round**.
- After each command, review the results, table, bracket and player stats.

## How winners and scores are calculated

Matches use a random-chance engine weighted by:

- Team Attack, Midfield and Defence
- Team Overall
- Home advantage or neutral-final setting
- Player position and rating for goalscorers/assisters
- Defensive/contact positions for cards and injuries

This means stronger sides usually win more often, but upsets, low blocks, penalties and chaotic cup games can still happen.

## Match details

Every simulated match can include:

- Scoreline
- xG
- Goalscorers
- Assisters
- Goal minutes
- Yellow cards
- Red cards
- Injuries
- Extra time
- Penalties

Open **View match details** under any result to see the event timeline.

## Tables and brackets

- League/group tables track played, wins, draws, losses, goals for, goals against, goal difference and points.
- World Cup/EURO modes track best third-placed qualifiers after the group stage.
- Knockout brackets update after each completed round.
- Top scorers and top assisters update across the active competition.

## Viewing real players

Open the **Teams** tab and use **View player squad** to see a national team's squad core.

Each player has:

- Name
- Position
- Rating estimate

These ratings are editable game estimates used by the simulation engine.

## Winner screen

When a final or league is complete, the app shows a trophy winner graphic with animated confetti. You can then save the game universe or start again.

## Save and load

Use the **Save** tab to download the active tournament as JSON. Upload the same JSON later to continue.

## Mobile controls

The app is designed for phones first:

- The sidebar starts collapsed.
- Main actions are large full-width buttons.
- Fixture cards are stacked for narrow screens.
- Tabs scroll horizontally on small displays.


## Detailed match stats

Each match now creates a fuller football box score: possession, shots, shots on target, big chances, corners, fouls, pass accuracy and keeper saves. Cards are lower-noise so the timeline is driven more by football actions than constant yellow-card spam.


## Mobile flow

1. Create or load a tournament.
2. Read the **WHAT TO CLICK NEXT** card.
3. Press the green **▶ Simulate matchday** or **▶ Simulate round** button.
4. On the Results tab, read the score cards and open **View match details** for full stats and timeline.
5. Use the **Continue** button at the bottom of the Results tab to keep playing without scrolling back to the top.

## Domestic modes

The **Domestic Cups/Leagues** start option now includes:

- **Premier League** — 20 clubs, 38 matchdays, full home-and-away season.
- **FA Cup** — 64-team random knockout draw with extra time and penalties.

The app uses small emoji flags and generated shield-style badge initials. It does **not** use official club crests.

## Watch Live mode

During any active tournament you now get three clear mobile actions:

- **🎬 Watch Live** — reveals the next matchday or round event-by-event over about 60 seconds.
- **⚡ Quick Sim** — instantly simulates the next matchday or round.
- **📋 Show Results** — opens the latest result cards without hunting through the page.

A bottom action menu repeats these controls so mobile users do not need to scroll back to the top.

## Late drama and upsets

The match engine now uses a stronger team-weight model, so better teams are still more likely to win. It also adds controlled late-drama logic:

- underdog late equalizers;
- stoppage-time winners;
- cup giant-killing chances;
- favourite pressure when chasing a game.

This should make FA Cup and knockout games more exciting without turning the results into pure randomness.

## Mobile Watch Mode

Before simulating a matchday or knockout round, use **Pick 1, 2 or 3 teams to watch live**.

- **Watch selected** follows those teams in a 60-second live feed.
- The match clock moves from kick-off to full-time.
- The current event appears in a large live panel.
- The selected teams' results appear first after the live feed.
- The rest of the matchday is still simulated and shown underneath.

Use **Quick Sim** when you want the whole matchday instantly.
