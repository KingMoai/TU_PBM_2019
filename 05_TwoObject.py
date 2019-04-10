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
        self.vel = []
        self.mass = []
        self.force = []
        self.loc.append(np.array([-15., 5., 0.])) #append : 배열에 어떤값을 넣는 것
        self.loc.append(np.array([15., -5., 0.]))
        self.vel.append(np.array([5., 0., 0.]))
        self.vel.append(np.array([-5., 0., 0.]))
        self.mass.append(1.0)
        self.mass.append(20.0)
        self.force.append(np.array([0., 0., 0.]))
        self.force.append(np.array([0., 0., 0.]))

        self.cameraAt([0, 0, 50], [0, 0, 0])

        # self.setBackground(b"background.jpg")

    def initObjects(self): #오브젝트를 원래 상태로 되돌림
        self.loc[0] = np.array([-15., 5., 0.])
        self.loc[1] = np.array([15., -5., 0.])
        self.vel[0] = np.array([5., 0., 0.])
        self.vel[1] = np.array([-5., 0., 0.])

    def frame(self):

        dt = self.getDt()

        super().frame()
        # your code here
        G = 100 #중력 계수
        m = [self.mass[0], self.mass[1]]
        x01 = self.loc[1] - self.loc[0]
        dist = np.linalg.norm(x01) #linalg.norm : 벡터의 길이를 반환 ##두 물체사이의 거리
        fdir = [x01/dist, -x01/dist] #힘의 방향
        mg = G * m[0] * m[1] / dist**2 #만유 인력

        # compute force
        for i in range(0, 2):
            self.force[i] = fdir[i] * mg ##만유인력을 방향을 곱해서 힘생성

        # simulate with the force
        for i in range(0, 2):
            self.vel[i] += self.force[i] * dt / m[i]  #속도를 시간으로 미분시 가속도 ##힘을 적분한게 아니라 가속을 적분한것
            self.loc[i] += self.vel[i] * dt

        for balls in self.loc:              # == for i in range(2):
            self.drawBall(balls)                    #self.drawBall(self.loc[i])

        super().afterFrame()

game = myGame(500, 500, b"gravity")
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