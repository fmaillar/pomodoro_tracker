"""Log the Pomodoro entries into a json file."""

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


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


def get_date():
    """Demander à l'utilisateur de choisir une date ou laisser vide pour aujourd'hui."""
    date_input = input("Veuillez entrer une date au format yy-mm-dd (laissez vide pour aujourd'hui) : ")
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
        self.SAVE_PNG_FOLDER = './png_folder/'
        self.DATE = date
        self.PLOT_NAME = self.SAVE_PNG_FOLDER + f"pomodoro_{self.DATE}.png"

    def enregistrer_session(self, tache, duree, estimation_initiale, estimation_finale):
        """Register the session pomodoro."""
        json_name = self.SAVE_JSON_FOLDER + f"sessions_pomodoro_{self.DATE}.json"
        session = {
            "Tâche": tache,
            "Pomodoros effectués": duree,
            "Estimation 1": estimation_initiale,
            "Estimation 2": estimation_finale,
        }
        if not os.path.exists(json_name):
            with open(json_name, mode="w", encoding="utf-8") as file:
                json.dump([session], file, ensure_ascii=False, indent=4)
        else:
            with open(json_name, mode="r+", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = []
                data.append(session)
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)

    def calculer_donnees(self):
        """Calculate data for plotting."""
        json_name = self.SAVE_JSON_FOLDER + f"sessions_pomodoro_{self.DATE}.json"
        if not os.path.exists(json_name):
            print("Aucune session disponible pour cette date.")
            return None

        with open(json_name, mode="r", encoding="utf-8") as file:
            sessions = json.load(file)

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

        return pomodoros_effectues, pomodoros_realises, surestimation, sous_estimation, taches

    def tracer_graphique(self, data, bshow):
        """Plot the graph."""
        if data is None:
            return

        pomodoros_effectues, pomodoros_realises, surestimation, sous_estimation, taches = data

        plt.figure(figsize=(10, 6))

        plots = [
            (pomodoros_effectues, pomodoros_realises, 'green', 'Pomodoros réalisés'),
            (pomodoros_effectues, surestimation, 'red', 'Surestimation'),
            (pomodoros_effectues, sous_estimation, 'blue', 'Sous-estimation')
        ]

        for x, y, color, label in plots:
            plt.plot(
                x,
                y,
                marker="o",
                color=color,
                label=label,
            )

        plt.xlabel("Session Pomodoro")
        plt.ylabel("Nombre de Pomodoros")

        label_list = ["Réalisés, ", "Sous-estimés, ", "Surestimés, ", f"{self.DATE}"]
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
            estimation_initiale = input("1ère estimation (Pomodoros) : ")
            estimation_finale = input("2ème estimation (Pomodoros) : ")

            self.enregistrer_session(tache, duree, estimation_initiale, estimation_finale)

            continuer = (
                    input("Voulez-vous enregistrer une autre session ? ([oui]/non) : ") or "oui"
            )
            if continuer.lower() == "non" or continuer[0].lower() == "n":
                break


if __name__ == "__main__":
    print("Bienvenue dans PomodoroTracker !")
    while True:
        date = get_date()
        pomodoro_tracker = PomodoroTracker(date)
        pomodoro_tracker.main()
        tracer_session = input("Voulez-vous tracer la figure de cette journée ? (oui/[non]) : ") or "non"
        if tracer_session.lower() == "oui" or tracer_session[0].lower() == "o":
            pomodoro_tracker.visualiser_sessions(False)
        continuer_global = input(
            "Voulez-vous enregistrer une session pour une autre date ? ([oui]/non) : ") or "oui"
        if continuer_global.lower() == "non" or continuer_global[0].lower() == "n":
            break
