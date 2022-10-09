## Zero-One Sequence Transmission based on LDR

File Structure

    - assets\
      |- test_data.dat          test data
      |- test_out.dat           expected output of test data
    - AnalogPrinter.py          class to print analog signal(original and filtered)
    - Decoder.py                class to handle the environment light level change and decode the received signals to 0-1 sequence. 
    - Encoder.py                class to control the LED light to emit signal representing zero, one, or control
    - iir_filter.py             class of IIR filter
    - MainWindow.py             window of the encoder input
    - QtPanningPlot.py          window to plot analog signal
    - realtime_iir_main.py      program entrance
    - rununittest.py            unit test of iir_filter.py


Youtube Clip: https://youtu.be/6JyAdl4u0hc