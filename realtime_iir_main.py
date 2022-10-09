#!/usr/bin/python3

import sys
from pyfirmata2 import Arduino
from PyQt5.QtWidgets import QApplication
from threading import Thread

from AnalogPrinter import AnalogPrinter
from MainWindow import ControlWidget
from QtPanningPlot import QtPanningPlot
from Encoder import Encoder
from Decoder import Decoder


RED_PIN = 9
BLUE_PIN = 10
GREEN_PIN = 11

PORT = Arduino.AUTODETECT
board = Arduino(PORT)
app = QApplication(sys.argv)
# signals to all threads in endless loops that we'd like to run these
running = True

originalPlot = QtPanningPlot("Original Signal")
filteredPlot = QtPanningPlot("Filtered Signal")

# get pins of the LED light
red = board.get_pin(f"d:{RED_PIN}:p")
blue = board.get_pin(f"d:{BLUE_PIN}:p")
green = board.get_pin(f"d:{GREEN_PIN}:p")

encoder = Encoder(red, green, blue)
mainWindow = ControlWidget(board, encoder)
decoder = Decoder()
analogPrinter = AnalogPrinter(board, originalPlot, filteredPlot, decoder)

decoder.register_on_decode_end(mainWindow.output_to_logbox)

analogPrinter.start()
mainWindow.show()

app.exec_()

running = False
app.exit()
board.exit()
