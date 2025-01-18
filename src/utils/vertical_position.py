
class VerticalPosition:
    def __init__(self, rely: float, rely_diff: float) -> None:
        self.rely: float = rely
        self.rely_diff: float = rely_diff
        self.position: int = 0

    def __next__(self) -> float:
        self.position += 1
        return self.rely + self.rely_diff * self.position + (self.rely_diff / 1.5)
