from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import numpy as np

# P(t) : t 시간의 위치
# P(t) = P(0) + V(0)*t + 1/2 * g * t^2
# Ball = Ball_최초 + 속도_최초 * t + 0.5 * 중력가속도 * t*t

dt = -1
currentTime = 0
lastTime=0

def TimerOn() :
    if dt>0 :
        return True
    else :
        return False

def TimerStart():
    global currentTime, lastTime, dt
    if dt<0 :
        currentTime = time.perf_counter()
        lastTime = currentTime

def TimerGetDt():
    global currentTime, lastTime, dt
    currentTime = time.perf_counter()
    dt = currentTime - lastTime
    lastTime = currentTime
    return dt

ball1 = np.array([0,0,0])   # P(0)
ball2 = np.array([0,0,5])

ball1V = np.array([5,15,0])     # V(0)
ball2V = np.array([5,15,0])

g = np.array([0, -10, 0])

et = 0.0 # elapsed time = dt의 누적


simulationStart = False

def GLinit() :
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL with Python")

def RegisterCallbacks() :
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutKeyboardFunc(key)

def key(k, x,y) :
    global simulationStart
    simulationStart = True

def drawLine(x,y,z, xx,yy,zz) :
    glBegin(GL_LINES)
    glVertex3f(x,y,z)
    glVertex3f(xx,yy,zz)
    glEnd()

def drawBall(pos) :
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glutWireSphere(1.0, 10,10)
    glPopMatrix()


def draw():
    global ball1, ball2, ball1V, ball2V, g, dt, et

    if TimerOn() != True :
        TimerStart()
        et = 0.0
        dt = 0.0

    glClear(GL_COLOR_BUFFER_BIT)

    # Lens
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0, 0.1, 1000.0)

    # World
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(20,20,20, 0,0,0, 0,1,0)

    glColor3f(1,0,0)
    drawLine(0, 0, 0, 10, 0, 0)
    glColor3f(0, 1, 0)
    drawLine(0, 0, 0,  0,10, 0)
    glColor3f(0, 0, 1)
    drawLine(0, 0, 0,  0, 0,10)

    glColor3f(1,1,1)

    if simulationStart :
        et = et + dt
        P1 = ball1 + ball1V * et + 0.5 * g * et**2
        P2 = ball2 + ball2V * et + 0.5 * g * et**2
        drawBall(P1)
        drawBall(P2)
    else:
        drawBall(ball1)
        drawBall(ball2)
    glFlush()

    dt = TimerGetDt()

GLinit()
RegisterCallbacks()
glutMainLoop()

# End of program