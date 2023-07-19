
class MinHeap:

    def __init__(self):
        self.maxSize = 10000
        self.heap = [0]*10000
        self.currentSize = 0

    def heappush(self, element):
        # if array is filled then double it
        if self.currentSize == self.maxSize:
            for _ in range(self.maxSize):
                self.heap.append(0)
            self.maxSize += self.maxSize
        
        # first element can be pushed on without need to sift
        if self.currentSize == 0:
            self.heap[0] = element
            self.currentSize += 1
            return
        
        # insert new element at the last index
        self.heap[self.currentSize] = element
        i = self.currentSize
        self.currentSize += 1

        # sift up
        while self.isSmaller(i, self.parent(i)):
            self.swap(i, self.parent(i))
            i = self.parent(i)

            # if element is at the top, break out of while loop
            if i == 0:
                break
        
        return
    
    def heappop(self):
        if self.currentSize == 0:
            return
        
        if self.currentSize == 1:
            self.currentSize -= 1
            return self.heap[0]
        
        if self.currentSize == 2:
            minValue = self.heap[0]
            self.heap[0] = self.heap[1]
            self.currentSize -= 1
            return minValue
            
        
        minValue = self.heap[0]

        # place last element on top
        self.heap[0] = self.heap[self.currentSize-1]
        self.currentSize -= 1
        i = 0

        # sift down
        while not (self.isSmaller(i, self.left_child(i)) and self.isSmaller(i, self.right_child(i))):

            if self.isSmaller(self.left_child(i), self.right_child(i)):
                self.swap(i, self.left_child(i))
                i = self.left_child(i)
            else:
                self.swap(i, self.right_child(i))
                i = self.right_child(i)

            if self.right_child(i) >= self.currentSize:
                break

        # handle case where left child exists but not right child - may need one additional sift down
        if self.left_child(i) < self.currentSize:
            if self.isSmaller(self.left_child(i), i):
                self.swap(i, self.left_child(i))

        return minValue

    
    # checks if element at index 1 is smaller than element at index 2
    # designed to work with our A* imeplementation (uses f-value first, then g-value, then third tiebreaker value)
    def isSmaller(self, index1, index2):
        # compare first values
        if self.heap[index1][0] < self.heap[index2][0]:
            return True
        elif self.heap[index1][0] > self.heap[index2][0]:
            return False
        else:
            # if first values are same, look at second values
            if self.heap[index1][1] < self.heap[index2][1]:
                return True
            elif self.heap[index1][1] > self.heap[index2][1]:
                return False
            else:
                # if second values are same, look at third values
                if self.heap[index1][2] < self.heap[index2][2]:
                    return True
                elif self.heap[index1][2] > self.heap[index2][2]:
                    return False
                else:
                    # if third values are same, just return false
                    return False
                
    # helper function to swap values at two given indices
    def swap(self, index1, index2):
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp
        return

    def parent(self, index):
        return (index-1) // 2

    def left_child(self, index):
        return (2*index) + 1

    def right_child(self, index):
        return (2*index) + 2
    
    def length(self):
        return self.currentSize
    
    def print(self):
        for i in range(self.currentSize):
            print(str(self.heap[i]), end=" ")
        print("")

'''
if __name__ == "__main__":
    heap = MinHeap()
    heap.heappush((100, 0, 0))
    print(heap.heappop())
    heap.heappush((100, 0, 0))
    heap.heappush((10, 0, 0))
    heap.heappush((150, 0, 0))
    heap.heappush((80, 0, 0))
    heap.heappush((1, 0, 0))
    heap.print()
    print(heap.heappop())
    heap.print()
'''

