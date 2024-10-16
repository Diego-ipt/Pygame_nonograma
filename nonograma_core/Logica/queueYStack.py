from collections import deque

class Queue:
    def __init__(self):
        self._elements = deque()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        if(len(self._elements) >= 1):
            return self._elements.popleft()
    
    def size(self):
        return len(self._elements)
    

class Stack:
    def __init__(self):
        self._elements = deque()
    
    def push(self, element):
        self._elements.append(element)

    def pop(self):
        if(len(self._elements) >= 1):
            return self._elements.pop()
    
    def size(self):
        return len(self._elements)
    