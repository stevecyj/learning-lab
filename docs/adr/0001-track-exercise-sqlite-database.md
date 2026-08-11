---
status: superseded by ADR-0002
---

# Track the exercise SQLite database

The `ex-IMP-part2.ipynb` exercise tracks its mutable
`game_reservations.db` file in Git so the learner can carry the persisted
reservation state between computers. This deliberately accepts binary diffs
and non-mergeable conflicts: only one computer should update the database at a
time, changes must be committed and pushed before switching computers, and the
other computer must pull before running the exercise.
