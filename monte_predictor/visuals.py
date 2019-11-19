import random

from matplotlib import pyplot as plt

from monte_predictor import Prediction


def graph_example_histories(prediction: Prediction):
    # Grab a bunch of the predictions and plot them
    sample_to_graph = random.sample(prediction.generated_futures, 50)
    plt.xkcd()
    for data in sample_to_graph:
        plt.plot(data.work_history)

    # No point in showing backwards in time or less than no work
    # remaining
    plt.ylim(bottom=0)
    plt.xlim(left=0)

    # Label stuff
    plt.title("Example work history")
    plt.xlabel("Number of weeks/sprints/iterations")
    plt.ylabel("Work remaining")

    plt.show()


def graph_frequencies(prediction: Prediction):
    x, y = zip(*prediction.duration_frequency_counts)
    plt.xkcd()

    plt.bar(x, y, color='g')
    plt.tight_layout()

    plt.title("Distribution of time taken")
    plt.xlabel("Number of weeks/sprints/iterations")

    plt.ylim(bottom=0)
    plt.xlim(left=0)

    plt.show()
