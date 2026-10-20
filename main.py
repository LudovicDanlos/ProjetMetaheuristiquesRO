import instance
import evaluation
import feasibility
import constructive

# Ouverture des données de l'instance
data = instance.read_instance("instance.dat")

# Calcul de la solution selon l'algorithme choisi
solution = constructive.construire_solution(data["avions"], data["separation"], data["nb_pistes"])
pistes, heures = solution

# Vérification de la faisabilité de la solution
if not feasibility.verifier_fenetres(data["avions"], heures):
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