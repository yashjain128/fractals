from vispy import plot, scene
import numpy as np  

fig = plot.Fig(size=(800,800))
fig.title = "Mandelbrot Set"

plane = fig[0, 0]
plane._configure_2d()

view_grid = scene.visuals.GridLines(color=(0, 0, 0, 0.25))
view_grid.set_gl_state('translucent')
plane.view.add(view_grid)

x1, x2 = -2, 2
y1, y2 = -2, 2 
density_per_unit = 250

plane.view.camera.set_range(x=[x1, x2], y=[y1, y2])

px_width = (x2-x1) * density_per_unit
px_height = (y2-y1) * density_per_unit
# real and imaginary axis
re = np.linspace(x1, x2, px_width)
im = np.linspace(y1, y2, px_height)

data = np.zeros((len(re), len(im)))

def mandelbrot(x, y, threshold):
    """Calculates whether the number c = x + i*y belongs to the 
    Mandelbrot set. In order to belong, the sequence z[i + 1] = z[i]**2 + c
    must not diverge after 'threshold' number of steps. The sequence diverges
    if the absolute value of z[i+1] is greater than 4.
    
    :param float x: the x component of the initial complex number
    :param float y: the y component of the initial complex number
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    c = complex(x, y)
    z = complex(0, 0)
    
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:  # it diverged
            return i
        
    return threshold - 1  # it didn't diverge

def basic(x, y):
    return x+y;

print(data)
img = scene.visuals.Image(data, 
                          interpolation='nearest',
                          parent=plane.view.scene,
                          method='subdivide',
                          cmap='magma')


fig.show(run=True)