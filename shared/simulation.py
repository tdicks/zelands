from twisted.internet.task import LoopingCall, Clock

class SimulationTime(Clock):
    _call = None

    def __init__(self, granularity, platform_clock):
        Clock.__init__(self)
        self.granularity = granularity
        self.platform_clock = platform_clock

    def _update(self, frames):
        self.advance(1.0 * frames / self.granularity)

    def start(self):
        self._call = LoopingCall.withCount(self._update)
        self._call.clock = self.platform_clock
        self._call.start(1.0 / self.granularity, now=False)

    def stop(self):
        self._call.stop()