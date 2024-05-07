"""
Pomodoro Tracker Module

This module provides classes and functions to track and visualize Pomodoro sessions.

Classes:
- PomodoroAnalyzer: Analyzes Pomodoro sessions and provides methods to calculate
and visualize data.
- PomodoroTracker: Tracks Pomodoro sessions, saves them to JSON files, and provides
methods for data visualization.
Functions:
- color_title: Creates a centered title with multiple colors for Matplotlib plots.
- get_date: Prompts the user to input a date in the format 'yy-mm-dd' or leave it
empty for today's date.
"""

import json
import os
from datetime import datetime
from typing import List, Tuple, Any, Dict, Union

from matplotlib import axes
import matplotlib.pyplot as plt
import numpy as np

DataTuple = (
    Tuple[
        List[int],  # Pomodoros effectués
        List[int],  # Estimations
        List[Union[int, float]],  # Autres données entières ou flottantes
        List[Union[int, float]],  # Autres données entières ou flottantes
        List[Any],  # Autres données de type indéterminé
    ]
    | None
)
Array = np.array
DatafTuple = Tuple[
    List[str],  # List of dates
    List[Array],  # List of numpy arrays
    List[Array],  # List of numpy arrays
]


def color_title(
    labels: List[str],
    colors: List[str],
    textprops: Dict[str, str] = None,
    a_x: axes.Axes = None,
    y_0: float = 1.013,
):
    """
    Create a good colorfull title.

    Creates a centered title with multiple colors. Don't change axes limits
    afterward.
    """
    precision = 10**-2
    if textprops is None:
        textprops = {"size": "large"}
    if a_x is None:
        a_x = plt.gca()

    plt.gcf().canvas.draw()
    transform = a_x.transAxes  # use axes coords
    x_t = 0  # where the text ends in x-axis coords
    shift = 0  # where the text starts
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
            x_pos = (
                text[label]
                .get_window_extent()
                .transformed(transform.inverted())
                .x1
            )

        x_t = x_pos  # where all text ends
        shift += precision / 2  # increase for next iteration
        if x_pos > 1:  # guardrail
            break


def get_date() -> str:
    """Ask a date."""
    date_input = input(
        "Veuillez entrer une date au format yy-mm-dd (vide pour aujourd'hui): "
    )
    if not date_input:
        return datetime.now().strftime("%y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%y-%m-%d")
            return date_input
        except ValueError:
            print("Format de date incorrect. Utilisez le format yy-mm-dd.")
            return get_date()


class PomodoroTracker:
    def __init__(self, date):
        self.SAVE_JSON_FOLDER = "./json_folder/"
        self.SAVE_PNG_FOLDER = "./png_folder/"
        self.DATE = date
        self.JSON_NAME = os.path.join(
            self.SAVE_JSON_FOLDER, f"sessions_pomodoro_{self.DATE}.json"
        )
        self.PLOT_NAME = os.path.join(
            self.SAVE_PNG_FOLDER, f"pomodoro_{self.DATE}.png"
        )

    def enregistrer_session(
        self, tache: str, duree: str, est_init: str, est_fin: str
    ) -> None:
        """Register the session pomodoro."""
        session = {
            "Tâche": tache,
            "Pomodoros effectués": duree,
            "Estimation 1": est_init,
            "Estimation 2": est_fin,
        }
        if not os.path.exists(self.JSON_NAME):
            with open(self.JSON_NAME, mode="w", encoding="utf-8") as file:
                json.dump([session], file, ensure_ascii=False, indent=4)
        else:
            with open(self.JSON_NAME, mode="r+", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = []
                data.append(session)
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)

    def calculer_donnees(self) -> DataTuple:
        """Calculate data for plotting."""
        if not os.path.exists(self.JSON_NAME):
            print("Aucune session disponible pour cette date.")
            return None

        with open(self.JSON_NAME, mode="r", encoding="utf-8") as file:
            sessions = json.load(file)

        pomo_r = []
        est = []
        pomo_e = []
        taches = []

        for i, session in enumerate(sessions, start=1):
            estimation_sum = int(session.get("Estimation 1", 0))
            estimation_sum += int(session.get("Estimation 2", 0))
            pomo_r.append(int(session.get("Pomodoros effectués", 0)))
            est.append(estimation_sum)
            pomo_e.append(i)
            taches.append(session.get("Tâche", ""))

        return pomo_e, pomo_r, est, taches

    def tracer_graphique(self, data: DataTuple, bshow: bool) -> None:
        """Plot the graph."""
        if data is None:
            return

        pomo_e, pomo_r, est, taches = data
        plt.figure(figsize=(10, 6))
        plots = [
            (pomo_e, pomo_r, "green", "Pomodoros réalisés"),
            (pomo_e, est, "blue", "Pomodoros estimés"),
        ]
        for x, y, color, label in plots:
            plt.plot(x, y, marker="o", color=color, label=label)

        plt.xlabel("Session Pomodoro")
        plt.ylabel("Nombre de Pomodoros")
        label_list = ["Réalisés, ", "Estimés, ", f"{self.DATE}"]
        colors = ["green", "blue", "black"]
        color_title(label_list, colors)
        plt.xticks(pomo_e, taches, rotation=45, ha="right")
        plt.yticks(np.arange(0, max(*pomo_r) + 1, 1))
        plt.ylim(0, max(*pomo_r) + 1)
        plt.grid(True)
        plt.savefig(self.PLOT_NAME, dpi=200)
        if bshow:
            plt.show()

    def visualiser_sessions(self, bshow):
        """Calculate data and plot the graph."""
        data = self.calculer_donnees()
        self.tracer_graphique(data, bshow)

    def main(self):
        """Compute the main part of the script."""
        while True:
            tache = input("Nom de la tâche : ")
            duree = input("Nombre de Pomodoros effectués : ")
            est_i = input("1ère estimation (Pomodoros) : ")
            est_f = input("2ème estimation (Pomodoros) : ")

            self.enregistrer_session(tache, duree, est_i, est_f)

            continuer = input("Une autre session ? ([oui]/non) : ") or "oui"
            if continuer.lower() == "non" or continuer[0].lower() == "n":
                break


