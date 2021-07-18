import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from control import controller
from numpy.linalg import inv
from resources.physics import M, F
def simulate():

    def T(q,qd,t,trajectories):
        q1 = q[0][0]
        q2 = q[1][0]
        w1 = qd[0][0]
        w2 = qd[1][0]
        q1_desired = trajectories[0](t) 
        q2_desired = trajectories[1](t)

        t1, t2 = controller(q1, q2, w1, w2, q1_desired, q2_desired)
        return np.array([t1,t2]).reshape(-1,1)

    def getImage(q, videoWriter, img):
        q1 = q[0]
        q2 = q[1]

        cv2.circle(img, (int(250+ 100*math.cos(q1)+100*math.cos(q1+q2)),int(300 - 100*math.sin(q1)- 100*math.sin(q1+q2))),0, (0,0,255) ,-1)
        new_img=img.copy()
        cv2.line(new_img,(250,300),(int(250+ 100*math.cos(q1)),int(300 - 100*math.sin(q1))),(255,0,0),5, lineType=cv2.LINE_AA)
        cv2.line(new_img,(int(250+ 100*math.cos(q1)),int(300 - 100*math.sin(q1))), (int(250+ 100*math.cos(q1)+100*math.cos(q1+q2)),int(300 - 100*math.sin(q1)- 100*math.sin(q1+q2))),(0,255,0),5, lineType=cv2.LINE_AA)
        videoWriter.write(new_img)
        return img

    def getRefImage(img, videoWriter, t, trajectories, addFrame):
        q1 = trajectories[0](t)
        q2 = trajectories[1](t)

        cv2.circle(img, (int(250+ 100*math.cos(q1)+100*math.cos(q1+q2)),int(300 - 100*math.sin(q1)- 100*math.sin(q1+q2))),0, (0,0,0) ,-1)
        if(addFrame):
            videoWriter.write(img)
        return img
    experiments = ["PS1_stand_still", "PS2_extended_circle", "PS3_vertical_circle"]
    trajectories = {
        "PS1_stand_still": [lambda t: math.pi/2, lambda t: 0],
        "PS2_extended_circle": [lambda t: math.pi*t/2000, lambda t: 0],
        "PS3_vertical_circle": [lambda t: math.pi*t/2000, lambda t: math.pi/2 - math.pi*t/2000],

    }


    for key in experiments:
        out = cv2.VideoWriter('{}.avi'.format(key),cv2.VideoWriter_fourcc(*'DIVX'), 120, (500,600))
        blank_canvas = img = np.ones((600, 500, 3), np.uint8)*244

        q0 = np.array([-math.pi/2,math.pi]).reshape(-1,1)
        qd0 = np.array([0.1,0]).reshape(-1,1)

        q=q0
        qd=qd0

        t_sampling = 0.001

        
        for k in tqdm(range(4000), desc="Creating {}'s reference trajectory".format(key)):
            if(k<4000 and k%2==0):
                if(k%20==0):
                    addFrame=True
                else:
                    addFrame=False
                blank_canvas = getRefImage(blank_canvas, out, k, trajectories[key], addFrame) 

        for k in tqdm(range(10000), desc="Creating {}'s control trajectory".format(key)):
            q_k=q
            if(k<4000 and k%2==0):
                blank_canvas= getImage(q_k, out, blank_canvas)
            qd_k=qd
            tau_k = T(q,qd,k, trajectories[key])
            
            q = q_k + t_sampling * qd_k
            qd = qd + t_sampling* np.dot(inv(M(q_k)), (tau_k - F(q_k, qd_k) ))

        out.release()