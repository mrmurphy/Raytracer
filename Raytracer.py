from MTools.Camera import Camera
from MTools.Sphere import Sphere
from MTools.Vector import Vector
from MTools.Light import Light
import pnglib
import sys

def Diffuse(hit, lights):
    color = hit.objColor
    newColor = [0, 0, 0, 255]
    for light in lights:
        # Loop through the colors
        for i in xrange(3):
            brightness = light.intensity * \
                hit.normal.dot((light.position - hit.worldHit).normalize())
            newColor[i] = newColor[i] + max(0, int(color[i] * brightness))
    return newColor

def Normal(hit):
    red = max(0, int(0xff * hit.normal.x))
    green = max(0, int(0xff * hit.normal.y))
    blue = max(0, int(0xff * hit.normal.z))
    return [red, green, blue, 0xff]

def RenderFrame(cam, objects, lights, outfile):
    canvas = pnglib.PNGCanvas(c.width, c.height)
    # Draw BG.
    canvas.color = [0x22, 0x22, 0x22, 0xff]
    canvas.filledRectangle(0,0, cam.width-1, cam.height-1)
    # Draw shapes.
    for i in xrange(0, cam.width - 1):
        for j in xrange(0, cam.height - 1):
            ray = cam.ray(i, cam.height - j)
            # This is to tell what's in the front:
            front = None
            for s in objects:
                hit = ray.hits(s)
                if(hit):
                    if(front == None):
                        front = hit
                    elif (hit.dist < front.dist):
                        front = hit
            if (front):
                # Do some shading:
                canvas.point(i, j, Diffuse(front, lights))

    #Write out data.
    f = open(outfile, "wb")
    f.write(canvas.dump())
    f.close()

def RenderAnimation(cam, objects, lights, prefix):
    for i in xrange(40):
        change = cam.e.x + 0.1
        cam.eSet(change, cam.e.y, cam.e.z)
        cam.lookAt(0, 0, -4)
        outname = prefix + str(i) + ".png"
        RenderFrame(cam, objects, lights, outname)

c = Camera(600, 400)
c.eSet(-2, 5, -1)
c.lookAt(0, 0, -4)
c.angleSet(60)

objs = [
    Sphere((0, 0, -4), 1, [0xff, 0x00, 0x00, 0xff]),
    Sphere((-2.5, 0, -4), 1, [0x00, 0xff, 0x00, 0xff]),
    Sphere((-1, 0.5, -3), 1, [0xff, 0xff, 0x00, 0xff]),
    Sphere((2.5, -0.7, -4), 1, [0x00, 0x00, 0xff, 0xff])]
lights = [Light(Vector(0, 55, -4), [0xff, 0xff, 0xff], 1),
            Light(Vector(0, -7, -4), [0xff, 0xff, 0xff], 0.2)]

# RenderFrame(c, objs, lights, "out.png")
RenderAnimation(c, objs, lights, "render/spheres")
