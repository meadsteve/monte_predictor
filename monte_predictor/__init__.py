import collections
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class TeamModel:
    # Set of previous velocities for the team
    sample_velocities: List[int]

    # The upper and lower bound for how many stories get
    # resolved for each starting story. This would include
    # bug fix work if the velocity included bug fixes.
    work_split_range: Tuple[int, int] = (1, 1)


def generate_a_future(work_to_do: int, model: TeamModel) -> List[int]:
    future = []
    actual_work_to_do = work_to_do * random.uniform(model.work_split_range[0], model.work_split_range[1])
    while actual_work_to_do > 0:
        velocity = random.choice(model.sample_velocities)
        future.append(velocity)
        actual_work_to_do = actual_work_to_do - velocity
    return future


class Prediction:
    generated_futures: List[List[int]]

    _durations: List[int]
    _duration_frequency: collections.Counter

    def __init__(self, generated_futures):
        self.generated_futures = generated_futures

        # Find out how many "sprints" each simulation took
        self._durations = [len(future) for future in generated_futures]

        # Now count how common each sprint number was
        self._duration_frequency = collections.Counter(self._durations)

    def probability_of_completion(self, target_duration: int) -> float:
        # Get the frequency of each prediction where
        # the work was completed within the target duration
        successes = [
            freq for (duration, freq) in self._duration_frequency.items()
            if duration <= target_duration
        ]

        # Now calculate what percentage of the total these
        # successful predictions made up
        return sum(successes) / len(self.generated_futures)


def make_a_prediction(
        work_to_do: int,
        model: TeamModel,
        simulation_count: int = 100_000
) -> Prediction:
    # Run the number of simulations specified by the
    # model and return this as a prediction
    generated_futures = [
        generate_a_future(work_to_do, model)
        for _ in range(1, simulation_count)
    ]
    return Prediction(generated_futures)
