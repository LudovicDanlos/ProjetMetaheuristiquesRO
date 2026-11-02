import re

avions = {
    1: {"E": 10, "T": 12, "L": 20},
    2: {"E": 11, "T": 14, "L": 22},
    3: {"E": 12, "T": 16, "L": 25},
}

separation = {
    (1, 2): 3,
    (1, 3): 3,
    (2, 3): 3,
}

nb_pistes = 2

def read_instance(filename, nb_pistes: int) -> dict:
    """Charge une instance 'airland' au format OPL (.dat).

    Si nb_pistes est None, on utilise la valeur m du fichier.
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
        "nb_pistes": nb_pistes if nb_pistes is not None else m,
    }


if __name__ == "__main__":
    inst = read_instance("data/airland1.dat", nb_pistes)
    print(inst["nb_pistes"], len(inst["avions"]))
    print(inst["avions"][1])
    print(inst["separation"][(1, 2)], inst["separation"][(1, 3)])
