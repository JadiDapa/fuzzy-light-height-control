import numpy as np


def gaussian_t2(x, mean, sigma_upper, sigma_lower):
    upper = np.exp(-0.5 * ((x - mean) / sigma_upper) ** 2)
    lower = np.exp(-0.5 * ((x - mean) / sigma_lower) ** 2)
    return upper, lower


def build_memberships(domains):
    x_height = domains["height"]
    x_distance = domains["distance"]
    x_output = domains["output"]

    return {
        "height": {
            "semai": gaussian_t2(x_height, 8, 4, 2),
            "vegetatif": gaussian_t2(x_height, 30, 6, 3),
            "generatif": gaussian_t2(x_height, 60, 6, 3),
            "produktif": gaussian_t2(x_height, 90, 6, 3),
        },
        "distance": {
            "sangat_dekat": gaussian_t2(x_distance, 5, 3, 1.5),
            "dekat": gaussian_t2(x_distance, 15, 5, 3),
            "sedang": gaussian_t2(x_distance, 30, 6, 3),
            "jauh": gaussian_t2(x_distance, 50, 7, 4),
            "sangat_jauh": gaussian_t2(x_distance, 80, 7, 4),
        },
        "output": {
            "turun_banyak": gaussian_t2(x_output, -30, 6, 3),
            "turun_sedikit": gaussian_t2(x_output, -15, 5, 2),
            "diam": gaussian_t2(x_output, 0, 4, 2),
            "naik_sedikit": gaussian_t2(x_output, 15, 5, 2),
            "naik_banyak": gaussian_t2(x_output, 30, 6, 3),
        },
    }
