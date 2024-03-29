import time

class mytimer:
    def __init__(self) -> None:
        self.start = time.time()

    @property 
    def get(self) -> str:
        delta: float = round(time.time()- self.start, 2)
        self.start = time.time()
        return str(delta)
