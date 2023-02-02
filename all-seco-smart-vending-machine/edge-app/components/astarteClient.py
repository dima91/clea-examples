

from astarteClient import AstarteClient
from PySide6.QtCore import Signal

class AstarteClient() :

    # Defining emitted signals
    NewConnectionStatus = Signal (bool)
    

    def __init__(self, config, loop) -> None:
        # TODO Initializing Astarte object
        # TODO Registering interfaces
        # TODO Connecting Astarte client
        pass