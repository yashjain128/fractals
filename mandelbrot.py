import numpy as np

from vispy import plot, scene
from vispy.visuals.transforms import STTransform

fig = plot.Fig(size=(800,800))
fig.title = "Mandelbrot Fractal"

x1, x2 = -2.5, 1
y1, y2 = -1.5, 1.5
width_px = 500
height_px = 500

# real and imaginary axis
re = np.linspace(x1, x2, width_px)
im = np.linspace(y1, y2, height_px)

data = np.zeros((len(im), len(re)))

@fig.events.key_press.connect
def on_key_press(event): 
    if (event.text=='\x12'):
        update()

def update():
    global x1, x2, y1, y2, re, im, data
    rect = plane.camera.rect
    y1, y2 = rect.bottom, rect.top
    x1, x2 = rect.left, rect.right

    re = np.linspace(x1, x2, width_px)
    im = np.linspace(y1, y2, height_px)

    data = np.zeros((len(im), len(re)))
    iter(mandelbrot, data)
    img.set_data(data)
    plane.camera.set_range(x=[x1, x2], y=[y1, y2], margin=0.001)
    img.transform = STTransform(scale=((x2-x1)/width_px, (y2-y1)/height_px), translate=(x1, y1))

def iter(fun, arr):
    for j, b in enumerate(im):
        for i, a in enumerate(re):
            arr[j][i] = fun(a, b, 100)

def mandelbrot(a, b, depth):
    # Z(n) = Z(n-1)^2 + C
    c = complex(a, b)
    z = complex(0., 0.)
    
    for i in range(depth):
        z = (z**2)+c
        if abs(z) > 4.:
            return i
        
    return depth - 1

iter(mandelbrot, data)

# Create coordinate plane
plane = fig[0, 0]

_marr = [[4, 4] for i in range(50)]
mark_data = np.array(_marr, dtype=np.float32)

plane._configure_2d()

m = plane.plot(data=mark_data, face_color="#ff0000")


# Image that moves every time that Ctrl-R is called
img = plane.image(data, cmap='magma')
img.transform = STTransform(scale=((x2-x1)/width_px, (y2-y1)/height_px), translate=(x1, y1))
# Base image to get relative position
base_img = plane.image(data, cmap='magma')
base_img.transform = STTransform(scale=((x2-x1)/width_px, (y2-y1)/height_px), translate=(x1, y1))


plane.camera.set_range(x=[x1, x2], y=[y1, y2], margin=0.001)
plane.view.bgcolor = "#000000"
plane.xlabel = 'a'
plane.ylabel = 'b'

update()
fig.show(run=True)