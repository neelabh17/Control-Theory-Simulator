m=1
l=1
g=9.8
import numpy as np
import math
from numpy.linalg import inv
import cv2
from tqdm import tqdm
import matplotlib.pyplot as plt

def M(q):
    q1 = q[0]
    q2 = q[1]
    m11 = (m*l**2)/3 + m*l**2 + (m*l**2)/3 + (m*l**2)*math.cos(q2)
    m12 = (m*l**2)/3 + 0.5*(m*l**2)*math.cos(q2)


    m21 = (m*l**2)/3 + 0.5*(m*l**2)*math.cos(q2)
    m22 = (m*l**2)/3 
 
    _M = [[m11,m12],
        [m21,m22]]

    return np.array(_M)

def F(q,qd):
    q1 = q[0]
    q2 = q[1]
    q1d = qd[0]
    q2d = qd[1]  
 

    f1 = -(m*l**2)*math.sin(q2)*q1d*q2d -0.5*(m*l**2)*math.sin(q2)*q2d*q2d + 1.5*m*g*l*math.cos(q1) + 0.5*g*m*l*math.cos(q1+q2)

    f2 = -0.5*(m*l**2)*math.sin(q2)*q1d*q1d +0.5*m*l*g*math.cos(q1+q2)

    _F = [f1,
        f2]

    return np.array(_F).reshape(-1,1)