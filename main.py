#!/usr/bin/env python3
"""One Letter for Your Day -- pick the strongest single letter.

The entry is exactly one letter, A-Z, standing for the word that describes
the day. The judge reads two letters at a time and picks the one whose word
behind it feels more vivid, funnier or truer, weighing, most important first:

  1. the letter is the first letter of a word that describes the day
     (every candidate here passes: each letter is the initial of its word)
  2. vivid and specific -- a sharp picture of the day, not a vague mood
  3. funny or surprising -- lands at once, the kind you repeat to a friend
  4. true to a real day -- an honest report, ordinary or strange
  5. the letter suits its word -- an initial that fits the sound and shape

Each candidate is scored 1-5 on criteria 2-5. A pairwise game goes through
the criteria in order: the first criterion where the two differ decides,
unless a later criterion differs by 3 or more, which then decides instead
(a much bigger gap later outweighs a small gap earlier). Every candidate
plays every other; the champion is the one with the most pairwise wins,
tie-broken by total score, then by earliest in the list. Deterministic,
no network, no arguments. Writes the winning letter to /output/entry.txt.
"""

import os

# letter, word behind it, scores (vivid, funny, true, fit) each 1-5.
CANDIDATES = [
    # Z: a night with literally zero sleep. Hyperbolic "zero" lands at
    # once, everyone has lived it, and Z is the sharp initial of "zero".
    ("Z", "zero sleep", (5, 4, 5, 5)),
    # S: clothes dripping, hair plastered down. Sharp picture, but the
    # joke is thinner than Z's and it needs rain to be true.
    ("S", "soaked", (5, 3, 4, 5)),
    # D: soaked through to the skin. Vivid, but narrower and less funny.
    ("D", "drenched", (5, 3, 3, 5)),
    # K: everything is broken, done, finished. A punchline word, but a
    # loanword whose picture is vaguer than a wet shirt or a sleepless night.
    ("K", "kaput", (4, 5, 3, 4)),
    # H: the morning after, light hurts, head pounds. Funny and true, but
    # the picture is a common hangover, less sharp than zero sleep.
    ("H", "hungover", (4, 4, 3, 5)),
    # M: the day itself is the dread. Universally true, but a calendar
    # label, not a picture of what the day looked like.
    ("M", "Monday", (3, 3, 5, 5)),
    # J: traffic, printer, plans -- everything stuck. Vivid, but the word
    # splits across too many pictures to land as one.
    ("J", "jammed", (4, 3, 4, 4)),
    # W: wiped out, nothing left in the tank. Honest, but a tired cliche.
    ("W", "wiped-out", (4, 3, 4, 4)),
    # Q: one snaking line, hours standing still. A sharp picture, but only
    # true on days with a queue, and more weary than funny.
    ("Q", "queue", (4, 3, 3, 5)),
    # P: rain hammering down. Vivid weather, weak joke, needs a storm.
    ("P", "pouring", (4, 2, 3, 5)),
    # B: running on fumes. True, but a vague mood word, not a picture.
    ("B", "burnt-out", (3, 2, 4, 4)),
    # C: everything at once, nothing clear. A vague mood, not a day.
    ("C", "chaotic", (2, 2, 4, 4)),
]

CRITERIA = ("vivid", "funny", "true", "fit")


def pairwise_winner(a, b):
    """Return the winner of one game between candidates a and b.

    Walk the criteria in order; the first differing criterion decides,
    unless a later criterion differs by 3+ in the other direction.
    """
    diffs = [x - y for x, y in zip(a[2], b[2])]
    first = next((i for i, d in enumerate(diffs) if d != 0), None)
    if first is None:
        return None  # exact tie on every criterion (does not happen here)
    # A later criterion only overrules the first differing one when it
    # disagrees by 3+; if several later criteria do, the biggest gap
    # wins the argument, not whichever happens to come first.
    override = None
    for j in range(first + 1, len(diffs)):
        if diffs[j] != 0 and abs(diffs[j]) >= 3 and (
            diffs[j] > 0
        ) != (diffs[first] > 0):
            if override is None or abs(diffs[j]) > abs(diffs[override]):
                override = j
    if override is not None:
        return a if diffs[override] > 0 else b
    return a if diffs[first] > 0 else b


def pick_winner(candidates):
    """Round-robin tournament; most pairwise wins takes it."""
    wins = {c[0]: 0.0 for c in candidates}
    for i, a in enumerate(candidates):
        for b in candidates[i + 1:]:
            w = pairwise_winner(a, b)
            if w is not None:
                wins[w[0]] += 1
            else:
                # Exact tie on every criterion: split the point so the
                # game still counts instead of vanishing from the table.
                wins[a[0]] += 0.5
                wins[b[0]] += 0.5
    totals = {c[0]: sum(c[2]) for c in candidates}
    order = {c[0]: i for i, c in enumerate(candidates)}
    # Most wins, then highest total score, then earliest listed.
    ranked = sorted(
        candidates,
        key=lambda c: (-wins[c[0]], -totals[c[0]], order[c[0]]),
    )
    return ranked[0], wins, totals


def main():
    winner, wins, totals = pick_winner(CANDIDATES)
    letter = winner[0]
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(letter)


if __name__ == "__main__":
    main()
