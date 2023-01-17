class Letter:
    def __init__(self, string):
        self.value = string

    def __eq__(self, other):
        return self.value == other.value

class Phoneme:
    def __init__(self, string, stressed=False):
        self.value = string
        self.stressed = stressed

    def __eq__(self, other):
        return self.value == other.value and self.stressed == other.stressed

    def is_vowel(self):
        for char in ["a", "e", "i", "o", "u", "y"]:
            if char in self.value:
                return True
        return False
