from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np

from TUGameEngine import TUGame


class myGame(TUGame.Game):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

        self.loc = []
        self.initObjects()

        sphere1 = self.addSphere("mySphere1")
        sphere1.translate(1,1,1)
        sphere1.color(1,0,0)

        cube = self.addCube("cube")
        cube.translate(0,5,-5)
        cube.scale(10,10,2)
        cube.color(0,1,0)

        cube2 = self.addTransparentCube("tCube")
        cube2.scale(5,5,5)
        cube2.color(0,1,1,0.7)

        cube3 = cube2.addChild("childCube", 1) # sphere
        cube3.rotate(45, 0,0)
        cube3.scale(5,5,5)
        cube3.translate(5,5,5)


        self.cameraAt([0,40,10], [0,0,0])

        #self.setBackground(b"background.jpg")

    def initObjects(self):
        self.loc = [0,0,0]

    def frame(self):

        dt = self.getDt()
        et = self.getEt()

        super().frame()
        # your code here

        myCube = self.scene.find("tCube")
        myCube.rotate(et*20.0, 0,0)


        self.loc[0] += 0.1
        self.drawBall(self.loc)

        super().afterFrame()


game = myGame(500, 500, b"Hello My World")
game.grid(True)


def key(k, x, y):
    if k is b' ':
        if game.timer.timerRunning:
            game.timerStop()
        else:
            game.timerStart()
    elif k is b'r':
        game.timerReset()
        game.initObjects()


def draw():
    game.frame()

game.start(draw, key)