import collections
import random
from dataclasses import dataclass
from typing import List


def generate_a_future(work_to_do: int, sample_velocities: List[int]) -> List[int]:
    future = []
    while work_to_do > 0:
        velocity = random.choice(sample_velocities)
        future.append(velocity)
        work_to_do = work_to_do - velocity
    return future


@dataclass
class Prediction:
    generated_futures: List[List[int]]
    durations: List[int]
    duration_frequency: collections.Counter

    def probability_of_completion(self, target_duration: int) -> float:
        # Get the frequency of each prediction where
        # the work was completed within the target duration
        successes = [
            freq for (duration, freq) in self.duration_frequency.items()
            if duration <= target_duration
        ]

        # Now calculate what percentage of the total these
        # succesfully predictions made up
        return sum(successes) / len(self.generated_futures)


def make_a_prediction(work_to_do: int, sample_velocities: List[int]) -> Prediction:
    # Run a 10,000 simulations. This should be relatively quick
    generated_futures = [
        generate_a_future(work_to_do, sample_velocities)
        for _ in range(1, 10000)
    ]

    # Find out how many "sprints" each simulation took
    durations = [len(future) for future in generated_futures]

    # Now count how common each sprint number was
    duration_frequency = collections.Counter(durations)

    return Prediction(
        generated_futures=generated_futures,
        durations=durations,
        duration_frequency=duration_frequency
    )