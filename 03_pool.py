from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np

from TUGameEngine import TUGame


class myGame(TUGame.Game):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

        self.initObjects()

        self.cameraAt([0, 25, 70], [0, 0, 0])

        obj = self.addObject("bar1", 1)
        obj.translate(-40, 10, -40)
        obj.scale(1, 20, 1)
        obj.color(1, 1, 0, 1.0)
        obj = self.addObject("bar2", 1)
        obj.translate(40, 10, -40)
        obj.scale(1, 20, 1)
        obj.color(1, 1, 0, 1.0)
        obj = self.addObject("bar3", 1)
        obj.translate(40, 10, 40)
        obj.scale(1, 20, 1)
        obj.color(1, 1, 0, 1.0)
        obj = self.addObject("bar4", 1)
        obj.translate(-40, 10, 40)
        obj.scale(1, 20, 1)
        obj.color(1, 1, 0, 1.0)

        obj = self.addTransparentCube("water") ##투명도가 있는 큐브
        obj.scale(80, 10, 80)
        obj.translate(0, 5, 0)
        obj.color(0.5, 0.75, 1.5, 0.8)

        wall = self.addTransparentObject("wall2", 1)
        wall.scale(80, 20, 0.1)
        wall.translate(0, 10, -40)
        wall.color(1, 1, 1, 0.5)

        wall = self.addTransparentObject("wall2", 1)
        wall.scale(80, 20, 0.1)
        wall.translate(40, 10, 0)
        wall.rotate(90, 0, 0)
        wall.color(1, 1, 1, 0.5)

        wall = self.addTransparentObject("wall2", 1)
        wall.scale(80, 20, 0.1)
        wall.translate(-40, 10, 0)
        wall.rotate(90, 0, 0)
        wall.color(1, 1, 1, 0.5)

        #self.setBackground(b"background.jpg")

    def initObjects(self):
        self.loc = []
        self.vel = []
        self.mass= []
        for i in range(0, 500): ##500개의 공이 같은 위치에
            self.loc.append(np.array([0, 25, 0]))
            self.vel.append(np.array([
                60.0 * (random.random() - 0.5),
                -random.random() * 10,
                60.0 * (random.random() - 0.5)])) ##vel값이 랜덤
            self.mass.append(random.random()+1.0)  # mass ranges [1.0,2.0)

    def frame(self):

        dt = self.getDt()

        super().frame()
        # your code here

        g = np.array([0.0, -9.8, 0.0])

        # collision detection and handling
        epsilon = 0.9 ##탄성계수
        C_drag = 2.0 ##항력
        rho = 0.4 ##부력에 사용할것
        vortexScale = 10.5

        # numerical integration : simulation
        glColor3f(1.0, 1.0, 0.5)
        for i in range(0, 500):
            # if balls are under the water
            f_drag = np.array([0., 0., 0.]) ##항력
            f_buoy = np.array([0., 0., 0.]) ##부력
            if self.loc[i][1] < 10:
                f_drag = -C_drag * self.vel[i] # 항력을 계산
                f_buoy = -rho * g * 4.0 #부력을 계산
            F = f_drag + f_buoy ##물체에 힘이 가해질땐 힘들이 더해진다

            self.vel[i] = self.vel[i] + (g + F/self.mass[i]) * dt
            self.loc[i] = self.loc[i] + self.vel[i] * dt
            glColor3f(self.mass[i]-1.0, 2.0-self.mass[i], 2.0-self.mass[i]) ##무게에 따른 색 변환
            self.drawBall(self.loc[i], 0.5)

        # collision detection and handling
        # floor
        min = -40.0 + 1.0
        max = 40.0 - 1.0

        for i in range(0, 500):
            if self.loc[i][1] < 0:
                self.loc[i][1] *= -epsilon
                if self.vel[i][1] < 0.0:
                    self.vel[i][1] *= -epsilon;

        # right wall (x=40)
        for i in range(0, 500):
            if self.loc[i][0] > max:
                penetration = self.loc[i][0] - max
                self.loc[i][0] -= (1.0 + epsilon) * penetration
                if self.vel[i][0] > 0.0:
                    self.vel[i][0] *= -epsilon;

        # left wall (x=-40)
        for i in range(0, 500):
            if self.loc[i][0] < min:
                penetration = min - self.loc[i][0]
                self.loc[i][0] += (1.0 + epsilon) * penetration
                if self.vel[i][0] < 0.0:
                    self.vel[i][0] *= -epsilon;

        # near wall (z=40)
        for i in range(0, 500):
            if self.loc[i][2] > max:
                penetration = self.loc[i][2] - max
                self.loc[i][2] -= (1.0 + epsilon) * penetration
                if self.vel[i][2] > 0.0:
                    self.vel[i][2] *= -epsilon;

        # far wall (z=-40)
        for i in range(0, 500):
            if self.loc[i][2] < min:
                penetration = min - self.loc[i][2]
                self.loc[i][2] += (1.0 + epsilon) * penetration
                if self.vel[i][2] < 0.0:
                    self.vel[i][2] *= -epsilon;

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