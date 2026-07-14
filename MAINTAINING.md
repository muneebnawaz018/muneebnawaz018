# Maintaining this profile

This repo is self-contained. Everything that renders on the profile lives here,
and the moving parts refresh themselves on a schedule. Manual commands are below
if you want to update something right now.

## What updates on its own

| Part | How it stays fresh | Schedule |
| :--- | :--- | :--- |
| Contribution snake | `.github/workflows/snake.yml` regenerates the SVGs into the `output` branch | Daily + on every push to `main` |
| Years of experience, repo count | `.github/workflows/update-stats.yml` runs `scripts/update-stats.mjs` | Monthly |

Both also have a **Run workflow** button under the repo's **Actions** tab
(`workflow_dispatch`).

## Update the snake now

```bash
gh workflow run "Generate contribution snake"
```

The snake counts private contributions too, as long as
**Settings → Profile → Include private contributions on my profile** is on.
Regenerate after toggling it so the change shows up.

## Update the stats now (years of experience, repo count)

```bash
node scripts/update-stats.mjs   # rewrites the neofetch lines in README.md
git add README.md && git commit -m "chore: refresh README stats" && git push
```

- Years of experience is computed as `current year - 2020`.
- Repo count is pulled live from the GitHub API.

## Regenerate the "How I ship" diagram

```bash
python3 scripts/gen-ship-diagram.py   # writes assets/how-i-ship-{dark,light}.svg
git add assets/ && git commit -m "chore: regenerate ship diagram" && git push
```

Edit the node list, colours, or animation timing at the top of
`scripts/gen-ship-diagram.py`, then rerun.
