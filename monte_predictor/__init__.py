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
    work_split_range: Tuple[float, float] = (1, 1)


@dataclass
class PossibleFuture:
    velocities: List[int]
    work_history: List[int]

    @property
    def duration(self) -> int:
        return len(self.velocities)


def generate_a_future(work_to_do: int, model: TeamModel) -> PossibleFuture:
    actual_work_to_do = work_to_do * random.uniform(model.work_split_range[0], model.work_split_range[1])
    velocities = []
    work_history = [actual_work_to_do]
    while actual_work_to_do > 0:
        velocity = random.choice(model.sample_velocities)
        velocities.append(velocity)
        actual_work_to_do = actual_work_to_do - velocity
        work_history.append(actual_work_to_do)
    return PossibleFuture(
        velocities=velocities,
        work_history=work_history
    )


class Prediction:
    generated_futures: List[PossibleFuture]

    _durations: List[int]
    _duration_frequency: collections.Counter

    def __init__(self, generated_futures: List[PossibleFuture]):
        self.generated_futures = generated_futures

        # Find out how many "sprints" each simulation took
        self._durations = [future.duration for future in generated_futures]

        # Now count how common each sprint number was
        self._duration_frequency = collections.Counter(self._durations)

    @property
    def mode_duration(self):
        return self._duration_frequency.most_common()[0][0]

    @property
    def duration_frequency_counts(self):
        return self._duration_frequency.items()

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
