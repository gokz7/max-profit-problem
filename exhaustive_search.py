"""
EXHAUSTIVE SEARCH CHECKER - Max Profit Problem (Task 2)

WHY THIS FILE EXISTS
max_profit.py uses a fast, clever method (Dynamic Programming).
This file uses a slow but very simple method: try EVERY possible build order.
If both methods always give the same answer, the fast method is correct.

HOW IT WORKS
Start with nothing built. Try adding T, P or C. From each of those, try
adding T, P or C again... until no shop can finish before time n.
Every path is one plan. Money for each shop = rate x (n - finish time).
Then we pick the plan(s) with the most money.

EXAMPLE (n = 13)
    T then T -> 12000 + 4500 = $16500   (best)
    T then P -> 12000 + 4000 = $16000
    P then T ->  9000 + 6000 = $15000
    C only   ->  6000        = $6000

It's only for checking: it gets slow for big n.

RUN:  python exhaustive_search.py       (checks n = 0 to 40)
      python exhaustive_search.py 30    (checks n = 0 to 30)
"""

import sys                                              # lets us read the number typed in the terminal
from max_profit import BUILDINGS, add_one, solve        # reuse the shop list, the helper, and the DP to compare


def exhaustive_solve(n):                                # returns (best money, list of best mixes)
    plans = []                                          # every plan we find: (money, mix)

    def explore(time_used, money, mix):                 # one step in the tree of choices
        plans.append((money, mix))                      # stopping here is a complete plan, so save it
        for i, (name, build_time, rate) in enumerate(BUILDINGS):   # try adding each shop next
            finish = time_used + build_time             # when this new shop would be finished
            if finish >= n:                             # finishes at or after n, so it earns $0
                continue                                # skip it
            shop_money = rate * (n - finish)            # money it earns from finish until n
            explore(finish, money + shop_money, add_one(mix, i))   # keep going with this longer plan

    explore(0, 0, (0, 0, 0))                            # start: time 0, $0, nothing built

    best = max(money for money, mix in plans)           # the highest money of all plans
    best_mixes = {mix for money, mix in plans if money == best}    # all mixes with that money (no duplicates)
    return best, sorted(best_mixes, reverse=True)       # same format and order as solve(n)


def main(args):                                         # compares DP and exhaustive search for many n
    max_n = 40                                          # default: check n = 0 to 40
    if args:                                            # if the user typed a number, use it
        if not args[0].isdigit():                       # only whole numbers allowed
            print("Error: please give a whole number 0 or more")
            return 1
        max_n = int(args[0])

    all_match = True                                    # becomes False if any answer is different
    for n in range(max_n + 1):                          # check every n from 0 to max_n
        dp = solve(n)                                   # answer from the fast DP method
        ex = exhaustive_solve(n)                        # answer from trying every order
        status = "OK" if dp == ex else "MISMATCH"       # do they agree?
        if dp != ex:
            all_match = False
        print(f"n={n:>3}  {status:<8}  money=${dp[0]:<7}  mixes={dp[1]}")   # one line per n

    if all_match:                                       # final summary
        print(f"\nRESULT: all {max_n + 1} cases match. The DP is correct.")
        return 0                                        # 0 means "success"
    print("\nRESULT: mismatch found. The DP has a bug.")
    return 1                                            # 1 means "something failed"


if __name__ == "__main__":                              # only runs when started directly
    sys.exit(main(sys.argv[1:]))                        # sys.argv[1:] = what you typed after the file name