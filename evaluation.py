# Calcul du coût d'une solution (P1)
def cout_p1(avions, heures):
    """
    Calcule le coût total des avances et retards (P1).

    avions : dictionnaire contenant T, g et h pour chaque avion.
    heures : dictionnaire contenant l'heure réelle d'atterrissage.

    Retourne le coût total.
    """
    cout = 0

    for i in avions:
        T = avions[i]["T"]
        g = avions[i]["g"]
        h = avions[i]["h"]
        x = heures[i]

        avance = max(0, T - x)
        retard = max(0, x - T)

        cout += g * avance + h * retard

    return cout

# TODO : retirer dans les reste du code et utiliser P1
# Calcul du coût d'une solution (P2)
def cout_p2(heures):
    return max(heures.values())