class Flag:
    def __init__(self, number, value):
        self.id = number
        self.value = value

    def set(self, value):
        self.value = value

    def get(self, value):
        return self.value
