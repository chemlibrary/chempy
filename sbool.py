## Sticky booleans that can only be changed once.

class Sbool:
    def __init__(self, b:bool = True):
        self.__b = b
        self.__x = not(b)
    def __str__(self):
        return str(self.__b)
    def __repr__(self):
        return str(self.__b)
    def __bool__(self):
        return bool(self.__b)
    def __eq__(self, other):
        return self.__b == other
    def __ne__(self, other):
        return self.__b != other
    def value(self):
        return self.__b
    def locked(self) -> bool:
        return self.__b == self.__x
    def flip(self) -> bool:
        if not self.locked():
            self.__b = self.__x
            return True
        return False
    def set(self, target):
        if self.value() != target:
            self.flip()
        return self.value()
