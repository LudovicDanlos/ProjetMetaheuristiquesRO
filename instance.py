import re

def read_instance(filename) -> dict:
    """Charge une instance 'airland' au format OPL (.dat).

    Returns :
        Un dictionnaire contenant 3 couples clés-valeurs :
            - Clef 'avions' --> sa valeur est un sous-dictionnaire ayant pour clés des chiffres (en string) qui correspondent chacun à un
            avion particulier. A chaque chiffre est associé un sous-dictionnaire contenant les données de l'avions à prendre en compte.
            - Clef 'separation' --> sa valeur est un sous-dictionnaire ayant pour clés des couples (type tuple) d'entiers, chaque entier
            représentant un avion particulier du dictionnaire associé à la clé 'avions'. A chaque couple d'entier est associé un entier
            pour valeurs. Cet entier est le temps de séparation minimum nécessaire entre les temps d'atterrissages des avions identifiés
            par chaque entier du couple d'entiers.
            - Clef 'nb_pistes' --> sa valeur est un entier qui représente le nombre de pistes considéré.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    def get_scalar(name):
        match = re.search(rf'\b{name}\s*=\s*(\d+)\s*;', content)
        if match is None:
            raise ValueError(f"Paramètre '{name}' introuvable dans {filename}")
        return int(match.group(1))

    def get_vector(name):
        match = re.search(rf'\b{name}\s*=\s*\[([^\[\]]*)\]\s*;', content)
        if match is None:
            raise ValueError(f"Vecteur '{name}' introuvable dans {filename}")
        return [float(x) for x in match.group(1).replace('\n', ' ').split(',') if x.strip()]

    def get_matrix(name):
        match = re.search(rf'\b{name}\s*=\s*\[(.*?)\]\s*;', content, re.DOTALL)
        if match is None:
            raise ValueError(f"Matrice '{name}' introuvable dans {filename}")
        rows = re.findall(r'\[([^\[\]]*)\]', match.group(1))
        return [[float(x) for x in row.split(',') if x.strip()] for row in rows]

    p = get_scalar('p')
    m = get_scalar('m')
    E = get_vector('E')
    T = get_vector('T')
    L = get_vector('L')
    cminus = get_vector('cminus')
    cplus = get_vector('cplus')
    s = get_matrix('s')

    assert len(E) == len(T) == len(L) == len(cminus) == len(cplus) == p, \
        "Les vecteurs ne font pas la taille p"
    assert len(s) == p and all(len(row) == p for row in s), \
        "La matrice de séparation n'est pas p x p"

    # Avions numérotés de 1 à p, comme dans ton exemple
    avions = {
        i + 1: {
            "E": int(E[i]),
            "T": int(T[i]),
            "L": int(L[i]),
            "cminus": cminus[i],   # pénalité par unité d'avance sur T
            "cplus": cplus[i],     # pénalité par unité de retard sur T
        }
        for i in range(p)
    }

    # Séparation pour toutes les paires ordonnées (i, j), i != j
    # (la diagonale 99999 est ignorée ; la matrice peut être asymétrique)
    separation = {
        (i + 1, j + 1): int(s[i][j])
        for i in range(p)
        for j in range(p)
        if i != j
    }

    return {
        "avions": avions,
        "separation": separation,
        "nb_pistes": m,
    }


if __name__ == "__main__":
    inst = read_instance("data/airland1.dat")
    print(inst["avions"])
    print(inst["separation"])
    print(inst["nb_pistes"])
