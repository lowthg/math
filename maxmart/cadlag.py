import numpy as py
import Gnuplot, Gnuplot.funcutils

def ffunc(t):
    return t/(1.0-t)+t * 1.5
def gfunc(t):
    return 1.0 / (1.0-t) - 1.3 / t

ymax = 5.0
ymin = -2.5
nPts = 200
tfmax = ymax/(1.0+ymax)
tgmin = 1.0 / (2.0 - ymin)
tgmax = (ymax + 2.0)/(ymax + 3.0)
tau = 0.65

g = Gnuplot.Gnuplot()

uselatex = False
if uselatex:
    g("set terminal epslatex dashed size 4.7,4.7")
    g('set output "maxmart_cadlag.tex"')
else:
    g("set terminal aqua dashed size 600 600")

g("set termoption enhanced")
g("set size ratio 0.85")
g.set_range("xrange", (0.0, 1.0))
g.set_range("yrange", (ymin, ymax))
g("unset xtics")
g("unset ytics")

g('set label "$0$" at 0,' + str(ymin-0.24) + ' center')
g('set label "$1$" at 1,' + str(ymin-0.24) + ' center')
g('set label "$m$" at -0.012,0 right')
g('set label "$\\\\tau$" at ' + str(tau) + ',' + str(ymin-0.24) + ' center')
t0 = 0.2
g('set label "$X_t$" at ' + str(t0) + ',' + str(ffunc(t0)+0.26) + ' center')
t1 = 0.72
g('set label "$f(t)$" at ' + str(t1) + ',' + str(ffunc(t1)+0.2) + ' right')
t2 = 0.8
g('set label "$\\\\varphi(f(t))$" at ' + str(t2+0.01) + ',' + str(gfunc(t2)) + ' left')

tvals = py.linspace(tau, tfmax, nPts)
fvals = map(ffunc, tvals)
plot1 = Gnuplot.Data(tvals, fvals, with_='lines linewidth 1 lc rgb "black" lt 2')
tgvals = py.linspace(tgmin, tgmax, nPts)
gvals = map(gfunc, tgvals)
plot2 = Gnuplot.Data(tgvals, gvals, with_='lines linewidth 1 lc rgb "black" lt 2')

xtvals = py.linspace(0.0, tau, nPts)
xvals = map(ffunc, xtvals)
yend = gfunc(tau)

plot3 = Gnuplot.Data(xtvals, xvals, with_='lines linewidth 4 lc rgb "blue" lt 1')
plot4 = Gnuplot.Data([tau, 1], [yend, yend], with_='lines linewidth 4 lc rgb "blue" lt 1')

g.plot(plot1, plot2, plot3, plot4)
