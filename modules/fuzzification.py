import numpy as np


def fuzzify(value, x, mf):
    upper = np.interp(value, x, mf[0])
    lower = np.interp(value, x, mf[1])
    return (upper + lower) / 2
