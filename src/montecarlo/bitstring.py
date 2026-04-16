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