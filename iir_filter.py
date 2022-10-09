#
# (C) 2020 Bernd Porr, mail@berndporr.me.uk
# Apache 2.0 license
#
import numpy as np

class IIR2_filter:
    """2nd order IIR filter"""

    def __init__(self,s):
        """Instantiates a 2nd order IIR filter
        s -- numerator and denominator coefficients
        """
        self.numerator0 = s[0]
        self.numerator1 = s[1]
        self.numerator2 = s[2]
        self.denominator1 = s[4]
        self.denominator2 = s[5]
        self.buffer1 = 0
        self.buffer2 = 0

    def filter(self,v):
        """Sample by sample filtering
        v -- scalar sample
        returns filtered sample
        """
        input = v - (self.denominator1 * self.buffer1) - (self.denominator2 * self.buffer2)
        output = (self.numerator1 * self.buffer1) + (self.numerator2 * self.buffer2) + input * self.numerator0
        self.buffer2 = self.buffer1
        self.buffer1 = input
        return output

class IIR_filter:
    """IIR filter"""
    def __init__(self,sos):
        """Instantiates an IIR filter of any order
        sos -- array of 2nd order IIR filter coefficients
        """
        self.cascade = []
        for s in sos:
            self.cascade.append(IIR2_filter(s))

    def filter(self,v):
        """Sample by sample filtering
        v -- scalar sample
        returns filtered sample
        """
        for f in self.cascade:
            v = f.filter(v)
        return v


if __name__ == "__main__":
    from scipy import signal
    sr = 15
    cutoff = 5
    num_str = """
    0.2102
    0.2102
    0.2102
    0.2092
    0.2092
    0.2072
    0.2063
    0.2053
    0.2033
    0.1994
    0.1935
    0.1896
    0.1935
    0.2004
    0.2014
    0.2043
    0.2072
    0.2092
    0.2102
    0.2053
    0.1975
    0.1926
    0.1906
    0.1955
    0.2014
    0.2053
    0.2082
    0.2102
    0.2102
    0.2033
    0.1955
    0.1906
    0.1906
    0.1975
    0.2023
    0.2063
    0.2082
    0.2102
    0.2082
    0.2004
    0.1945
    0.1896
    0.1926
    0.1994
    0.2033
    0.2072
    0.2092
    0.2102
    0.2072
    0.1984
    """
    nums = [float(item.strip()) for item in num_str.strip().strip("\n").split("\n")]

    sos = signal.butter(2, cutoff/sr*2, 'lowpass', output = 'sos')
    iir = IIR_filter(sos)

    for num in nums:
        print(iir.filter(num))
