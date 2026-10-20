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

def read_instance(filename):
    # TODO : charge les vrai données depuis les fichier .dat
    return {
        "avions": avions,
        "separation": separation,
        "nb_pistes": nb_pistes,
    }
