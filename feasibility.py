# Vérifie que les heures d'arrivée et de départ des avions sont dans les fenêtres de temps autorisées
# heure -> xi
def verifier_fenetres(avions, heures):
    for i, heure in heures.items():
        # print(f"Vérification de l'avion {i}: heure = {heure}, fenêtre = [{avions[i]['E']}, {avions[i]['L']}]")
        if not avions[i]["E"] <= heure <= avions[i]["L"]:
            return False
    return True