# Vérifie que les heures d'arrivée et de départ des avions sont dans les fenêtres de temps autorisées
# heure -> xi
def verifier_fenetres(avions, heures):
    for i, heure in heures.items():
        # print(f"Vérification de l'avion {i}: heure = {heure}, fenêtre = [{avions[i]['E']}, {avions[i]['L']}]")
        if not avions[i]["E"] <= heure <= avions[i]["L"]:
            return False
    return True


def verifier_separations(avions, heures, pistes, separation):
    """
    Vérifie les séparations de sécurité entre les avions
    qui utilisent la même piste.

    heures : {avion: heure_atterrissage}
    pistes : {avion: numero_piste}
    separation : {(i, j): temps_separation}
    """

    liste_avions = list(avions.keys())

    # Examiner chaque paire d'avions une seule fois
    for position in range(len(liste_avions)):
        i = liste_avions[position]

        for autre_position in range(position + 1, len(liste_avions)):
            j = liste_avions[autre_position]

            # Si les avions utilisent des pistes différentes,
            # aucune séparation n'est nécessaire entre eux.
            if pistes[i] != pistes[j]:
                continue

            # Déterminer lequel des deux avions atterrit en premier
            if heures[i] < heures[j]:
                premier = i
                second = j

            elif heures[j] < heures[i]:
                premier = j
                second = i

            else:
                # Deux avions ne peuvent pas atterrir
                # exactement au même instant sur la même piste.
                return False

            # Récupérer la séparation directionnelle
            s = separation[(premier, second)]

            # Vérifier la séparation minimale
            if heures[second] < heures[premier] + s:
                return False

    return True



def verifier_faisabilite(avions, heures, pistes,
                         separation, nb_pistes):
    """
    Vérifie la faisabilité complète d'une solution ALP.

    Contraintes vérifiées :
      1. Chaque avion possède une heure d'atterrissage.
      2. Chaque avion est affecté à une piste valide.
      3. Les fenêtres de temps sont respectées.
      4. Les séparations de sécurité sont respectées.
    """

    # Vérifier que tous les avions ont une heure
    if set(heures.keys()) != set(avions.keys()):
        return False

    # Vérifier que tous les avions ont une piste
    if set(pistes.keys()) != set(avions.keys()):
        return False

    # Vérifier que les pistes sont valides
    for i in avions:
        if pistes[i] not in range(1, nb_pistes + 1):
            return False

    # Vérifier les fenêtres de temps
    if not verifier_fenetres(avions, heures):
        return False

    # Vérifier les séparations
    if not verifier_separations(
        avions, heures, pistes, separation
    ):
        return False

    return True
