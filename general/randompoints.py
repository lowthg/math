import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Generate 1000 random points
n = 5000
x = np.random.rand(n) * 1920
y = np.random.rand(n) * 1080
x[0] = 960
y[0] = 540

raw = False

if raw:
    img = Image.new('RGB', (1920, 1080), "black")
    pixels = img.load()

    for i in range(len(x)):
        pixels[int(x[i]), int(y[i])] = (255, 127, 0)

    img.show()
else:

    x = x - 960
    y = y - 540

    # Create a plot
    plt.figure(figsize=(19.20, 10.80), facecolor='black')
    col = (1, 0.5, 0)
    col = [None] * len(x)
    for i in range(len(col)):
        a = np.random.rand()
        b = (np.random.rand()+2)/3
        col[i] = (a, a * b, a * b)
    plt.scatter(x, y, color=col, s=0.3)

    # Set black background and remove axes
    plt.gca().set_facecolor('black')
    plt.gca().axis('off')
    plt.gca().set_xlim(-960, 960)
    plt.gca().set_xlim(-540, 540)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)

    # Save the plot as a PNG file
    plt.savefig('random_points.png', dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black')

    # Show the plot (optional)
    plt.show()