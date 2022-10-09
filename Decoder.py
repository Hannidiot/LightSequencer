import numpy as np

class Decoder:
    def __init__(self, buffer_size = 500, log_func = print, level_step = 0.003, deviation_tolerance = 0.01,
            time_offset = 13, init_duration = 200, one_duration = 100, zero_duration = 50):
        self.buffer = []
        self.env_level = 0
        self.level_step = level_step
        self.buffer_size = buffer_size
        self.log = log_func
        self.deviation_tolerance = deviation_tolerance

        self.buffer_sum = 0
        self.buffer_avg = 0
        self.ctr = 0

        self.status = "IDLE"
        self.last_active = 0
        self.output = ""

        # callback functions
        self._on_decode_start = []
        self.on_decode_end = []

        # for detecting high voltage value
        self.high_vol_avg = 0
        self.stop_ctr = 0
        self.high_vol_ctr = 0
        self.high_vol = 0

        # decoding according to signal duration
        self.time_offset = time_offset
        self.init_duration = init_duration
        self.one_duration = one_duration
        self.zero_duration = zero_duration

    def _detect_environment_level_change(self, data, data_to_process):
        if data_to_process == -1:
            self.buffer_sum += data
        else:
            self.buffer_sum = self.buffer_sum + data - data_to_process
        self.buffer_avg = self.buffer_sum / len(self.buffer)
        
        if data_to_process == -1:
            return

        # calculate deviation
        buffer_deviation = 0
        for num in self.buffer:
            buffer_deviation += abs(num - self.buffer_avg)
        buffer_deviation /= self.buffer_size

        # determine whether env level changes
        if buffer_deviation < self.deviation_tolerance and abs(self.buffer_avg - self.env_level) > self.level_step:
            self.env_level = self.buffer_avg
            self.log(f"env level changes to: {self.env_level}")

    def _switch_to(self, to_status):
        if to_status == "IDLE":
            self.status = to_status
            for func in self.on_decode_end:
                func(self.output)
            print(self.output)
            self.output = ""
        elif to_status == "RUNNING":
            self.status = to_status
            for func in self._on_decode_start:
                func()
            self.last_active = self.ctr

    def register_on_decode_start(self, func):
        self._on_decode_start.append(func)

    def register_on_decode_end(self, func):
        self.on_decode_end.append(func)

    def decode(self, data):
        data_to_process = self._add(data)
        self.ctr += 1
        self._detect_environment_level_change(data, data_to_process)

        # jump out if no data to process
        if data_to_process == -1:
            return

        self._decode(data_to_process)

    def _decode(self, data):
        if self.status == "IDLE":
            level, duration = self._detect_continuous_signal(data)
            if (level, duration) != (-1, -1) and abs(duration - self.init_duration) < self.time_offset:
                self.high_vol = level
                self._switch_to("RUNNING")
        elif self.status == "RUNNING":
            if self.ctr - self.last_active >= 2000:
                self.log("decoding timeout, switching to IDLE")
                self._switch_to("IDLE")

            level, duration = self._detect_continuous_signal(data)
            if (level, duration) != (-1, -1) and abs(level - self.high_vol) < self.deviation_tolerance:
                self.last_active = self.ctr
                if abs(duration - self.one_duration) < self.time_offset:
                    self.output += "1"
                elif abs(duration - self.zero_duration) < self.time_offset:
                    self.output += "0"
                elif abs(duration - self.init_duration) < self.time_offset:
                    self._switch_to("IDLE")

    def _detect_continuous_signal(self, data):
        if abs(data - self.env_level) < self.deviation_tolerance:
            return -1, -1

        if abs(data - self.high_vol_avg) > self.deviation_tolerance:
            if self.high_vol_ctr >= 10:
                self.stop_ctr += 1
            else:
                self.high_vol_avg = data
                self.high_vol_ctr = 1
        else:
            self.high_vol_avg = ((self.high_vol_avg * self.high_vol_ctr) + data) / (self.high_vol_ctr + 1)
            self.high_vol_ctr += 1
        
        if self.stop_ctr >= 3:
            h = self.high_vol_ctr
            self.high_vol_ctr = 0
            self.stop_ctr = 0
            return self.high_vol_avg, h
        
        return -1, -1

    def _add(self, data):
        """
        add the data into buffer, and throw the first value into the decoder if len(buffer) > buffer_size
        """
        self.buffer.append(data)

        if len(self.buffer) > self.buffer_size:
            return self.buffer.pop(0)
        return -1
