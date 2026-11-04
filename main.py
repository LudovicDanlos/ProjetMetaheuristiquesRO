import instance
import evaluation
import feasibility
import constructive

# Ouverture des données de l'instance
data = instance.read_instance("data/airland1.dat")

# Calcul de la solution selon l'algorithme choisi
solution = constructive.construire_solution(data["avions"], data["separation"], data["nb_pistes"])
if solution is None:
    raise SystemExit("Aucune solution faisable n'a été trouvée.")

pistes, heures = solution
affectations = {
    avion: numero_piste
    for numero_piste, piste in enumerate(pistes, start=1)
    for avion in piste
}

# Vérification de la faisabilité de la solution
if not feasibility.verifier_faisabilite(
    data["avions"], heures, affectations, data["separation"], data["nb_pistes"]
):
    print("La solution n'est pas faisable.")
else:
    print("La solution est faisable.")

# Calcul du coût de la solution
cost = evaluation.cout_p2(heures)
print(f"Le coût de la solution est : {cost}")

# Affichage de la solution
print("-" * 20)
for r, piste in enumerate(pistes):
    print(f"Piste {r + 1}: {piste}")