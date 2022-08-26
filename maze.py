import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from random import randint

class maze:
    def __init__(self,height,width, endX, endY, startX, startY, numberTrap = 0):
        self.height = height
        self.width = width
        self.startX = startX
        self.startY = startY
        self.posX = startX
        self.posY = startY
        self.endX = endX
        self.endY = endY
        self.actions = [0, 1, 2, 3] #
        self.stateCount = self.height*self.width
        self.actionCount = len(self.actions)
        self.trap = []
        self.genTrap(numberTrap)

    def genTrap(self,numberTrap = 2):
        while len(self.trap) < numberTrap:
            trapX = randint(1, self.width-1)
            trapY = randint(1, self.height-1)
            canAdd = not (trapX == self.endX and trapY == self.endY)
            if canAdd:
                self.trap.append([trapX,trapY])


    def reset(self):
        self.posX = self.startX
        self.posY = self.startY
        self.done = False
        # Map position
        pos = self.posY + self.posX
        # return pos, 4, False
        return pos, False


    # reset Maze For display trajectory
    def resetMaze(self):
        maze = np.zeros((self.height, self.width))
        maze[self.endY, self.endX] = 5
        for trapX, trapY in self.trap:
            maze[trapY, trapX] = -1
        return maze


    # take action
    def step(self, action):
        if action == 0: # left
            self.posX = self.posX-1 if self.posX > 0 else self.posX
        if action == 1: # right
            self.posX = self.posX+1 if self.posX < self.width - 1 else self.posX
        if action == 2: # up
            self.posY = self.posY-1 if self.posY > 0 else self.posY
        if action == 3: # down
            self.posY = self.posY+1 if self.posY < self.height - 1 else self.posY

        # END CASE
        if self.posX == self.endX and self.posY == self.endY:
            reward = 1
            done = True
        # END with Trap
        elif [self.posX,self.posY] in self.trap:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        # mapping (x,y) position to number
        nextState = self.width * self.posY + self.posX
        # reward = 1 if done else 0
        return nextState, reward, done

    # get current position
    def getPos(self):
        return self.posX, self.posY

    # return a random action
    def randomAction(self):
        return np.random.choice(self.actions)

    # display environment
    def exportTrajectory(self, positionList, title):
        mazeBlank = self.resetMaze()
        listImages = []
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('epochs : {}'.format(title))
        for position in positionList:
            mazedisplay = mazeBlank.copy()
            mazedisplay[position[1], position[0]] = 1
            im = plt.imshow(mazedisplay, animated=True, cmap='hot')
            listImages.append([im])

        ani = animation.ArtistAnimation(fig, listImages, interval=100, blit=True,
                                        repeat_delay=100)
        ani.save('epochs_{}.gif'.format(title.zfill(3)))
        plt.clf()
