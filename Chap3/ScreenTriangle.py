class ScreenTriangle:
    def __init__(self, v0, v1, v2):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
    
    def render(self):
        return [
            (int(self.v0[0]), int(self.v0[1])),
            (int(self.v1[0]), int(self.v1[1])),
            (int(self.v2[0]), int(self.v2[1]))
        ]