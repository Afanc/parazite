# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Bouncing balls 
"""
from random import *

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import math
from datetime import datetime
from quadtree import Quadtree
import cProfile

DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100


class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)         #if it's float or int, doesn't work
    velocity_y = NumericProperty(0)
    angle = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    #@profile
    def update(self,dt):

        quad = Quadtree(0,[self.x,self.x + self.width, self.y, self.y + self.height])
        quad.reset()    #est-ce que ça sert à rien ?
        balls = {}

        for c in self.children: 
            if isinstance(c,Ball) :
                balls[(c.x, c.x + c.width, c.y, c.y + c.height)] = c   #key : position, access : ball

        for i in balls :         #donc là ça fait n
            quad.insert(i) 

        for i in balls:                                         #for each key (=position)
            temp_keys = quad.fetch(i)
            other_balls = {key:balls[key] for key in temp_keys} #on crée un nouveau dico avec que les collisions

            for j in other_balls:
                
                dx = i[0] - j[0]
                dy = i[2] - j[2]

                dist = math.hypot(dx, dy)
                if dist < (i[1]-i[0])/2 + (j[1] - j[0])/2 :
                    tangent = math.atan2(dy, dx)
                    angle = 0.5 * math.pi + tangent
                    
                    balls[i].angle = 2 * tangent - balls[i].angle
                    other_balls[j].angle = 2 * tangent - other_balls[j].angle

                    balls[i].x += math.sin(angle)
                    balls[i].y -= math.cos(angle)
                    other_balls[j].x -= math.sin(angle)
                    other_balls[j].y += math.cos(angle)

                    b_vel = math.sqrt(balls[i].velocity_x**2 + balls[i].velocity_y**2)
                    o_vel = math.sqrt(other_balls[j].velocity_x**2 + other_balls[j].velocity_y**2)

                    balls[i].velocity_x = math.sin(angle)*b_vel
                    balls[i].velocity_y = -math.cos(angle)*b_vel
                    other_balls[j].velocity_x = -math.sin(angle)*o_vel
                    other_balls[j].velocity_y = math.cos(angle)*o_vel
        balls = []
        for c in self.children:     
            if isinstance(c,Ball) :
                balls.append(c)
        
        for ball in balls:
            if (ball.x < self.x and ball.velocity_x < 0) or (ball.right > self.right and ball.velocity_x > 0):
                ball.velocity_x *= -1
            if (ball.y < self.y and ball.velocity_y < 0) or (ball.top > self.top and ball.velocity_y > 0):
                ball.velocity_y *= -1

            #-------------- update balls here -----------------
            ball.update(dt)
            #-------------- update balls here -----------------

        #print datetime.now() - startTime


    def start_balls(self):
        for i in range(0,50):
            ball = Ball()
            r = randint(-100,100)               #placement aléatoire à faire MIEUX
            ball.center = (400+r,400+r)
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)

class Gui1App(App):
    """Represents the whole application."""
    def build(self):
        """Entry point for creating app's UI."""
        root = BallsContainer()
        root.start_balls()
        Clock.schedule_interval(root.update, DELTA_TIME)
        return root

if __name__ == '__main__':
    Gui1App().run()
