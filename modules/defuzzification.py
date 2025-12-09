import numpy as np


def defuzz(x, upper, lower):
    try:
        cu = np.sum(x * upper) / np.sum(upper)
        cl = np.sum(x * lower) / np.sum(lower)
        return (cu + cl) / 2
    except ZeroDivisionError:
        return 0
