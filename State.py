"""State class"""
class State:
    def __init__(self, x, y, isBlocked):
        self.x = x
        self.y = y
        self.isBlocked = isBlocked 
        self.isObserved = False 
        
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        
        self.pointer = None
        self.search = 0
        
    def update(self):
        self.f = self.g + self.h
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    
    
    
    
    