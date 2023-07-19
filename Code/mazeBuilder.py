'''
THIS CODE IS PULLED FROM THE FOLLOWING EDUCATIONAL ARTICLE ON GENERATING MAZES IN PYTHON USING PRIM'S ALGORITHM:
https://edtg.co.uk/2020/04/16/procedural-maze-generator-using-python/
'''

import random
import math

class Generator(object):

    def __init__(self, startx, starty, sizex = 10, sizey = 10):
        self.Grid = [[0 for i in range(sizex)] for j in range(sizey)]
        self.Grid[starty][startx] = 1
        self.Frontier = []
        self.sizex = sizex
        self.sizey = sizey

        Pathways = 0
        self.CalculateFrontier(startx, starty)
        while (len(self.Frontier) > 0):
            self.Expand()
        
        self.AddLoops(math.floor(math.sqrt(sizex*sizey)-1/2))

    def SetGridValue(self, x, y, Value):
        self.Grid[y][x] = Value

    def GetGridValue(self, x, y):
        return self.Grid[y][x]

    def CalculateFrontier(self, x, y):
        if (x >= 0 and x <= self.sizex-1 and y >= 0 and y <= self.sizey-1):
            if (x - 2 >= 0 and x - 2 <= self.sizex-1 and self.Grid[y][x-2] != 1):
                if (not [x-2, y] in self.Frontier):
                    self.Frontier.append([x-2, y])

            if (x + 2 >= 0 and x + 2 <= self.sizex-1 and self.Grid[y][x+2] != 1):
                if (not [x+2, y] in self.Frontier):
                    self.Frontier.append([x+2, y])

            if (y - 2 >= 0 and y - 2 <= self.sizey-1 and self.Grid[y-2][x] != 1):
                if (not [x, y-2] in self.Frontier):
                    self.Frontier.append([x, y-2])

            if (y + 2 >= 0 and y + 2 <= self.sizey-1 and self.Grid[y+2][x] != 1):
                if (not [x, y+2] in self.Frontier):
                    self.Frontier.append([x, y+2])

    def GetNeighbors(self, x, y):
        Neighbors = []
        if (x >= 0 and x <= self.sizex-1 and y >= 0 and y <= self.sizey-1):
            if (x-2 >= 0):
                if (self.Grid[y][x-2] == 1):
                    Neighbors.append([x-2, y])
            if (x+2 <= self.sizex-1):
                if (self.Grid[y][x+2] == 1):
                    Neighbors.append([x+2, y])
            if (y-2 >= 0):
                if (self.Grid[y-2][x] == 1):
                    Neighbors.append([x, y-2])
            if (y+2 <= self.sizey-1):
                if (self.Grid[y+2][x] == 1):
                    Neighbors.append([x, y+2])
        return Neighbors

    def GetDirectNeighbors(self, x, y):
        Neighbors = []
        if (x >= 0 and x <= len(self.Grid)-1 and y >= 0 and y <= len(self.Grid)-1):
            if (x-1 >= 0):
                if (self.Grid[y][x-1] == 1):
                    Neighbors.append([x-1, y])
            if (x+1 <= len(self.Grid)-1):
                if (self.Grid[y][x+1] == 1):
                    Neighbors.append([x+1, y])
            if (y-1 >= 0):
                if (self.Grid[y-1][x] == 1):
                    Neighbors.append([x, y-1])
            if (y+1 <= len(self.Grid)-1):
                if (self.Grid[y+1][x] == 1):
                    Neighbors.append([x, y+1])
        return Neighbors

    def Expand(self):
        FrontierIndex = random.randint(0, len(self.Frontier)-1)
        FE = self.Frontier[FrontierIndex]
        Neighbors = self.GetNeighbors(FE[0], FE[1])
        NeighborIndex = random.randint(0, len(Neighbors)-1)

        Mid = self.Mid(FE, Neighbors[NeighborIndex])
        x = Mid[0]
        y = Mid[1]

        self.Grid[FE[1]][FE[0]] = 1
        self.Grid[y][x] = 1

        self.Frontier.remove(FE)
        self.CalculateFrontier(FE[0], FE[1])

    def AddLoops(self, NumLoops):
        for i in range(NumLoops):
            # Get a random point and one of it's neighbors
            p1 = [round(random.randint(0, self.sizex-1)/2)*2, round(random.randint(0, self.sizey-1)/2)*2]
            p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            
            # Get new points if the current ones are already linked
            while (self.Grid[self.Mid(p1, p2)[1]][self.Mid(p1, p2)[0]] == 1):
                p1 = [round(random.randint(0, self.sizex-1)/2)*2, round(random.randint(0, self.sizey-1)/2)*2]
                p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            self.Grid[self.Mid(p1, p2)[1]][self.Mid(p1, p2)[0]] = 1

    def Mid(self, p1, p2):
        x = y = 0
        # X is equal
        if (p1[0] == p2[0]):
            x = p1[0]
            # Calc y
            if (p1[1] > p2[1]):
                y = p2[1] + 1
            else:
                y = p1[1] + 1
        # Y is equal
        elif (p1[1] == p2[1]):
            y = p1[1]
            # Calc x
            if (p1[0] > p2[0]):
                x = p2[0] + 1
            else:
                x = p1[0] + 1

        return [x, y]

    def PrintGrid(self):
        for row in self.Grid:
            for cell in row:
                if (cell == 0):
                    print(" ", end=" ")
                    #print("\u25A1", end=" ")
                elif (cell == 1):
                    print("\033[1;32;40m\u25A0\033[1;30;40m", end=" ")
                    #print("\u25A0", end=" ")
                elif (cell == 2):
                    print("\033[1;34;40m\u25A0\033[1;30;40m", end=" ")
                elif (cell == 3):
                    print("\033[1;31;40m\u25A0\033[1;30;40m", end=" ")
            print("\n", end="")

    