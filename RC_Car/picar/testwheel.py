# -*- coding: utf-8 -*-

import front_wheels as fw

import back_wheels as bw

 

def test():

    import random as rd

    import time

    back_wheels = bw.Back_Wheels()

    front_wheels = fw.Front_Wheels(channel=0)

    x,y = 0,0

    back_wheels.backward()

##    for i in range(0,100):

##        x = rd.randrange(-1,2)

##        y = rd.randrange(-1,2)

##        if x == -1:

##            front_wheels.turn_right()

##        elif x == 0:

##            front_wheels.turn_straight()

##        else:

##            front_wheels.turn_left()

##        s = rd.randrange(30,70)

##        back_wheels.speed = s

##        print "frontward, speed =", x

##        print "Backward, speed =", s

##        time.sleep(0.5)

    back_wheels.stop()

 

if __name__ == "__main__":

    test()
