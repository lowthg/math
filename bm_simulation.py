import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Set up the figure and axis
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1, hspace=0, wspace=0)

marker = dict(marker='o', markerfacecolor='black', markeredgecolor='black', markersize=5)

# Define the quadratic function
def quadratic(a, b, c, x):
    return a * x**2 + b * x + c


# Define the animation update function
def update(frame):
    global states
    ax.clear()
    ax.set_facecolor('black')
    xvals = []
    yvals = []
    sizes = []
    for state in states:
        var = state[2]
        state[0] += random.gauss(0, var)
        state[1] += random.gauss(0, var)
        xvals.append(state[0])
        yvals.append(state[1])
        sizes.append(state[3] * 5)
#        ax.plot(state[0], state[1], **marker)

    ax.scatter(xvals, yvals, s=sizes, color='white')

    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xticks([])
    ax.set_yticks([])

random.seed(1)
var = 0.005
nparticles = 4000

states = []
for i in range(nparticles):
    size = random.uniform(0,1) + 0.5
    states.append([random.uniform(-1, 1), random.uniform(-1,1), var/size, size])


# Create the animation
ani = animation.FuncAnimation(fig, update, interval=40)

# Save the animation as an animated GIF
animation_file = 'bm_animation.gif'
ani.save(animation_file, writer='pillow')

# Display the animation
plt.show()

