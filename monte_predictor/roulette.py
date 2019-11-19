import math
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Future:
    history: List[int]
    final_balance: int


def _put_it_on_red(bet: int) -> int:
    # 48.60% is the odds on winning if it all goes on red
    if random.random() <= 0.4860:
        return bet * 2
    return 0


def generate_a_future(cash: int, gambles_to_run: int) -> Future:
    # Keep a record of our fortunes:
    money_history = [cash]

    # Whilst we've still got time and money lets spin
    while cash > 0 and len(money_history) <= gambles_to_run:

        # We've decided our strategy is to always bet half our remaining
        # cash on red
        bet = math.ceil(cash / 2)
        cash = cash - bet
        winnings = _put_it_on_red(bet)

        # Add our winnings back to our pile of money
        cash = cash + winnings
        money_history.append(cash)

    # Gambling complete. Return the history
    return Future(history=money_history, final_balance=cash)


print(generate_a_future(100, 10))
print(generate_a_future(100, 10))
print(generate_a_future(100, 10))
print(generate_a_future(100, 10))
print(generate_a_future(100, 10))
