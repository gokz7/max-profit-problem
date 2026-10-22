"""
=====================================================================
 MAX PROFIT PROBLEM  -  Ever Quint Interview Assignment (Task 2)
=====================================================================

THE PROBLEM (in simple words)
-----------------------------
Mr. X has a timer of n time units. He can build shops, ONE AT A TIME:

    Shop                 Build time   Earns per time unit (after it's built)
    Theatre (T)          5            $1500
    Pub (P)              4            $1000
    Commercial Park (C)  10           $2000

A shop earns money every time unit from the moment it is finished until
the timer ends. We must find the shop mix that earns the MOST money.
If two or more mixes tie, we show ALL of them.

EXAMPLE: n = 13
---------------
    Build Theatre 1 -> ready at time 5  -> earns (13 - 5)  x 1500 = $12000
    Build Theatre 2 -> ready at time 10 -> earns (13 - 10) x 1500 = $4500
                                                      Total = $16500
    Answer: T: 2 P: 0 C: 0

HOW WE SOLVE IT (Dynamic Programming)
-------------------------------------
We ask one question for every amount of time t, from 0 up to n:
    "With t time units left, what's the most money I can make?"

To answer it, we try building each shop FIRST:
    money = (rate of that shop) x (time left after it's built)
          + (best money we can make with that leftover time)

The "best money with leftover time" is a smaller question we have
ALREADY answered (because we go from small t to big t). So we just
look it up in our table - no repeated work.

ASSUMPTIONS (the PDF does not say these, so we decide them)
-----------------------------------------------------------
1. Earnings are PER TIME UNIT (needed to match the PDF's test cases).
2. A shop that finishes exactly at time n earns $0, so we don't build it.
3. Land size, auditoriums, spaces, dance floors do NOT affect the answer.
4. If no shop can earn money (n <= 4), answer is $0 with T: 0 P: 0 C: 0.
5. Tied solutions are listed with the most Theatres first.

HOW TO RUN
----------
    python max_profit.py 13
"""

# Lets us write type hints like "list[int]" on older Python versions too
from __future__ import annotations

import argparse                    # reads the number typed in the terminal
import sys                         # used to exit the program cleanly
from dataclasses import dataclass  # quick way to make a simple data class


# ---------------------------------------------------------------------
# A "Mix" is how many of each shop we build, always in this order:
#     (number of Theatres, number of Pubs, number of Commercial Parks)
# Example: (2, 0, 0) means 2 Theatres, 0 Pubs, 0 Commercial Parks.
# ---------------------------------------------------------------------
Mix = tuple[int, int, int]


# ---------------------------------------------------------------------
# A Building holds the 4 facts we need about each shop type.
# frozen=True means these values can't be changed by mistake later.
# ---------------------------------------------------------------------
@dataclass(frozen=True)
class Building:
    code: str        # the letter shown in the output: "T", "P" or "C"
    name: str        # full name, for readability
    build_time: int  # how many time units it takes to build
    rate: int        # dollars it earns per time unit once open


# The 3 shop types from the PDF.
# IMPORTANT: this order (T, P, C) must match the order inside a Mix.
BUILDINGS: tuple[Building, ...] = (
    Building("T", "Theatre", 5, 1500),
    Building("P", "Pub", 4, 1000),
    Building("C", "Commercial Park", 10, 2000),
)


def solve(n: int) -> tuple[int, list[Mix]]:
    """
    Find the maximum earnings for n time units, and every shop mix
    that reaches it.

    Returns: (max_earnings, list_of_mixes)
    Example: solve(7) -> (3000, [(1, 0, 0), (0, 1, 0)])
    """

    # --- Step A: check the input is valid --------------------------
    # (True/False are technically ints in Python, so we block them too)
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be 0 or more")

    # --- Step B: create two empty tables, one slot for each t ------
    # best_value[t] = most money possible with t time units left
    # best_mixes[t] = all shop mixes that earn best_value[t]
    best_value: list[int] = [0] * (n + 1)
    best_mixes: list[set[Mix]] = [set() for _ in range(n + 1)]

    # --- Step C: fill the tables from t = 0 up to t = n ------------
    for t in range(n + 1):

        # Start by assuming we build nothing: $0, mix (0, 0, 0)
        value = 0
        mixes: set[Mix] = {(0, 0, 0)}

        # Try building each shop FIRST, one by one
        for index, building in enumerate(BUILDINGS):

            # Time left on the clock after this shop is finished
            time_left = t - building.build_time

            # If it finishes at or after t, it earns $0 - skip it.
            # (Example: a Pub with t = 4 finishes exactly at 4, earns $0)
            if time_left <= 0:
                continue

            # Money = this shop's earnings
            #       + best money from the time that is left
            # (best_value[time_left] is already filled, since time_left < t)
            candidate = building.rate * time_left + best_value[time_left]

            # Found a NEW best total? Throw away the older, worse mixes.
            if candidate > value:
                value = candidate
                mixes = set()

            # This choice equals the best total -> keep its mixes.
            # We take each best mix for the leftover time and add
            # 1 of the current shop to it.
            if candidate == value:
                for mix in best_mixes[time_left]:
                    new_mix = list(mix)
                    new_mix[index] += 1   # add one of this shop
                    mixes.add((new_mix[0], new_mix[1], new_mix[2]))

        # Save the answer for this t, so bigger t values can use it
        best_value[t] = value
        best_mixes[t] = mixes

    # --- Step D: sort the mixes: most Theatres, then Pubs, then C ---
    # (the minus signs mean "biggest first")
    sorted_mixes = sorted(best_mixes[n], key=lambda m: (-m[0], -m[1], -m[2]))
    return best_value[n], sorted_mixes


def format_result(n: int, earnings: int, mixes: list[Mix]) -> str:
    """
    Turn the answer into text in the same layout as the PDF.

    Example output for n = 7:
        Time Unit: 7
        Earnings: $3000
        Solutions
        1. T: 1 P: 0 C: 0
        2. T: 0 P: 1 C: 0
    """
    lines = [
        f"Time Unit: {n}",
        f"Earnings: ${earnings}",
        "Solutions",
    ]
    # Number each solution 1, 2, 3...
    for number, (t_count, p_count, c_count) in enumerate(mixes, start=1):
        lines.append(f"{number}. T: {t_count} P: {p_count} C: {c_count}")
    return "\n".join(lines)


def _non_negative_int(text: str) -> int:
    """
    Check what the user typed in the terminal.
    Accepts only whole numbers 0 or more. Otherwise shows a clear error
    instead of crashing.
    Examples: "13" -> 13 (ok), "-5" -> error, "abc" -> error
    """
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{text}' is not a whole number"
        ) from None
    if value < 0:
        raise argparse.ArgumentTypeError("time units must be 0 or more")
    return value


def main(argv: list[str] | None = None) -> int:
    """
    Command-line entry point.
    Reads n from the terminal, solves, and prints the answer.
    (argv lets the tests pass fake input; normally it's None)
    """
    parser = argparse.ArgumentParser(
        description="Find the building mix that earns the most money in n time units."
    )
    parser.add_argument(
        "n",
        type=_non_negative_int,
        help="total time units available (whole number, 0 or more)",
    )
    args = parser.parse_args(argv)

    earnings, mixes = solve(args.n)
    print(format_result(args.n, earnings, mixes))
    return 0  # 0 means "finished with no errors"


# This runs only when you start the file directly:
#     python max_profit.py 13
# It does NOT run when another file (like the tests) imports this one.
if __name__ == "__main__":
    sys.exit(main())