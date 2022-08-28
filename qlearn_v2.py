from maze import maze
import numpy as np
import time
import matplotlib.pyplot as plt

# create Maze
height = 7
width = 7
endX = width - 1
endY = 0
env = maze(height=height, width=width, endX=endX, endY=endY, startX=0, startY=6,
           numberTrap=7)

# create Q-table
qtable = []
for i in range(env.stateCount):
    qtable.append([0]*env.actionCount)

# hyperparameters
epochs = 200
gamma = 0.95
epsilon = 0.1
alpha = 0.2

# parameters for output
epochList = [1,10,50,75,100,150]
resultSteps = []

def exportQtable(title):
    plt.clf()
    qtableNP = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            # mapping (x,y) position to number
            temp_maxQ = max(qtable[width * j + i])
            qtableNP[j, i] = temp_maxQ
            # qtableNP[position[i], position[j]] = max(max(qtable[next_state]))

    fig, ax = plt.subplots()
    ax.set_title('epochs : {}'.format(title))
    shw = ax.imshow(qtableNP)
    bar = plt.colorbar(shw)
    bar.set_label('ColorBar')
    plt.savefig('epochs {}.png'.format(str(title).zfill(3)))
    plt.clf()


if __name__ == '__main__':
    # training loop
    for i in range(epochs):
        state, done = env.reset()
        # reset start reward
        reward = 999
        steps = 0
        actions = []
        positionList = []
        # add start position
        positionList.append(env.getPos())
        print("epoch #", i + 1, "/", epochs)
        while not done:
            time.sleep(0.05)

            # count steps to finish game
            steps += 1

            # act randomly sometimes to allow exploration
            if np.random.uniform() < epsilon:
                action = env.randomAction()
            # if not select max action in Qtable (act greedy)
            else:
                action = qtable[state].index(max(qtable[state]))
                maxQ = max(qtable[state])
                minQ = min(qtable[state])
                if minQ==maxQ:
                    action = env.randomAction()

            # take action
            next_state, reward, done = env.step(action)
            actions.append(action)
            # update qtable value with Bellman equation
            maxQ = max(qtable[next_state])
            qtable[state][action] = qtable[state][action] + alpha*(reward + gamma * max(qtable[next_state])-qtable[state][action])

            # update state
            state = next_state
            # save position
            positionList.append(env.getPos())

        print("\nDone in", steps, "steps".format(steps))
        print(actions)
        # export Q-Table
        # export Trajectory
        if i+1 in epochList:
            env.exportTrajectory(title="{}_{}x{}".format(str(i+1),height,width),positionList=positionList)
            exportQtable(title=(str(i+1)))
        resultSteps.append(steps)
        time.sleep(0.8)

    plt.plot(resultSteps)
    plt.ylabel("Number of Steps")
    plt.xlabel("Epoch")
    plt.savefig('step.png')
    # plt.show()