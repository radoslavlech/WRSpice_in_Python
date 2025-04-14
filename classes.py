import numpy as np
class Device:
    def __init__(self) -> None:
        self.fro = None
        self.to = None
        self.symbol = None
        self.type = None
        self.value = None
        self.no_subbranches = 1
        self.subbranch = 0

class JJ(Device):
    def __init__(self):
        super().__init__()
        self.junction_node = None

class Current_Source(Device):
    def __init__(self):
        super().__init__()
        self.current_type = None


class Node:
    def __init__(self) -> None:
        self.index = None
        self.fro = []
        self.to = []
        self.between= None
        self.pos = np.array([0.0, 0.0])