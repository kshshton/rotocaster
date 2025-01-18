
class VerticalPosition:
    def __init__(self, rely, rely_diff):
        self.rely = rely
        self.rely_diff = rely_diff
        self.position = 0

    def __next__(self) -> float:
        self.position += 1
        return self.rely + self.rely_diff * self.position + (self.rely_diff / 1.5)
