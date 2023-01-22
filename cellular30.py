import random
from PIL import Image


def printrow(x, window, pixels):
    rowstr = ""
    for i in range(window):
        if x & 1:
            rowstr += "X"
            pixels[i, printrow.row] = (0, 0, 0)
        else:
            rowstr += " "
        x >>= 1
    assert x == 0
    # pixels[0, printrow.row] = edgecolor
    # pixels[window, printrow.row] = edgecolor
    # print("|" + rowstr + "|")
    printrow.row += 1

printrow.row = 0
# edgecolor = (50, 50, 200)
# edgecolor = (0, 0, 255)
edgecolor = (255, 255, 255)

case = 4
# end = 10000000
end = 1000000000
#end = 150
start = end - 150

if case == 1:
    window = 200
    x = 1 << (window // 2)
elif case == 2:
    window = 200
    random.seed(12345)
    x = random.getrandbits(window)
elif case == 3:
    window = 200
    p = 0.5
    x = 0
    random.seed(12345)
    for i in range(window):
        if random.random() < p:
            x += 1 << i
elif case == 4:
    window = 200
    text = ''.join('{0:08b}'.format(a) for a in b'Zero Knowledge')
    x = int(text[::-1], 2)

else:
    raise Exception("Unknown case")

w = window - 1
a = (1 << window) - 1
img = Image.new('RGB', (window, end - start + 1), "white")
pixels = img.load()
#for i in range(window + 2):
#    pixels[i, 0] = edgecolor
#    pixels[i, end - start + 2] = edgecolor

print(start)
print(end)

print('{:b}'.format(x)[::-1])
if 0 >= start:
    printrow(x, window, pixels)
for i in range(1, end + 1):
    x = (x << 1 & a | x >> w) ^ (x | x >> 1 | (x & 1) << w)
    if i >= start:
        printrow(x, window, pixels)
    if i % 10000000 == 0:
        print(i)

print('{:b}'.format(x)[::-1])

img.show()
