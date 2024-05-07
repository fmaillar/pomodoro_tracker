"""Plot the global Analysis."""
import os
from pomodoro_classes import PomodoroAnalyzer, PomodoroTracker

def plot_for_all_records():
    # Follow all the json_folder
    for filename in os.listdir('./json_folder'):
        # date extraction
        date = filename.split("_")[-1].split(".")[0]
        tracker = PomodoroTracker(date)
        # plot the graph for this date
        tracker.visualiser_sessions(bshow=False)


if __name__ == "__main__":
    analyzer = PomodoroAnalyzer()
    analyzer.visualiser_sessions()
    plot_for_all_records()
