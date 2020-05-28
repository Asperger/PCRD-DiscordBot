from time import clock

class reserved:
    def __init__(self, id, cmt, time=0):
        self.time = time + clock()
        self.id = id
        self.comment = cmt

    def __str__(self):
        return f"{self.id} {self.comment} {self.time})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, '{self.comment}', {self.time})"

    def __lt__(self, other):
        return self.time < other.time
