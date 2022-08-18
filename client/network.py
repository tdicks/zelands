from twisted.protocols.amp import(
    AMP, Command, Integer, Float, Argument
)

class NetworkController(AMP):

    environment = None

    def __init__(self, clock):
        self.modelObjects = {}
        self.clock = clock

    