from . bitstring import BitString
import numpy as np

class IsingHamiltonian:
    def __init__(self, G):
        self.G = G
        self.mus = None

    def energy(self, bs: BitString):
        spins = []
        for val in bs.config:
            if val == 0:
                spins.append(-1)
            else:
                spins.append(1)

        E = 0.0

        for edge in self.G.edges:
            weight = self.G.edges[edge]['weight']
            E += (weight * spins[edge[0]] * spins[edge[1]])

        if (self.mus is not None):
            for i in range(len(spins)):
                weight = spins[i] * self.mus[i]
                E += weight

        return E

    def set_mu(self, mus: np.ndarray):
        self.mus = mus
    
    def compute_average_values(self, T: float):

        bs = BitString(6)

        M  = 0.0
        Z  = 0.0
        EE = 0.0
        MM = 0.0

        # Write your function here!
        beta = 1.0 / T

        energies = np.array([], dtype=np.float128)
        magnetism = np.array([], dtype=np.int32)
        for i in range(0, pow(2, bs.__len__())):
            bs.set_integer_config(i)
            energies = np.append(energies, self.energy(bs))
            magnetism = np.append(magnetism, (bs.on() - bs.off()))
        shiftedWeights = energies * -beta
        shiftedWeights = shiftedWeights - np.max(shiftedWeights)
        Z = np.sum(np.exp(shiftedWeights))

        probabilities = np.exp(shiftedWeights) / Z

        E = np.sum(energies*probabilities)
        EE = np.sum(np.pow(energies, 2)*probabilities)
        M = np.sum(magnetism * probabilities)
        MM = np.sum(np.pow(magnetism, 2)*probabilities)
        HC = (EE - pow(E, 2))*pow(T, -2)
        MS = (MM - pow(M, 2))*pow(T, -1)
        
        return E, M, HC, MS