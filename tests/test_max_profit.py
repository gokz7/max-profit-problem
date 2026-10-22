"""
TESTS - Max Profit Problem (Task 2)

What these tests check:
    1. The 3 test cases from the PDF give the exact expected answer.
    2. The printed output matches the PDF format exactly.
    3. Too little time (n = 0 to 4) earns $0.
    4. Bad input gives an error instead of a wrong answer.
    5. The fast DP and the slow exhaustive search agree for n = 0 to 40.
    6. More time never earns less money.

RUN:  pytest -v
"""

import pytest                                           # the testing tool
from max_profit import solve, format_result, main       # the code we are testing
from exhaustive_search import exhaustive_solve          # the slow checker, to compare against


# ---------- 1. The 3 test cases from the PDF ----------

@pytest.mark.parametrize(                               # run the same test once for each row below
    "n, expected_money, expected_mixes",                # names of the 3 values in each row
    [
        (7, 3000, [(1, 0, 0), (0, 1, 0)]),              # PDF test case 1: two tied solutions
        (8, 4500, [(1, 0, 0)]),                         # PDF test case 2
        (13, 16500, [(2, 0, 0)]),                       # PDF test case 3
    ],
)
def test_pdf_cases(n, expected_money, expected_mixes):
    money, mixes = solve(n)                             # solve the problem
    assert money == expected_money                      # money must match the PDF
    assert mixes == expected_mixes                      # mixes (and their order) must match the PDF


# ---------- 2. Output format matches the PDF ----------

def test_output_format_matches_pdf():
    money, mixes = solve(7)                             # use test case 1 (it has 2 solutions)
    expected = (                                        # the exact text we expect
        "Time Unit: 7\n"
        "Earnings: $3000\n"
        "Solutions\n"
        "1. T: 1 P: 0 C: 0\n"
        "2. T: 0 P: 1 C: 0"
    )
    assert format_result(7, money, mixes) == expected   # must match character by character


# ---------- 3. Too little time earns nothing ----------

@pytest.mark.parametrize("n", [0, 1, 2, 3, 4])          # no shop can finish AND earn before time 5
def test_too_little_time_earns_nothing(n):
    assert solve(n) == (0, [(0, 0, 0)])                 # $0 and nothing built


# ---------- 4. Bad input ----------

def test_negative_n_raises():
    with pytest.raises(ValueError):                     # we EXPECT an error here
        solve(-5)                                       # negative time makes no sense


def test_non_integer_n_raises():
    with pytest.raises(ValueError):                     # we EXPECT an error here
        solve("5")                                      # text, not a number


def test_main_prints_answer(capsys):                    # capsys captures what main() prints
    exit_code = main(["13"])                            # same as typing: python max_profit.py 13
    printed = capsys.readouterr().out                   # grab the printed text
    assert exit_code == 0                               # 0 means success
    assert "Earnings: $16500" in printed                # correct money was printed
    assert "1. T: 2 P: 0 C: 0" in printed               # correct mix was printed


@pytest.mark.parametrize(
    "args",
    [
        ["-5"],                                         # negative number
        ["abc"],                                        # not a number
        [],                                             # nothing typed
        ["7", "8"],                                     # too many values
    ],
)
def test_main_rejects_bad_input(args, capsys):
    exit_code = main(args)                              # run with bad input
    assert exit_code == 1                               # 1 means error (no crash, no wrong answer)


# ---------- 5. DP agrees with exhaustive search ----------

@pytest.mark.parametrize("n", range(41))                # every n from 0 to 40
def test_dp_matches_exhaustive(n):
    assert solve(n) == exhaustive_solve(n)              # same money AND same mixes


# ---------- 6. More time never earns less ----------

def test_more_time_never_earns_less():
    previous = 0                                        # money for the previous n
    for n in range(101):                                # check n = 0 to 100
        money, _ = solve(n)                             # we only need the money here
        assert money >= previous                        # extra time can't make you poorer
        previous = money                                # remember it for the next n