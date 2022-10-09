import time
from iir_filter import IIR_filter
from scipy import signal

from Decoder import Decoder

class AnalogPrinter:

    def __init__(self, board, original_signal_plot, filtered_signal_plot, decoder: Decoder):
        # sampling rate: 1000Hz
        self.samplingRate = 1000
        self.timestamp = 0
        self.board = board
        
        # bind output plot
        self.original_signal_plot = original_signal_plot
        self.filtered_signal_plot = filtered_signal_plot

        # bind decoder
        self.decoder = decoder

        # cut off frequency: 50Hz
        cut_off = 50
        sos = signal.butter(2, cut_off/self.samplingRate*2, 'lowpass', output = 'sos')
        self.iir = IIR_filter(sos)

    def start(self):
        self.board.analog[0].register_callback(self.callback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[0].enable_reporting()

    def callback(self, data):
        now = time.time()
        filtered_data = self.iir.filter(data)

        self.original_signal_plot.addData(data, now)
        self.filtered_signal_plot.addData(filtered_data, now)
        self.decoder.decode(filtered_data)
