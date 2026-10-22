# Max Profit Problem

Ever Quint Interview Assignment, Task 2.

Given **n** time units, find the mix of buildings that earns Mr. X the most money.

---

## The Problem

Mr. X builds shops **one at a time** (never two in parallel). A shop earns money
every time unit from the moment it is finished until time **n** ends.

| Shop | Build time | Earnings per time unit |
|---|---|---|
| Theatre (T) | 5 | $1500 |
| Pub (P) | 4 | $1000 |
| Commercial Park (C) | 10 | $2000 |

The output is the maximum earnings, plus every shop mix that achieves it, in the format `T: x P: y C: z`.

---

## Results (PDF test cases)

| Input (n) | Expected | Output | Status |
|---|---|---|---|
| 7 | $3000. `T:1 P:0 C:0` or `T:0 P:1 C:0` | $3000. Both solutions | ✅ |
| 8 | $4500. `T:1 P:0 C:0` | $4500. `T:1 P:0 C:0` | ✅ |
| 13 | $16500. `T:2 P:0 C:0` | $16500. `T:2 P:0 C:0` | ✅ |

```
$ python max_profit.py 7
Time Unit: 7
Earnings: $3000
Solutions
1. T: 1 P: 0 C: 0
2. T: 0 P: 1 C: 0
```

---

## Assumptions

The PDF leaves some details unstated. These were decided, and checked against the test cases:

1. **Earnings are per time unit.** The table only says "$1500", but n=7 → $3000 only works as 2 units × $1500.
2. **A shop that finishes exactly at time n earns $0, so it is not built or counted.** At n=8, a second Pub would finish at 8 and earn nothing. The expected answer is `T:1` only, which confirms this.
3. **Land size, auditoriums, commercial spaces and dance floors don't affect the answer.** Land is stated as infinite, and none of these change earnings.
4. **If no shop can earn money (n ≤ 4), the answer is $0 with `T: 0 P: 0 C: 0`.**
5. **Tied solutions are listed with the most Theatres first, then Pubs, then Commercial Parks.** This matches the order in test case 1.
6. **Input must be a whole number, 0 or more.** Anything else prints a clear error.

---

## Approach: Dynamic Programming

**Key point: order matters.** The first shop built earns for the longest time. So we can't just pick the shop with the best rate. We need to compare whole build plans.

For every amount of time `t` from 0 up to `n`, we compute the best money possible:

```
best(t) = max over each shop S that finishes before t of:
              rate(S) × (t − build_time(S))    ← money from building S first
            + best(t − build_time(S))          ← best money from the time left
best(t) = 0 if no shop can finish before t
```

Because `t` goes from small to large, `best(time left)` is always already computed.
All mixes that tie for the best value are kept. That's how n=7 returns two solutions.

**Worked example (n = 13):**

| Build first | Money from it | + Best for time left | Total |
|---|---|---|---|
| Theatre | (13−5) × 1500 = 12000 | best(8) = 4500 | **16500** ✅ |
| Pub | (13−4) × 1000 = 9000 | best(9) = 6000 | 15000 |
| Commercial | (13−10) × 2000 = 6000 | best(3) = 0 | 6000 |

**Complexity:** O(n) time, since there are 3 choices for each `t`, and O(n) memory.

---

## Proof of Correctness

Passing 3 test cases doesn't prove the solver is right for every `n`. So the DP is checked against a second, independent method.

**Exhaustive search** (`exhaustive_search.py`) tries **every possible build order**, calculates the money directly from the timeline (`rate × (n − finish time)`), and keeps the best. It's slow for big `n`, but simple enough to trust.

**Result: the DP and exhaustive search give identical money and mixes for every n from 0 to 40.**

**58 automated tests** (pytest) cover:
- the 3 PDF test cases (money, mixes and order)
- the exact output format
- n = 0 to 4 earning $0
- bad input: negative numbers, text, and a missing or extra argument
- DP vs exhaustive search for n = 0 to 40
- more time never earning less money (n = 0 to 100)

---

## Insights

**1. Commercial Park is never the right choice.**
With `r` time units left, compare one Commercial Park with two Theatres. Both take 10 units to build.

- One C earns: `2000 × (r − 10)` = **2000r − 20000**
- Two T earn: `1500 × (r − 5) + 1500 × (r − 10)` = **3000r − 22500**

Two Theatres win whenever `1000r > 2500`, which means `r > 2.5`. But a Commercial Park only earns anything when `r > 10`. So it never wins, despite having the highest rate.

**2. Theatres dominate, and Pubs fill leftover time.**
Earnings per unit of build time: Theatre 1500/5 = **300**, Pub 1000/4 = **250**, Commercial 2000/10 = **200**.
Optimal plans are mostly Theatres. A Pub only appears when its shorter build fits the remaining time better (for example, n = 10 → `T:1 P:1`).

---

## How to Run

**Requirements:** Python 3.10+

```bash
git clone https://github.com/gokz7/max-profit-problem.git
cd max-profit-problem
python -m venv .venv
```

Activate the virtual environment:
- **Windows (cmd):** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

**Solve for any n:**
```bash
python max_profit.py 13
```

**Compare DP vs exhaustive search (n = 0 to 40 by default):**
```bash
python exhaustive_search.py
python exhaustive_search.py 30
```

**Run all tests:**
```bash
pytest -v
```

---

## Project Structure

```
max-profit-problem/
├── max_profit.py          # DP solver + command-line program
├── exhaustive_search.py   # tries every build order, to verify the DP
├── tests/
│   └── test_max_profit.py # 58 pytest tests
├── pytest.ini             # pytest settings
├── requirements.txt       # dependencies (pytest)
└── README.md
```