class PomodoroAnalyzer:
    def __init__(self):
        self.SAVE_JSON_FOLDER = "./json_folder/"
        self.SAVE_PNG_FOLDER = "./png_folder/"

    def charger_sessions(self, date: str) -> List[dict]:
        """Load the pomodoros json sessions."""
        filename = os.path.join(
            self.SAVE_JSON_FOLDER, f"sessions_pomodoro_{date}.json"
        )
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as file:
                sessions = json.load(file)
            return sessions
        return []

    @staticmethod
    def somme_pomodoros(sessions: List) -> Tuple[int, int]:
        """Estimate the total kind of pomodoros."""
        pomodoros_realises = [
            int(session["Pomodoros effectués"])
            for session in sessions
            if session.get("Pomodoros effectués", "").isdigit()
        ]
        estimations = [
            (int(session["Estimation 1"]), int(session["Estimation 2"]))
            for session in sessions
            if (
                session.get("Estimation 1", "").isdigit()
                and session.get("Estimation 2", "").isdigit()
            )
        ]

        s_realises = sum(pomodoros_realises)
        s_estimation = sum(sum(estimation) for estimation in estimations)

        return s_realises, s_estimation

    @staticmethod
    def conv_znan(arr: np.array) -> np.array:
        """Convert zeros as nan in numpy arrays."""
        arr = arr.astype("float")
        arr[arr == 0] = np.nan

        return arr

    def calculer_donnees(self) -> DatafTuple:
        """Calculate the data for plotting."""
        # Extract dates from file names using list comprehension
        dates = [
            file.split("_")[-1].split(".")[0]
            for file in os.listdir(self.SAVE_JSON_FOLDER)
            if file.startswith("sessions_pomodoro_") and file.endswith(".json")
        ]

        # Calculate sums using map and zip
        sessions = [self.charger_sessions(date) for date in dates]
        s_realises, s_estimation = zip(*map(self.somme_pomodoros, sessions))

        # Apply znan conversion to each element in the list
        a_list_s = [
            self.conv_znan(np.array(x)) for x in [s_realises, s_estimation]
        ]

        return dates, *a_list_s

    def visualiser_sessions(self) -> None:
        """Plot the graph."""
        date_plot = datetime.now().strftime("%y-%m-%d")
        plot_name = self.SAVE_PNG_FOLDER + f"pomodoro_global_{date_plot}.png"

        dates, a_r, a_e = self.calculer_donnees()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, a_r, marker="o", color="green", label="Pomo réalisés")
        plt.plot(dates, a_e, marker="^", color="blue", label="Pomo estimés")

        plt.xlabel("Date")
        plt.ylabel("Somme des Pomodoros quotidiens")
        label_list = ["Réalisés", "Estimés", "par jour"]
        colors = ["green", "blue", "black"]
        color_title(label_list, colors)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.yticks(np.arange(0, max(*a_r, *a_e) + 1))
        plt.ylim(0, max(*a_r, *a_e) + 1)
        plt.savefig(plot_name, dpi=200)
        plt.show()
