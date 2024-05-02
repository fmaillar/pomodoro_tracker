"""Log the Pomodoro entries into a json file."""

import json
import os
from datetime import datetime

DATE = datetime.now().strftime("%y-%m-%d")
SAVE_JSON_FOLDER = "./json_folder/"
JSON_NAME = SAVE_JSON_FOLDER + f"sessions_pomodoro_{DATE}.json"


def enregistrer_session(tache, duree, estimation_initiale, estimation_finale):
    """Register the session pomodoro."""
    session = {
        "Tâche": tache,
        "Pomodoros effectués": duree,
        "Estimation 1": estimation_initiale,
        "Estimation 2": estimation_finale,
    }
    if not os.path.exists(JSON_NAME):
        with open(JSON_NAME, mode="w", encoding="utf-8") as file1:
            json.dump([session], file1, ensure_ascii=False, indent=4)
    else:
        with open(JSON_NAME, mode="r+", encoding="utf-8") as file2:
            try:
                data = json.load(file2)
            except json.decoder.JSONDecodeError:
                data = []
            data.append(session)
            file2.seek(0)
            json.dump(data, file2, ensure_ascii=False, indent=4)


def main():
    """Compute the main part of the script."""
    print("Bienvenue dans PomodoroTracker !")
    while True:
        tache = input("Nom de la tâche : ")
        duree = input("Nombre de Pomodoros effectués : ")
        estimation_initiale = input("1ère estimation (Pomodoros) : ")
        estimation_finale = input("2ème estimation (Pomodoros) : ")

        enregistrer_session(tache, duree, estimation_initiale, estimation_finale)

        continuer = (
            input("Voulez-vous enregistrer une autre session ? ([oui]/non) : ") or "oui"
        )
        if continuer.lower() == "non" or continuer[0].lower() == "n":
            break


if __name__ == "__main__":
    if not os.path.exists(JSON_NAME):
        with open(JSON_NAME, mode="w", encoding="utf-8") as file:
            pass
    main()
