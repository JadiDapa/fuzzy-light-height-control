import numpy as np


def create_domains():
    return {
        "height": np.linspace(0, 110, 300),
        "distance": np.linspace(0, 100, 300),
        "output": np.linspace(-50, 50, 300),
    }
