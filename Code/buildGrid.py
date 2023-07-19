from matplotlib import pyplot
from matplotlib.pyplot import figure, draw, pause
from matplotlib import colors
import numpy as np
import random
import mazeBuilder

class Grid():

        def __init__(self):
                pass

        def build_new_maze(self):
                self.grid = mazeBuilder.Generator(0, 0, 101, 101).Grid

        def generate_figure(self):
                # some lines of code initializing grid
                self.grid[0][0] = -1
                self.grid[-1][-1] = -1
                pyplot.figure(figsize = (8,8))
                colormap = colors.ListedColormap(["#2bf016","gray","white"])
                self.figure = pyplot.imshow(self.grid, cmap=colormap)
                ax = pyplot.gca()

                # create gridlines
                ax.set_xticks(np.arange(-.5, 101, 1), minor=True)
                ax.set_yticks(np.arange(-.5, 101, 1), minor=True)

                ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

                pyplot.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
                pyplot.show()
        
        def color_path(self, coordinates):
                # for each tuple inside list of coordinates - color blue
                for x, y in coordinates:
                        self.grid[y][x] = 2
                self.grid[0][0] = -1
                self.grid[-1][-1] = -1

                pyplot.figure(figsize = (8,8))
                colormap = colors.ListedColormap(["#2bf016","gray","white","#8cfffb"])
                self.figure = pyplot.imshow(self.grid, cmap=colormap)
                ax = pyplot.gca()

                # create gridlines
                ax.set_xticks(np.arange(-.5, 101, 1), minor=True)
                ax.set_yticks(np.arange(-.5, 101, 1), minor=True)

                ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

                pyplot.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
                pyplot.show()