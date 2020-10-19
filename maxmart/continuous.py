import numpy as py
import Gnuplot.funcutils
import random

random.seed(4)

def phi(x):
    return x - 2.0 - 1.0 / (x + 1)

dt = 0.001
sdt = py.sqrt(dt)

W = 0.0
Wmax = 0.0
t = 0.0
target = phi(W)

Wvals = [W]
tvals = [t]
Wmaxvals = [Wmax]
targetvals = [target]

count = 0

while (count < 20000) & (W > target):
    t += dt
    W += random.normalvariate(0, 1) * sdt
    if W > Wmax:
        Wmax = W
        target = phi(W)
    Wvals.append(max(W,target))
    tvals.append(t)
    Wmaxvals.append(Wmax)
    targetvals.append(target)
    count += 1

print count
print t

g = Gnuplot.Gnuplot()

uselatex = False
if uselatex:
    g("set terminal epslatex dashed size 4.7,4.7")
    g('set output "maxmart_continuous.tex"')
else:
    g("set terminal aqua dashed size 600 600")

g("set termoption enhanced")
g("set size ratio 0.85")
g("unset xtics")
g("unset ytics")

ymax = Wmaxvals[-1] * 1.1
ymin = min(Wvals) - 0.5
svals = map(lambda t: t/(t + 1.0) * 0.95, tvals)

g.set_range("yrange", (ymin, ymax))
g.set_range("xrange", (0, 1))

g('set label "$0$" at 0,' + str(ymin-0.1) + ' center')
g('set label "$1$" at 1,' + str(ymin-0.1) + ' center')
g('set label "$\\\\tau^*$" at ' + str(svals[-1]-0.01) + ',' + str(ymin-0.1) + ' left')
g('set label "$X^*$" at 0.5,1 center')
g('set label "$\\\\varphi(X^*)$" at 0.5,-1.5 center')
g('set label "$X$" at 0.35,-0.13 center')
g('set label "$m$" at -0.03,0 center')


s2vals = list(svals)
s2vals.append(1.0)
Wvals.append(Wvals[-1])
plot1 = Gnuplot.Data(s2vals, Wvals, with_='lines linewidth 1 lc rgb "black" lt 1')
plot2 = Gnuplot.Data(svals, Wmaxvals, with_='lines linewidth 4 lc rgb "blue" lt 1')
plot3 = Gnuplot.Data(svals, targetvals, with_='lines linewidth 4 lc rgb "red" lt 1')

g.plot(plot1, plot2,plot3)