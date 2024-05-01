"""Plot the pomodoro session of the day."""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pomodoro_logger  # pylint: disable=F0401

DATE = datetime.now().strftime("%y-%m-%d")
SAVE_PNG_FOLDER = "./png_folder/"
PLOT_NAME = SAVE_PNG_FOLDER + f"pomodoro_{DATE}.png"


def color_title(labels, colors, textprops=None, a_x=None, y_0=1.013):
    """
    Create a good colorfull title.

    Creates a centered title with multiple colors. Don't change axes limits
    afterwards.
    """
    precision = 10**-2
    if textprops is None:
        textprops = {"size": "large"}
    if a_x is None:
        a_x = plt.gca()

    plt.gcf().canvas.draw()
    transform = a_x.transAxes  # use axes coords

    # initial params
    x_t = 0  # where the text ends in x-axis coords
    shift = 0  # where the text starts

    # for text objects
    text = {}

    while (np.abs(shift - (1 - x_t)) > precision) and (shift <= x_t):
        x_pos = shift

        for label, col in zip(labels, colors):
            try:
                text[label].remove()
            except KeyError:
                pass

            text[label] = a_x.text(
                x_pos,
                y_0,
                label,
                transform=transform,
                ha="left",
                color=col,
                **textprops,
            )

            x_pos = text[label].get_window_extent().transformed(transform.inverted()).x1

        x_t = x_pos  # where all text ends

        shift += precision / 2  # increase for next iteration

        if x_pos > 1:  # guardrail
            break


def charger_sessions():
    """Load the sessions."""
    with open(pomodoro_logger.JSON_NAME, mode="r", encoding="utf-8") as file:
        sessions = json.load(file)
    return sessions


def visualiser_sessions():
    """Plot the graph."""
    sessions = charger_sessions()
    pomodoros_realises = []
    surestimation = []
    sous_estimation = []
    pomodoros_effectues = []
    taches = []

    for session in sessions:
        estimation_sum = int(session["Estimation 1"]) + int(session["Estimation 2"])
        pomodoros_realises.append(int(session["Pomodoros effectués"]))
        pomodoros_effectues.append(len(pomodoros_effectues) + 1)
        taches.append(session["Tâche"])

        if pomodoros_realises[-1] < estimation_sum:
            surestimation.append(estimation_sum)
            sous_estimation.append(np.nan)  # Utiliser NaN pour les valeurs manquantes
        elif pomodoros_realises[-1] > estimation_sum:
            sous_estimation.append(estimation_sum)
            surestimation.append(np.nan)  # Utiliser NaN pour les valeurs manquantes
        else:
            surestimation.append(np.nan)
            sous_estimation.append(np.nan)

    plt.figure(figsize=(10, 6))

    # Tracer la ligne pour le nombre de pomodoros réalisés
    plt.plot(
        pomodoros_effectues,
        pomodoros_realises,
        marker="o",
        color="green",
        label="Pomodoros réalisés",
    )

    # Tracer la ligne pour la surestimation
    plt.plot(
        pomodoros_effectues,
        surestimation,
        marker="o",
        color="red",
        label="Surestimation",
    )

    # Tracer la ligne pour la sous-estimation
    plt.plot(
        pomodoros_effectues,
        sous_estimation,
        marker="o",
        color="blue",
        label="Sous-estimation",
    )

    plt.xlabel("Session Pomodoro")
    plt.ylabel("Nombre de Pomodoros")

    label_list = ["Réalisés, ", "Sous-estimés, ", "Surestimés, ", f"{DATE}"]
    colors = ["green", "blue", "red", "black"]

    color_title(label_list, colors)

    # Ajouter les noms de tâche associés à l'axe des abscisses
    plt.xticks(pomodoros_effectues, taches, rotation=45, ha="right")
    # Ajuster les ticks et l'échelle des ordonnées pour les pomodoros entiers
    plt.yticks(
        np.arange(
            0,
            max(*pomodoros_realises, *surestimation, *sous_estimation) + 1,
            1,
        )
    )

    # Réglez les limites de l'axe des ordonnées
    plt.ylim(0, max(*pomodoros_realises, *surestimation, *sous_estimation) + 1)

    plt.grid(True)
    plt.savefig(PLOT_NAME, dpi=200)
    plt.show()


if __name__ == "__main__":
    visualiser_sessions()
