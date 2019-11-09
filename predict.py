from monte_predictor import make_a_prediction

print("Predicting...\n\n")

# The velocities for the previous N time periods (could be days, sprints, weeks etc.)
# The velocities could be in story points, number of stories or another unit as
# long as the unit is the same.
# In this case the total work was 24 over 7 time periods
previous_velocities = [2, 4, 5, 2, 3, 5, 3]

# Lets make a prediction on how long it would take us to do the
# same 24 points of work (this can be used to see if out model is sensible)
prediction = make_a_prediction(
    work_to_do=24,
    sample_velocities=previous_velocities
)

for sprints in [5, 6, 7, 8, 9, 10]:
    complete_within = prediction.probability_of_completion(sprints)
    print(f"The chance of completion within {sprints} sprints is {round(complete_within * 100)}%")
