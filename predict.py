from monte_predictor import make_a_prediction, TeamModel
from monte_predictor.visuals import graph_example_histories, graph_frequencies

print("Predicting...\n\n")

# Some point per sprint velocities
previous_velocities = [81, 18, 48, 38, 10, 47, 38]


model = TeamModel(
    # Use the previous data we have for how quickly the team works
    sample_velocities=previous_velocities,
    # Now assume the team actually does 1 - 3 times the estimated work
    work_split_range=(1, 3)
)

# Lets make a prediction on how long it would take to do a task that's initially broken down
# as 164 points
prediction = make_a_prediction(
    work_to_do=164,
    model=model,
    simulation_count=10_000  # Running 10k predictions should be quick but accurate
)

# Print out the probability of completing the work in
# a few given time periods
for sprints in range(max(prediction.mode_duration - 5, 0), prediction.mode_duration + 4):
    complete_within = prediction.probability_of_completion(sprints)
    print(f"The chance of completion within {sprints} sprints is {round(complete_within * 100)}%")

graph_frequencies(prediction)
graph_example_histories(prediction)
