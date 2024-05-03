"""Plot the global analysis of pomodoros."""

import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import plot_pomodoro  # pylint: disable=F0401
import pomodoro_logger  # pylint: disable=F0401

DATE_PLOT = datetime.now().strftime("%y-%m-%d")
SAVE_PNG_FOLDER = "./png_folder/"
SAVE_JSON_FOLDER = "./json_folder/"
PLOT_NAME = SAVE_PNG_FOLDER + f"pomodoro_global_{DATE_PLOT}.png"


def charger_sessions(date):
    """Load the pomodoros json sessions."""
    filename = SAVE_JSON_FOLDER + f"sessions_pomodoro_{date}.json"
    if os.path.exists(filename):
        with open(filename, mode="r", encoding="utf-8") as file:
            sessions = json.load(file)
        return sessions

    return []


def somme_pomodoros(sessions):
    """Estimate the total kind of pomodoros."""
    somme_realises = 0
    somme_sous_estimation = 0
    somme_surestimation = 0

    for session in sessions:
        estimation_sum = int(session["Estimation 1"]) + int(session["Estimation 2"])
        pomodoros_realises = int(session["Pomodoros effectués"])

        if pomodoros_realises < estimation_sum:
            somme_sous_estimation += estimation_sum - pomodoros_realises
        elif pomodoros_realises > estimation_sum:
            somme_surestimation += pomodoros_realises - estimation_sum

        somme_realises += pomodoros_realises

    return somme_realises, somme_sous_estimation, somme_surestimation

def diff_with_first_value(arr):
    """Compute the differences between array elements while keeping the first value intact."""
    arr_diff = np.diff(arr)
    return np.insert(arr_diff, 0, arr[0])

def visualiser_sessions():
    """Plot the graph."""
    dates = []
    s_realises_list = []
    s_sous_estimation_list = []
    s_surestimation_list = []

    # Obtenez la liste des fichiers JSON dans le répertoire
    files = [
        file
        for file in os.listdir(SAVE_JSON_FOLDER)
        if file.startswith("sessions_pomodoro_") and file.endswith(".json")
    ]

    for file in files:
        # Extraire la date du nom du fichier
        date = file.split("_")[-1].split(".")[0]
        dates.append(date)

        sessions = charger_sessions(date)
        s_realises, s_sous_estimation, s_surestimation = somme_pomodoros(sessions)
        s_realises_list.append(s_realises)
        s_sous_estimation_list.append(s_sous_estimation)
        s_surestimation_list.append(s_surestimation)

    plt.figure(figsize=(10, 6))

    # Tracer la somme des pomodoros réalisés
    plt.plot(
        dates,
        diff_with_first_value(s_realises_list),
        marker="o",
        color="green",
        label="Pomodoros réalisés",
    )

    # Tracer la somme des pomodoros sous-estimés
    plt.plot(
        dates,
        diff_with_first_value(s_sous_estimation_list),
        marker="o",
        color="blue",
        label="Sous-estimation",
    )

    # Tracer la somme des pomodoros surestimés
    plt.plot(
        dates,
        diff_with_first_value(s_surestimation_list),
        marker="o",
        color="red",
        label="Surestimation",
    )

    plt.xlabel("Date")
    plt.ylabel("Somme des Pomodoros quotidiens")
    label_list = ["Réalisés, ", "Sous-estimés, ", "Surestimés, ", "par jour"]
    colors = ["green", "blue", "red", "black"]

    plot_pomodoro.color_title(label_list, colors)

    plt.grid(True)
    plt.xticks(rotation=45)
    plt.yticks(
        np.arange(
            0,
            max(
                *s_realises_list,
                *s_sous_estimation_list,
                *s_surestimation_list,
            )
            + 1,
        )
    )

    plt.ylim(
        0,
        max(*s_realises_list, *s_sous_estimation_list, *s_surestimation_list) + 1,
    )

    plt.savefig(f"{PLOT_NAME}", dpi=200)
    plt.show()


if __name__ == "__main__":
    visualiser_sessions()
