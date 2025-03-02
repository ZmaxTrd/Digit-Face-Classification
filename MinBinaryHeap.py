from State import State

class MinBinaryHeap:
    def __init__(self, isLargerGFirst: bool):
        self.heap = [] 
        self.length = len(self.heap)
        self.isLargerGFirst = isLargerGFirst

    def size(self):
        return self.length

    def isEmpty(self):
        return self.length == 0

    def insert(self, state):
        """Insert an item into the heap and maintain heap order."""
        
        self.heap.append(state)
        self.length += 1
        self.heapUp(len(self.heap) - 1) 

    def pop(self):
        """Remove and return the state with the smallest f-value from the heap."""
        
        if self.isEmpty():
            return None

        self.swap(0, len(self.heap) - 1) 
        min_val = self.heap.pop()
        self.heapDown(0)
        self.length -= 1

        return min_val

    def remove(self, state):
        """Remove a specific state from the heap."""
        
        if self.heap.index(state) == 0:
            self.pop()
            self.length -= 1
            return True
        else:
            if self.length > 0:
                while state in self.heap:
                    i = self.heap.index(state)
                    self.swap(i, self.length - 1)
                    
                    del (self.heap[self.length - 1])
                    self.length -= 1
                    self.heapDown(i + 1)

        

    def peek(self):
    #"""Return the state with the smallest f-value without removing it."""
        if self.size() > 0:
            return self.heap[0]
        return None

    def heapUp(self, i):
        """Move a node up to maintain the heap property."""
        
        parent = (i - 1) // 2
        while i > 0 and self.compare(self.heap[i], self.heap[parent]):
            self.swap(i, parent)
            i = parent
            parent = (i - 1) // 2

    def heapDown(self, i):
        """Move a node down to maintain the heap"""
        
        n = len(self.heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i

            if left < n and self.compare(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < n and self.compare(self.heap[right], self.heap[smallest]):
                smallest = right

            if smallest == i:
                break

            self.swap(i, smallest)
            i = smallest

    def swap(self, i, j):
        """Swap two states in the heap."""
        
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def contains(self, state):
        """Check if a state exists in the heap."""
        
        return state in self.heap

    def compare(self, s1, s2):
        """
        Compare two states based on f-value.
        Tie-breaking is done using:
        - 999 * f - g (larger g first)
        - 999 * f + g (smaller g first)
        """
        
        if s1.f == s2.f:
            s1_priority = (999 * s1.f - s1.g) if self.isLargerGFirst else (999 * s1.f + s1.g)
            s2_priority = (999 * s2.f - s2.g) if self.isLargerGFirst else (999 * s2.f + s2.g)
            return s1_priority < s2_priority  #min-heap
        
        return s1.f < s2.f




def test_heap_with_tiebreaking():
    print("Testing MinBinaryHeap with tie-breaking...\n")

    use_larger_g = True  
    heap = MinBinaryHeap(use_larger_g)

    #10 test states
    states = [
        State(0, 0, False),  
        State(1, 1, False),  
        State(2, 2, False),  
        State(3, 3, False),  
        State(4, 4, False),  
        State(5, 5, False),  
        State(6, 6, False),  
        State(7, 7, False),  
        State(8, 8, False),  
        State(9, 9, False),  
    ]

    # Assign g, h vals
    g_h_values = [
        (1, 2), (2, 3), (2, 1), (5, 3), (3, 2),
        (4, 2), (2, 4), (7, 3), (4, 3), (3, 0)
    ]
    
    for state, (g, h) in zip(states, g_h_values):
        state.g = g
        state.h = h
        state.update()

    # Insert states into the heap
    print("Inserting states into heap...\n")
    for state in states:
        heap.insert(state)
        print(f"Inserted ({state.x}, {state.y}) with f = {state.f}, g = {state.g}, h = {state.h}")

    print("\nPopping states in order:")
    while not heap.isEmpty():
        state = heap.pop()
        print(f"Popped ({state.x}, {state.y}) with f = {state.f}, g = {state.g}, h = {state.h}")

    print("\nHeap test completed!")
    
if __name__ == '__main__':
    test_heap_with_tiebreaking()