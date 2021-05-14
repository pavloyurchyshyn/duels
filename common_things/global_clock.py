class Clock:
    def __init__(self, time=0, d_time=0):
        self._time = time
        self._d_time = d_time

    @property
    def time(self):
        return self._time

    @property
    def d_time(self):
        return self._time

    def update(self, d_time):
        self._d_time = d_time
        self._time += d_time

    def __call__(self, *args, **kwargs):
        return self._time, self._d_time

    def reload(self):
        self._d_time = self._time = 0

    def set_time(self, time, d_time):
        self._time, self._d_time = time, d_time


GLOBAL_CLOCK = Clock()
ROUND_CLOCK = Clock()