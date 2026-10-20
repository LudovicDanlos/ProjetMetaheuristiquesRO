# Algorithme glouton pour construire une solution initiale.
def construire_solution(avions, separations, nb_pistes):
    # Chaque piste contient une liste d'avions.
    pistes = [[] for _ in range(nb_pistes)]
    heures = {}

    # Commencer par les avions dont l'heure cible est la plus tôt.
    ordre = sorted(avions, key=lambda i: avions[i]["T"])

    for i in ordre:
        meilleur_choix = None

        for r in range(nb_pistes):
            # On commence à l'heure la plus tôt autorisée.
            heure = avions[i]["E"]

            # Respecter la séparation avec le dernier avion de la piste.
            if pistes[r]:
                dernier = pistes[r][-1]
                s = separations.get((dernier, i),
                                    separations.get((i, dernier), 0))
                heure = max(heure, heures[dernier] + s)

            if heure <= avions[i]["L"]:
                choix = (heure, r)

                if meilleur_choix is None or choix < meilleur_choix:
                    meilleur_choix = choix

        if meilleur_choix is None:
            return None  # Échec : aucune piste faisable trouvée.

        heure, r = meilleur_choix
        pistes[r].append(i)
        heures[i] = heure

    return pistes, heures
