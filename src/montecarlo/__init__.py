"""Top-level package for montecarlo."""

# import numpy as np
import numpy as np

class BitString:
    """
    Simple class to implement a config of bits
    """
    def __init__(self, N):
        self.N = N
        self.config = np.zeros(N, dtype=int) 

    def __repr__(self):
        out = ""
        for i in self.config:
            out += str(i)
        return out

    def __eq__(self, other):        
        returnVal = True
        if self.config != other.config:
            returnVal = False
        if self.integer() != other.integer():
            returnVal = False
        if len(self) != len(other):
            returnVal = False
        return returnVal
    
    def __len__(self):
        return len(self.config)

    def on(self):
        """
        Return number of bits that are on
        """
        count = 0
        for i in self.config:
            if i == 1:
                count += 1
        return count

    def off(self):
        """
        Return number of bits that are off
        """
        count = 0
        for i in self.config:
            if i == 0:
                count += 1
        return count

    def flip_site(self,i):
        """
        Flip the bit at site i
        """
        if self.config[i] == 0:
            self.config[i] = 1
        else:
            self.config[i] = 0
    
    def integer(self):
        """
        Return the decimal integer corresponding to BitString
        """
        number = 0
        for i in range(len(self.config)):
            if self.config[len(self.config)-1-i] == 1:
                exponent = i
                number += pow(2, exponent)
        return number
 

    def set_config(self, s:list[int]):
        """
        Set the config from a list of integers
        """
        self.config = s

    def set_integer_config(self, dec:int, digits=None):
        """
        convert a decimal integer to binary
    
        Parameters
        ----------
        dec    : int
            input integer
            
        Returns
        -------
        Bitconfig
        """
        if (digits != None):
            self.config = np.zeros(digits, dtype=int) 
        binary = []
        while (dec > 0):
            remainder = dec%2
            binary.insert(0, remainder)
            dec = dec // 2

        while len(binary) < len(self.config):
            binary.insert(0, 0)
            
        self.config = binary




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
    

class MonteCarlo:
    def __init__(self, ham: IsingHamiltonian):
        self.ham = ham