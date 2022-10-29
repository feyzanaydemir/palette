class Color:
    def __init__(self, rgb=None, hex=None, name=None, weight=0, percentage=0):
        self.rgb = rgb
        self.hex = hex
        self.name = name
        self.weight = weight
        self.percentage = percentage
        self.isMerged = False

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        percentage = "{:.2f}".format(self.percentage)
        return f"(rgb: {self.rgb}, hex: {self.hex}, percentage: {percentage}, name: {self.name})"
