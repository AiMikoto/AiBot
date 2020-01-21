class TooManyValues(Exception):
    pass

class NotAnInteger(Exception):
    pass

class ValueOutsideOfScope(Exception):
    def __init__(self, value):
        self.value = value

class StandardException(Exception):
    def __init__(self, value):
        self.value = value    