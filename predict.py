from monte_predictor import make_a_prediction, TeamModel
from monte_predictor.visuals import graph_example_histories, graph_frequencies

print("Predicting...\n\n")

# Randomly pulled in per week data. Loaded from jira then monkeyed around in
# google sheets. Includes all story kinds including bug fix work.
previous_velocities = [
    8,
    13,
    11,
    6,
    15,
    4,
    4,
    5,
    2,
    10,
    15,
    9,
    15
]


model = TeamModel(
    # Use the previous data we have for how quickly the team works
    sample_velocities=previous_velocities,
    # Assuming a large amount of work splitting as the velocities include bug fixing
    work_split_range=(1, 5)
)

# Lets make a prediction on how long it would take us to do a piece of work currently
# broken down into 10 stories
prediction = make_a_prediction(
    work_to_do=10,
    model=model,
    simulation_count=10_000  # Running 10k predictions should be quick but accurate
)

# Print out the probability of completing the work in
# a few given time periods
for weeks in range(max(prediction.mode_duration - 5, 0), prediction.mode_duration + 4):
    complete_within = prediction.probability_of_completion(weeks)
    print(f"The chance of completion within {weeks} weeks is {round(complete_within * 100)}%")

graph_frequencies(prediction)
graph_example_histories(prediction)
