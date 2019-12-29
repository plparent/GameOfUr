#!/bin/env python3
import pyglet

window = pyglet.window.Window(visible=False)
window.set_size(694,465)
window.set_visible()

image = pyglet.resource.image('gameofur.png')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

pyglet.app.run()
