import time


class Clock:
    start = time.time()

    def __init__(self, time=0, d_time=0):
        self._time = time
        self._d_time = d_time

    @property
    def time(self):
        return self._time

    @property
    def d_time(self):
        return self._d_time

    def update(self, d_time):
        """
        d_time in seconds
        """
        self._d_time = d_time
        self._time += d_time

    def __call__(self, *args, **kwargs):
        return self._time, self._d_time

    def reload(self):
        self._d_time = self._time = 0

    def set_time(self, time, d_time=0.00000001):
        self._time, self._d_time = time, d_time

    @property
    def timer_format(self):
        minute = str(abs(self._time) // 60).split('.')[0]
        sec = str(abs(self._time) % 60).split('.')[0]

        return f"{minute if abs(int(minute)) > 9 else f'0{minute}'}:{sec if abs(int(sec)) > 9 else f'0{sec}'}"


GLOBAL_CLOCK = Clock()
ROUND_CLOCK = Clock()
