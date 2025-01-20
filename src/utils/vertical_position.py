
class VerticalPosition:
    def __init__(self, rely: float, rely_padding: float) -> None:
        self.rely: float = rely
        self.rely_padding: float = rely_padding
        self.position: int = 0

    def __next__(self) -> float:
        self.position += 1
        return self.rely + self.position * self.rely_padding
