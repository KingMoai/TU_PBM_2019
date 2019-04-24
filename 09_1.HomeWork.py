from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random
import numpy as np
import math

from TUGameEngine import TUGame

class rigidObj :

    def __init__(self):
        ##### rigid body states and properties
        ## 선운동을 위한 상태
        self.loc = np.array([2.5,0.5,0.])
        self.vel = np.array([0.0,0.,0.])
        self.drag = 2.0 ##항력
        ## 회전운동을 위한 상태
        self.angle = 0.
        self.aVel = 0.
        self.aDrag = 2. ##회전 항력
        ## properties
        self.mass = 2.
        self.rMass = 3.

        self.engines = [False,False,False,False]
        self.engineLoc = np.array([[-1.,1.,0.],[1.,1.,0.],[-1.,-1.,0.],[1.,-1.,0.]])
        self.engineForce = np.array([[1.,0.,0.],[-1.,0.,0.],[0.,3.,0.],[0.,3.,0.]])
        print(self.engineLoc[0])

        return

    def show(self):
        glColor3f(1,0,0)
        glPushMatrix()
        glTranslatef(self.loc[0], self.loc[1], self.loc[2])
        glRotatef(math.degrees(self.angle), 0,0,1)

        # 본체
        glBegin(GL_QUADS)
        glVertex2f(-1, 1)
        glVertex2f(-1,-1)
        glVertex2f( 1,-1)
        glVertex2f( 1, 1)
        glEnd()
        # 엔진
        for i in range(4) :
            if self.engines[i] is True :
                glLineWidth(5)
                glColor3f(1,1,0)
                glPushMatrix()
                L = self.engineLoc[i]
                F = self.engineForce[i]
                glTranslatef(L[0], L[1], L[2])
                glBegin(GL_LINES)
                glVertex3f(0,0,0)
                glVertex3f(-F[0], -F[1], -F[2])
                glEnd()
                glPopMatrix()
                glLineWidth(1)

        glPopMatrix()

    def simulate(self, dt):
        # 항력 계산
        fDrag = np.array([0., 0., 0.])
        fDrag = -self.drag * self.vel

        afDrag = np.array([0., 0., 0.])
        afDrag = -self.aDrag * self.aVel

        # 힘 계산 -> 가속 구함
        force = np.array([0.0, 0.0, 0.0])
        for i in range(4) :
            if self.engines[i] is True :
                force += self.local2global(self.engineForce[i])
        acc = force / self.mass

        self.vel += (acc + fDrag / self.mass) * dt #현제 가속도에 항력을 더한뒤 질량을 나누어 준다.
        self.loc += self.vel * dt #항력이 더해진 속도 만큼 loc가 바뀌어서 동작

        # 토크 계산 -> 각가속도 구함
        torque = 0.
        for i in range(4) :
            if self.engines[i] is True:
                torque += self.cross(self.engineLoc[i], self.engineForce[i])
        aAcc = torque / self.rMass #회전할때와 직선운동을 할때 가해지는 항력이 다를 꺼라 생각하여 각각의 항력을 주고 그에따른 질량도 각각 주었다.
        self.aVel += (aAcc + afDrag / self.rMass) * dt #회전에서또한 마찬가지
        self.angle += self.aVel * dt #최전에선 항력이 더해진 속도가 위치 대신 각을 변화

    def local2global(self, v):
        result = np.array([0.,0.,0.])
        c = math.cos(self.angle)
        s = math.sin(self.angle)
        result[0] = c * v[0] - s * v[1]
        result[1] = s * v[0] + c * v[1]
        return result

    def cross(self, u, v):
        return u[0]*v[1]-u[1]*v[0]

    def engineSwitch(self, swNo):
        idx = swNo - 1
        if idx < 0 or idx > 3 :
            return
        if self.engines[idx] is True :
            self.engines[idx] = False
        else :
            self.engines[idx] = True

class myGame(TUGame.Game) :


    def __init__(self, w, h, title):
        super().__init__(w,h,title)

        self.myObj = rigidObj()

        self.initObjects()

        self.cameraAt([0.,0.,20.], [0.,0.,0.], [0.,1.,0.])
        self.cam.setLens(60, 1, 0.1, 2000.)


        #self.setBackground("bg_cosmos.jpg")


    def initObjects(self):

        return


    def frame(self):
        dt = self.getDt()

        super().frame()

        self.myObj.simulate(dt)
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