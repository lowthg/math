import numpy as py
import PyGnuplot as gp
#import Gnuplot, Gnuplot.funcutils

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

#g = Gnuplot.Gnuplot()

uselatex = False
if uselatex:
    gp.c("set terminal epslatex dashed size 4.7,4.7")
    gp.c('set output "maxmart_cadlag.tex"')
else:
    gp.c("set terminal aqua dashed size 600 600")

gp.c("set termoption enhanced")
gp.c("set size ratio 0.85")
gp.c("set xrange[0.0:1.0]")
gp.c("set yrange[{},{}]".format(ymin, ymax))
gp.c("unset xtics")
gp.c("unset ytics")

gp.c('set label "$0$" at 0,' + str(ymin-0.24) + ' center')
gp.c('set label "$1$" at 1,' + str(ymin-0.24) + ' center')
gp.c('set label "$m$" at -0.012,0 right')
gp.c('set label "$\\\\tau$" at ' + str(tau) + ',' + str(ymin-0.24) + ' center')
t0 = 0.2
gp.c('set label "$X_t$" at ' + str(t0) + ',' + str(ffunc(t0)+0.26) + ' center')
t1 = 0.72
gp.c('set label "$f(t)$" at ' + str(t1) + ',' + str(ffunc(t1)+0.2) + ' right')
t2 = 0.8
gp.c('set label "$\\\\varphi(f(t))$" at ' + str(t2+0.01) + ',' + str(gfunc(t2)) + ' left')

tvals = py.linspace(tau, tfmax, nPts)
tgvals = py.linspace(tgmin, tgmax, nPts)
fvals = list(map(ffunc, tvals))
gvals = list(map(gfunc, tgvals))
xtvals = py.linspace(0.0, tau, nPts)
xvals = list(map(ffunc, xtvals))
yend = gfunc(tau)

#gp.s([tvals, fvals, tgvals, gvals, xtvals, xvals, [tau,1], [yend, yend]])
gp.s([tvals, fvals])
#plot1 = Gnuplot.Data(tvals, fvals, with_='lines linewidth 1 lc rgb "black" lt 2')
#plot2 = Gnuplot.Data(tgvals, gvals, with_='lines linewidth 1 lc rgb "black" lt 2')
#plot3 = Gnuplot.Data(xtvals, xvals, with_='lines linewidth 4 lc rgb "blue" lt 1')
#plot4 = Gnuplot.Data([tau, 1], [yend, yend], with_='lines linewidth 4 lc rgb "blue" lt 1')

#g.plot(plot1, plot2, plot3, plot4)

gp.c('plot "tmp.dat" u 1:2 w lp')
gp.p('myfigure.ps')
