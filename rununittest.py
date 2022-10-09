import unittest
import numpy as np

from iir_filter import IIR_filter
from scipy import signal


class TestIIRFilter(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

        sr = 15     # sampling rate
        cutoff = 5  # cutoff frequency
        sos = signal.butter(2, cutoff/sr*2, 'lowpass', output = 'sos')
        self.filter = IIR_filter(sos)

    def test_filter(self):
        _in = np.loadtxt("assets/test_data.dat")
        expected_out = np.loadtxt("assets/test_out.dat")

        out = []
        for num in _in:
            out.append(self.filter.filter(num))
        
        self.assertEqual(len(out), len(expected_out))
        for i in range(len(out)):
            self.assertEqual(out[i], expected_out[i])


if __name__ == "__main__":
    unittest.main()