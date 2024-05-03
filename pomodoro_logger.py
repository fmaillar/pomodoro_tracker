"""Log the Pomodoro entries into a json file."""
from pomodoro_classes import PomodoroTracker, get_date

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
