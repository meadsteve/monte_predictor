import collections
import math
import random
from dataclasses import dataclass
from typing import List

from matplotlib import pyplot as plt

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


@dataclass
class Prediction:
    generated_futures: List[Future]

    _final_balances: collections.Counter

    def __init__(self, generated_futures: List[Future]):
        self.generated_futures = generated_futures

        # Find out how many "sprints" each simulation took
        final_balances = [future.final_balance for future in generated_futures]

        # Now count how common each sprint number was
        self._final_balances = collections.Counter(final_balances)

    @property
    def mode_final_balance(self) -> int:
        return self._final_balances.most_common()[0][0]

    @property
    def frequency_of_final_balances(self):
        return self._final_balances.items()

    def probability_of_having_money(self, target_money: int) -> float:
        successes = [
            freq for (balance, freq) in self.frequency_of_final_balances
            if balance >= target_money
        ]

        return sum(successes) / len(self.generated_futures)


def make_a_prediction(
    starting_cash: int,
    gambles_to_run: int,
    simulation_count: int = 100_000
) -> Prediction:
    # Run the number of simulations specified by the
    # model and return this as a prediction
    generated_futures = [
        generate_a_future(starting_cash, gambles_to_run)
        for _ in range(1, simulation_count)
    ]
    return Prediction(generated_futures=generated_futures)


def graph_example_histories(prediction_to_plot: Prediction):
    # Grab a bunch of the predictions and plot them
    sample_to_graph = random.sample(prediction_to_plot.generated_futures, 10)
    plt.xkcd()
    for data in sample_to_graph:
        plt.plot(data.history)

    # No point in showing backwards in time or less than no money
    plt.ylim(bottom=0)
    plt.xlim(left=0)

    # Label stuff
    plt.title("Am I rich?")
    plt.xlabel("Number of spins")
    plt.ylabel("Euros")

    plt.show()


def graph_frequencies(prediction_to_plot: Prediction):
    x, y = zip(*prediction_to_plot.frequency_of_final_balances)
    plt.xkcd()

    plt.bar(x, y, color='g')
    plt.tight_layout()

    plt.title("How rich am I at the end?")
    plt.xlabel("Euros I have")

    plt.ylim(bottom=0, top=8000)
    plt.xlim(left=0, right=150)

    plt.show()


prediction = make_a_prediction(starting_cash=100, gambles_to_run=30)

print(f"The probability of having at least a single euro: {math.floor(100 * prediction.probability_of_having_money(1))}%")
print(f"The probability of having made at least a dollar: {math.floor(100 * prediction.probability_of_having_money(101))}%")
print(f"The probability of having at least doubled your money: {math.floor(100 * prediction.probability_of_having_money(200))}%")

graph_example_histories(prediction)
graph_frequencies(prediction)


