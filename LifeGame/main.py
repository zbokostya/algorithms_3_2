import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

matplotlib.use("TkAgg")


def randomGrid(N):
    arr = np.random.randint(2, size=N * N)
    return arr.reshape(N, N)


class Grid:
    def __init__(self, N):
        self.grid = randomGrid(N)

    def count_neighbours(self, x, y):
        neighbours = 0
        arr = [-1, 0, 1]
        for i in arr:
            for j in arr:
                neighbours += self.grid[(x + i) % len(self.grid)][(y + j) % len(self.grid[0])]
        return neighbours - self.grid[x][y]

    def update(self, frameNum, img, abc):
        next_iter = self.grid.copy()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                neighbours = self.count_neighbours(i, j)
                if self.grid[i][j] == 0 and neighbours == 3:
                    next_iter[i][j] = 1
                elif self.grid[i][j] == 1 and (neighbours < 2 or neighbours > 3):
                    next_iter[i][j] = 0

        img.set_data(next_iter)
        self.grid = next_iter
        return img


if __name__ == '__main__':
    updateInterval = 50
    gridCl = Grid(50)
    grid = gridCl.grid
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, func=gridCl.update,
                                  fargs=(img, gridCl),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()
