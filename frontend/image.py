import pyglet

window = pyglet.window.Window(width=762, height=321)

background_image = pyglet.resource.image('board.png')
white_image = pyglet.resource.image('white.png')
white = pyglet.sprite.Sprite(white_image, x=50, y=50)
black_image = pyglet.resource.image('black.png')
black = pyglet.sprite.Sprite(black_image, x=50, y=150)

@window.event
def on_draw():
    window.clear()
    background_image.blit(0,0)
    white.draw()
    black.draw()

pyglet.app.run()
