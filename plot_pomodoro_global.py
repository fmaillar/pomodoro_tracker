import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from pomodoro_logger import color_title


class PomodoroAnalyzer:
    def __init__(self):
        self.SAVE_JSON_FOLDER = "./json_folder/"
        self.SAVE_PNG_FOLDER = "./png_folder/"

    def charger_sessions(self, date):
        """Load the pomodoros json sessions."""
        filename = self.SAVE_JSON_FOLDER + f"sessions_pomodoro_{date}.json"
        if os.path.exists(filename):
            with open(filename, mode="r", encoding="utf-8") as file:
                sessions = json.load(file)
            return sessions

        return []

    @staticmethod
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

    @staticmethod
    def diff_with_first_value(arr):
        """Compute the differences between array elements while keeping the first value intact."""
        arr_diff = np.diff(arr)
        return np.insert(arr_diff, 0, arr[0])

    def calculer_donnees(self):
        """Calculate the data for plotting."""
        dates = []
        s_realises_list = []
        s_sous_estimation_list = []
        s_surestimation_list = []

        # Obtenez la liste des fichiers JSON dans le répertoire
        files = [
            file
            for file in os.listdir(self.SAVE_JSON_FOLDER)
            if file.startswith("sessions_pomodoro_") and file.endswith(".json")
        ]

        for file in files:
            # Extraire la date du nom du fichier
            date = file.split("_")[-1].split(".")[0]
            dates.append(date)

            sessions = self.charger_sessions(date)
            s_realises, s_sous_estimation, s_surestimation = self.somme_pomodoros(sessions)
            s_realises_list.append(s_realises)
            s_sous_estimation_list.append(s_sous_estimation)
            s_surestimation_list.append(s_surestimation)

        return dates, s_realises_list, s_sous_estimation_list, s_surestimation_list

    def tracer_graphique(self, x_data, y_data, color, label):
        """Plot a single line on the graph."""
        plt.plot(
            x_data,
            self.diff_with_first_value(y_data),
            marker="o",
            color=color,
            label=label,
        )

    def visualiser_sessions(self):
        """Plot the graph."""
        date_plot = datetime.now().strftime("%y-%m-%d")
        plot_name = self.SAVE_PNG_FOLDER + f"pomodoro_global_{date_plot}.png"

        dates, s_realises_list, s_sous_estimation_list, s_surestimation_list = self.calculer_donnees()

        plt.figure(figsize=(10, 6))

        # Tracer la somme des pomodoros réalisés
        self.tracer_graphique(dates, s_realises_list, "green", "Pomodoros réalisés")

        # Tracer la somme des pomodoros sous-estimés
        self.tracer_graphique(dates, s_sous_estimation_list, "blue", "Sous-estimation")

        # Tracer la somme des pomodoros surestimés
        self.tracer_graphique(dates, s_surestimation_list, "red", "Surestimation")

        plt.xlabel("Date")
        plt.ylabel("Somme des Pomodoros quotidiens")
        label_list = ["Réalisés, ", "Sous-estimés, ", "Surestimés, ", "par jour"]
        colors = ["green", "blue", "red", "black"]

        color_title(label_list, colors)

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

        plt.savefig(plot_name, dpi=200)
        plt.show()


if __name__ == "__main__":
    analyzer = PomodoroAnalyzer()
    analyzer.visualiser_sessions()
