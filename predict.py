from monte_predictor import make_a_prediction, TeamModel
from monte_predictor.visuals import graph_example

print("Predicting...\n\n")

# The velocities for the previous N time periods (could be days, sprints, weeks etc.)
# The velocities could be in story points, number of stories or another unit as
# long as the unit is the same.
# In this case the total work was 24 over 7 time periods
previous_velocities = [2, 4, 5, 2, 3, 5, 3]

# An example of a less consistent team
# previous_velocities = [1, 3, 8, 1, 2, 6, 3]


model = TeamModel(
    # Use the previous data we have for how quickly the team works
    sample_velocities=previous_velocities,
    # Now assume the team creates up to about half as many stories again whilst working
    work_split_range=(1, 1.5)
)

# Lets make a prediction on how long it would take us to do the
# 19 points. Given we've modeled the team often split
# out extra stories between 1 and 1.5 times the initial estimate
# we'd expect the team to complete about 24 points
# therefor the model should give predictions close to the initial
# data (7 time periods)
prediction = make_a_prediction(
    work_to_do=19,
    model=model,
    simulation_count=10_000  # Running 10k predictions should be quick but accurate
)

# Print out the probability of completing the work in
# a few given time periods
for sprints in range(prediction.mode_duration - 4, prediction.mode_duration + 3):
    complete_within = prediction.probability_of_completion(sprints)
    print(f"The chance of completion within {sprints} sprints is {round(complete_within * 100)}%")

graph_example(prediction)
