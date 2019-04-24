import math
import numpy as np


#로컬벡터(지역 좌표계)
#글로벌벡터 (전역 좌표계)
def local2global(angle, vec) : ##로컬 벡터를 글로벌 벡터로 변환 지역좌표계를 전역좌표계로 바꿀때는 변경 각 만큼 좌표에 곱해준다.
    c = math.cos(angle)
    s = math.sin(angle)
    x = c*vec[0] -s*vec[1]
    y = s*vec[0] +c*vec[1]
    return np.array([x,y,0.0])

def rad2deg(rad) :
    return 180.0*(rad/3.141592)

def deg2rad(deg) :
    return 3.141592*(deg/180.0)