"""Top-level package for montecarlo."""

# import numpy as np
import numpy as np
from . bitstring import BitString
from . isinghamiltonian import IsingHamiltonian

class MonteCarlo:
    def __init__(self, ham: IsingHamiltonian):
        self.ham = ham

    def getRandConfig(self):
        num = np.random.rand() * pow(2, len(self.ham.mus))
        config = BitString(len(self.ham.mus))
        config.set_integer_config(num)
        return config

    def run(self, T: float, n_samples: int, n_burn: int):
        b = 1.0 / T
        E = []
        M = []
        alpha = BitString(len(self.ham.mus))

        for i in range(n_samples):
            beta = self.getRandConfig()
            eChange = self.ham.energy(beta) - self.ham.energy(alpha)
            if (eChange <= 0):
                alpha = beta
            else:
                prob = np.exp(-b * (eChange))
                r = np.random.rand()
                if (prob > r):
                    alpha = beta
            if (i >= n_burn):
                E.append(self.ham.energy(alpha))
                M.append(alpha.on()-alpha.off())

        return E, M