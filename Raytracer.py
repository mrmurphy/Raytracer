from MTools.Camera import Camera
from MTools.Sphere import Sphere
import pnglib

c = Camera(150, 100)
objs = [
    Sphere((0, 0, -4), 1, [0xff, 0x00, 0x00, 0xff]),
    Sphere((-2.5, 0, -4), 1, [0x00, 0xff, 0x00, 0xff]),
    Sphere((1, -0.5, -3), 1, [0xff, 0xff, 0x00, 0xff]),
    Sphere((2.5, 0, -4), 1, [0x00, 0x00, 0xff, 0xff])]

canvas = pnglib.PNGCanvas(c.width, c.height)
# Draw BG.
canvas.color = [0x22, 0x22, 0x22, 0xff]
canvas.filledRectangle(0,0,c.width-1, c.height-1)
# Draw shapes.
circleColor = [0xaa, 0xaa, 0xaa, 0xff]
for i in xrange(0, c.width - 1):
    for j in xrange(0, c.height - 1):
        ray = c.ray(i, j)
        front = None
        for s in objs:
            hit = ray.hits(s)
            if(hit > 0):
                if(front == None):
                    front = [hit, s]
                elif (hit < front[0]):
                    front = [hit, s]
        if (front != None):
            canvas.point(i, j, front[1].color)

#Write out data.
f = open("out.png", "wb")
f.write(canvas.dump())
f.close()
