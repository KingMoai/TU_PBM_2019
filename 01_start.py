##use professor code
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np
from math import *
from TUGameEngine import TUGame

class myGame(TUGame.Game):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

        self.loc = []
        self.initObjects()
        #self.setBackground(b"background.jpg")

    def initObjects(self):
        self.loc = np.array([0. ,0. ,0.])
        self.vel = np.array([5., 10., 0.])

    def frame(self):
        dt = self.getDt()
        et = self.getEt()
        e = 0.9
        mess = 1.
        super().frame()

        # your code here
        #f/m = a
        #dv = a dt --> v <= v + dv
        #dx = v dt --> x <= v + dx
        gravity = np.array([0., -9.8, 0.]) ##중력 가속도
        dragC = 1.0 ## 항력
        f_drag = -dragC * self.vel #정성 항력 즉 층류 상태

        self.vel += (gravity + f_drag / mess) * dt ##중력에 항력과 질량을 적용하여 속도변환 제어
        self.loc += self.vel * dt

        self.cameraAt(self.loc + np.array([self.loc[0], 2., 5.]), self.loc)

        if self.loc[1] < 0.0: ##충돌체크
            self.loc[1] = -e * self.loc[1] #충돌시 y값 반전시켜 멈춤
            if self.vel[1] < 0.0: ##충돌시 속도변환
                self.vel[1] = -e * self.vel[1] ##충돌시 y값을 반전시켜 튀어오름

        self.drawBall(self.loc, 0.1)

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
