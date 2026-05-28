# Mobile Watch Mode UX Fix Report

## Requested changes

- Make the app easier to follow on mobile.
- Let the user pick 1, 2 or 3 teams to watch.
- Show results more clearly under team/result cards.
- Add more spacing so team names can be read.
- Add visible timer movement during Watch Live mode.

## Changes made

### 1. Team-focused Watch Live selector

Added a mobile-first selector above every upcoming matchday/round:

- **Pick 1, 2 or 3 teams to watch live**
- The live broadcast focuses only on games involving those teams.
- The rest of the matchday is still simulated quietly.
- After the live feed, watched games are shown first, then the rest of the results.

### 2. Readable fixture cards

The old compact horizontal fixture cards were too hard to read on mobile. They now use:

- One card per fixture.
- Separate Home and Away rows.
- Larger generated badge/crest.
- Full team names instead of truncated names.
- More padding and spacing.

### 3. Clearer result cards

Result cards now use a large stacked score layout:

- Home team block.
- Big centre score.
- Away team block.
- Watched games get a visible **Watched game** badge.
- Match stats remain underneath.

### 4. Moving match clock

Watch Live mode now updates a single live stage instead of dumping lots of tiny cards down the page. It includes:

- Current minute.
- Animated progress bar from kick-off to full-time.
- Big current event text.
- Live scores for the watched games.
- Latest movement log.

### 5. Mobile layout fixes

- Fixture cards switch to one column on mobile.
- Result cards stack vertically on mobile.
- Score tiles stack vertically on mobile.
- Team names wrap instead of being cut off.
- Bottom action menu still works with the selected watch teams.

## Test result

`python tools/fidelity_check.py`

Result: **FULL FIDELITY CHECK PASSED**
