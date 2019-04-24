from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math
import numpy as np

from TUGameEngine import TUGame


import HoverCraft as HC
import common

class myGame(TUGame.Game) :


    def __init__(self, w, h, title):
        super().__init__(w,h,title)

        self.myObj = HC.HoverCraft()

        self.initObjects()


        self.cam.setLens(60, 1, 0.1, 2000.)


        #self.setBackground("bg_cosmos.jpg")


    def initObjects(self):

        return


    def frame(self):

        dt = self.getDt()

        super().frame()

        self.myObj.simulate(dt)

        loc = self.myObj.getLoc()
        up = common.local2global(self.myObj.angle, [0, 1, 0])

        self.cameraAt([loc[0], loc[1], 25.], loc, up )

        self.myObj.show()


        super().afterFrame()


game = myGame(500,500, b"2D Rigid")
game.grid(True)
game.rotateGrid(90, [1,0,0])

def key(k, x,y) :

    if k is b' ' :
        if game.timer.timerRunning :
            game.timerStop()
        else :
            game.timerStart()
    elif k is b'r':
        game.timerReset()
        game.initObjects()

    elif k is b'1':
        game.myObj.engineSwitch(1)
    elif k is b'2':
        game.myObj.engineSwitch(2)
    elif k is b'3':
        game.myObj.engineSwitch(3)
    elif k is b'4':
        game.myObj.engineSwitch(4)


def draw() :
    game.frame()

game.start(draw, key)