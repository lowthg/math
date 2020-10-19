import numpy as py
import Gnuplot, Gnuplot.funcutils

xmin = -1.0
xmax = 1.0
ymax = 1.0
m = 0.0
nPts = 200
a = 0.35
x0 = -0.25

def cfunc(x):
    return (py.sqrt(a + (x-m)*(x-m))-x+m)/2

def cdiff(x):
    return ((x-m) / py.sqrt(a + (x-m)*(x-m)) - 1.0)/2

y0 = cfunc(x0)
grad = cdiff(x0)

yleft = y0 + grad * (xmin-x0)
x1 = x0 - y0/grad

xvals = py.linspace(xmin,xmax,nPts)
yvals = map(cfunc, xvals)
g = Gnuplot.Gnuplot()
uselatex = False
if uselatex:
    g("set terminal epslatex dashed size 4.7,4.7")
    g('set output "maxmart_convex.tex"')
else:
    g("set terminal aqua dashed size 600 600")

g("set termoption enhanced")
g("set size ratio 0.7")
g.set_range("xrange", (xmin, xmax))
g.set_range("yrange", (0.0, ymax))
g("unset xtics")
g("unset ytics")
g('set label "$m$" at ' + str(m) + ',-0.035 center')
g('set label "$x$" at ' + str(x1) + ',-0.035 center')
g('set label "$y = \\\\varphi(x)$" at ' + str(x0) + ',-0.035 center')
xlabel1 = -0.5
xlabel2 = 0.5
g('set label "$(m-x)_+$" at ' + str(xlabel1-0.10) + ',' + str(m-xlabel1-0.06) + ' center')
g('set label "$c(x)$" at ' + str(xlabel2) + ',' + str(cfunc(xlabel2)+0.04) + ' center')
plot1 = Gnuplot.Data([xmin, m, xmax], [m-xmin, 0.0, 0.0], with_='lines linewidth 2 lc rgb "black" lt 1')
plot2 = Gnuplot.Data(xvals, yvals, with_='lines linewidth 2 lc rgb "blue" lt 1')
plot3 = Gnuplot.Data([xmin,x1], [yleft, 0.0], with_='lines linewidth 2 lc rgb "red" lt 1')
plot4 = Gnuplot.Data([x0, x0], [0, y0], with_='lines linewidth 1 lc rgb "black" lt 2')
g.plot(plot1, plot2, plot3, plot4)
