---
status: accepted
---

# Do not track the runtime SQLite database

The `ex-IMP-part2.ipynb` exercise generates `game_reservations.db` locally and
does not track it in Git. Git carries the notebook, schema, and seed logic
between computers, while each computer keeps independent runtime reservation
state; this avoids binary diffs and unmergeable database conflicts.
