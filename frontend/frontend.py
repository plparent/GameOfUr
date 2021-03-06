#!/bin/env python3
import pyglet
import time
import os
import sys
import easygui

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

import board
import square

class Button:
    def __init__(self, name, x, y, fct, img):
        self.name = name
        self.x = x
        self.y = y
        self.width = img.width
        self.height = img.height
        self.fct = fct
        self.img = img

    def click(self, x, y):
        if self.x <= x and x <= self.x + self.width and self.y <= y and y <= self.y + self.height:
            self.fct()
            return True
        else:
            return False

    def render(self):
        pyglet.sprite.Sprite(self.img, x=self.x, y=self.y).draw()
        pyglet.text.Label(self.name,
                          font_name='Times New Roman',
                          font_size=16,
                          color=(0,0,0,255),
                          x=self.x + 30, y=self.y + 18).draw()
            

def grid2square(x, y, offsetX, offsetY):
    i = -1
    j = -1

    x = x - offsetX
    y = y - offsetY

    if y > 217 and y <= 287:
        i = 0
    elif y > 131 and y <= 201:
        i = 1
    elif y > 45 and y <= 115:
        i = 2

    if x > 38 and x <= 108:
        j = 0
    elif x > 124 and x <= 194:
        j = 1
    elif x > 212 and x <= 284:
        j = 2
    elif x > 299 and x <= 374:
        j = 3
    elif x > 390 and x <= 462:
        j = 4
    elif x > 474 and x <= 546:
        j = 5
    elif x > 560 and x <= 634:
        j = 6
    elif x > 646 and x <= 720:
        j = 7

    if i == -1 or j == -1:
        return -1
    else:
        return i * 8 + j

def square2grid(pos, offsetX, offsetY):
    xTable = [39, 125, 213, 300, 391, 475, 561, 647]
    yTable = [218, 132, 46]
    if pos >= 0 and pos < 24:
        return (xTable[pos % 8] + offsetX, yTable[pos // 8] + offsetY)
    else:
        return (-1,-1)



game = board.Board()
button_list = []


window = pyglet.window.Window(width=1024, height=600)

background_image = pyglet.resource.image('background.png')
board_image = pyglet.resource.image('board.png')
white_image = pyglet.resource.image('white.png')
black_image = pyglet.resource.image('black.png')
button_image = pyglet.resource.image('button.png')
button_image.width = 175
button_image.height = 50

background = pyglet.sprite.Sprite(board_image, y=150)

def nextmove():
    game.NextMove()

def previousmove():
    game.PreviousMove()

def savegame():
    name = "GameOfUrSave-" + str(time.time())
    game.SaveGame(name)
    print("Saved: ", name)

def loadgame():
    name = easygui.fileopenbox()
    game.LoadGame(name)
    button_list.append(Button("Next Move", 600, 25, nextmove, button_image))
    button_list.append(Button("Previous Move", 200, 25, previousmove, button_image))
    print("Loaded: ", name)

button_list.append(Button("Save Replay", 800, 500, savegame, button_image))
button_list.append(Button("Load Replay", 800, 400, loadgame, button_image))


game.ThrowDice(-1)
hasWon = square.Color.empty

def draw_count(num, color, offsetX, offsetY):
    for i in range(num):
        if color == square.Color.white:
            pyglet.sprite.Sprite(white_image, x=offsetX + i * 64, y=offsetY).draw()
        else:
            pyglet.sprite.Sprite(black_image, x=offsetX + i * 64, y=offsetY).draw()

@window.event
def on_mouse_press(x,y,button,modifiers):
    if button == pyglet.window.mouse.LEFT:
        is_button = False
        for b in button_list:
            is_button = b.click(x,y)
            if is_button:
                break
        
        if not is_button:
            if game.CanMove():
                if game.Move(grid2square(x, y, 0, 150)):
                    game.ThrowDice(-1)

                    global hasWon
                    if game.HasWon(square.Color.white):
                        hasWon = square.Color.white
                    elif game.HasWon(square.Color.black):
                        hasWon = square.Color.black
            else:
                game.ThrowDice(-1)
        

@window.event
def on_draw():
    window.clear()
    background_image.blit(0,0)
    background.draw()

    for i in range(24):
        item = game.GetSquare(i)
        x,y = square2grid(i, 0, 150)
        if item.GetColor() == square.Color.white:
            pyglet.sprite.Sprite(white_image, x=x, y=y).draw()
        elif item.GetColor() == square.Color.black:
            pyglet.sprite.Sprite(black_image, x=x, y=y).draw()

    draw_count(game.GetSquare(4).GetCount(), square.Color.black, 0, 470)
    draw_count(game.GetSquare(20).GetCount(), square.Color.white, 0, 100)

    draw_count(game.GetSquare(5).GetCount(), square.Color.black, 500, 470)
    draw_count(game.GetSquare(21).GetCount(), square.Color.white, 500, 100)

    pyglet.text.Label('Dice: ' + str(game.dice),
                      font_name='Times New Roman',
                      font_size=36,
                      color=(0,0,0,255),
                      x=800, y=300).draw()

    pyglet.text.Label('Player: ' + str(game.GetTurn())[6:],
                      font_name='Times New Roman',
                      font_size=24,
                      color=(0,0,0,255),
                      x=800, y=250).draw()

    if hasWon != square.Color.empty:
        pyglet.text.Label(str(hasWon)[6:] + ' Won!',
                          font_name='Times New Roman',
                          font_size=36,
                          color=(0,0,0,255),
                          x=400, y=50).draw()

    for button in button_list:
        button.render()

if __name__ == "__main__":
    pyglet.app.run()
