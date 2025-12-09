import numpy as np
from fuzzification import fuzzify


def infer(plant_height, lamp_distance, domains, mf, rules):
    xh = domains["height"]
    xd = domains["distance"]
    xo = domains["output"]

    μh = {k: fuzzify(plant_height, xh, v) for k, v in mf["height"].items()}
    μd = {k: fuzzify(lamp_distance, xd, v) for k, v in mf["distance"].items()}

    agg_u = np.zeros_like(xo)
    agg_l = np.zeros_like(xo)

    for h, d, out in rules:
        strength = min(μh[h], μd[d])
        u, l = mf["output"][out]
        agg_u = np.fmax(agg_u, np.fmin(strength, u))
        agg_l = np.fmax(agg_l, np.fmin(strength, l))

    return agg_u, agg_l
