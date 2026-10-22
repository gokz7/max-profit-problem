"""
MAX PROFIT PROBLEM - Ever Quint Task 2

THE PROBLEM
Mr. X builds shops one at a time: Theatre (T), Pub (P), Commercial Park (C).
A shop earns money every time unit after it is built, until time n ends.
Goal: find the shop mix that earns the most money in n time units.

    Shop   Build time   Money per time unit
    T      5            $1500
    P      4            $1000
    C      10           $2000

THE IDEA
For every time t from 0 up to n, we find: "best money with t time units".
For each t, we try building each shop FIRST:
    money = shop's rate x (time left after it's built)
          + best money for that leftover time (already worked out earlier)
We keep the highest money, and every mix that ties for it.

EXAMPLE (n = 13)
    Theatre 1 ready at 5  -> earns 8 x 1500 = $12000
    Theatre 2 ready at 10 -> earns 3 x 1500 = $4500
    Total = $16500  ->  T: 2 P: 0 C: 0

ASSUMPTIONS
    - Money is earned per time unit (this matches the PDF's test cases).
    - A shop that finishes exactly at n earns $0, so it is not built.
    - Land size, auditoriums, dance floors do not affect the answer.

RUN:  python max_profit.py 13
"""

import sys                                              # lets us read the number typed in the terminal

BUILDINGS = [                                           # all shops: (name, build time, money per time unit)
    ("T", 5, 1500),                                     # Theatre
    ("P", 4, 1000),                                     # Pub
    ("C", 10, 2000),                                    # Commercial Park
]


def add_one(mix, i):                                    # add 1 shop of type i to a mix like (T, P, C)
    counts = list(mix)                                  # copy the tuple into a list so we can change it
    counts[i] += 1                                      # add one shop (i=0 is T, i=1 is P, i=2 is C)
    return tuple(counts)                                # turn it back into a tuple, e.g. (1, 0, 0)


def solve(n):                                           # returns (best money, list of best mixes)
    if not isinstance(n, int) or n < 0:                 # n must be a whole number, 0 or more
        raise ValueError("n must be a whole number 0 or more")

    best_money = [0] * (n + 1)                          # best_money[t] = most money possible with t time units
    best_mixes = [{(0, 0, 0)} for _ in range(n + 1)]    # best_mixes[t] = mixes that earn it (start: build nothing)

    for t in range(n + 1):                              # work from small t up to n
        for i, (name, build_time, rate) in enumerate(BUILDINGS):   # try each shop as the FIRST one built
            time_left = t - build_time                  # time remaining after this shop is finished
            if time_left <= 0:                          # shop would finish at or after t, so it earns $0
                continue                                # skip this shop

            money = rate * time_left + best_money[time_left]   # this shop's money + best money for the rest

            if money > best_money[t]:                   # found a better total than before
                best_money[t] = money                   # save the new best money
                best_mixes[t] = set()                   # forget the older, worse mixes

            if money == best_money[t]:                  # this choice equals the best total
                for mix in best_mixes[time_left]:       # take each best mix for the leftover time
                    best_mixes[t].add(add_one(mix, i))  # and add this shop to it

    mixes = sorted(best_mixes[n], reverse=True)         # sort: most T first, then most P, then most C
    return best_money[n], mixes                         # e.g. (3000, [(1, 0, 0), (0, 1, 0)])


def format_result(n, money, mixes):                     # turn the answer into text like the PDF
    lines = [f"Time Unit: {n}", f"Earnings: ${money}", "Solutions"]   # first three lines
    for number, (t, p, c) in enumerate(mixes, start=1):               # number each mix 1, 2, 3...
        lines.append(f"{number}. T: {t} P: {p} C: {c}")               # e.g. "1. T: 2 P: 0 C: 0"
    return "\n".join(lines)                             # join all lines with new lines


def main(args):                                         # runs the program with what was typed in the terminal
    if len(args) != 1:                                  # we need exactly one number
        print("Usage: python max_profit.py <time units>")
        return 1                                        # 1 means "error"

    text = args[0]                                      # the typed value, e.g. "13"
    if not text.isdigit():                              # only digits allowed, so "-5" and "abc" are rejected
        print("Error: time units must be a whole number 0 or more")
        return 1

    n = int(text)                                       # turn "13" into the number 13
    money, mixes = solve(n)                             # solve the problem
    print(format_result(n, money, mixes))               # print the answer
    return 0                                            # 0 means "success"


if __name__ == "__main__":                              # only runs when started directly, not when imported
    sys.exit(main(sys.argv[1:]))                        # sys.argv[1:] = what you typed after the file name