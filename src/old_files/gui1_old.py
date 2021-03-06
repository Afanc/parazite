# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Bouncing balls 
"""
from random import *

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import math
from datetime import datetime
import cProfile


BASE_COLOR = [0,0,1]

class MyApp(App):
    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')


DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 0.5


class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)         #if it's float or int, doesn't work
    velocity_y = NumericProperty(0)
    angle = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    col = ListProperty(BASE_COLOR)

    
    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos

    #@profile
    def collide(self,p2):
        #calcul de la distance entre le centre des particules
        dx = self.x - p2.x
        dy = self.y - p2.y
        dist = math.hypot(dx, dy)
        
        # comportement physique des particules en cas de collision
        if dist < self.size[0]/2 + p2.size[0]/2 :
            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent

            self.angle -= 2 * tangent
            p2.angle -= 2 * tangent

            #self.x += math.sin(angle)
            #self.y -= math.cos(angle)
            self.velocity_x += math.sin(angle)
            self.velocity_y -= math.cos(angle)
            p2.velocity_x -= math.sin(angle)
            p2.velocity_y += math.cos(angle)

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def old_update(self,dt):

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
                if dist <= float(i[1]-i[0])/2 + float(j[1] - j[0])/2 :
                    tangent = math.atan2(dy, dx)
                    angle = 0.5 * math.pi + tangent

                    balls[i].angle -= 2 * tangent
                    other_balls[j].angle -= 2 * tangent

                    angle = 0.5 * math.pi + tangent

                    balls[i].velocity_x += math.sin(angle)
                    balls[i].velocity_y -= math.cos(angle)
                    other_balls[j].velocity_x -= math.sin(angle)
                    other_balls[j].velocity_y += math.cos(angle)

                    other_balls[j].update(dt)

                balls[i].update(dt)

        balls = []
        for c in self.children:     
            if isinstance(c,Ball) :
                balls.append(c)
        
        for ball in balls:
            if (ball.x < self.x and ball.velocity_x < 0) or (ball.right > self.right and ball.velocity_x > 0):
                ball.velocity_x *= -1
            if (ball.y < self.y and ball.velocity_y < 0) or (ball.top > self.top and ball.velocity_y > 0):
                ball.velocity_y *= -1
            



    #@profile
    def update(self, dt):
        balls = []
        for c in self.children:     #pour tous les enfants
            if isinstance(c,Ball) : #si ce sont des balles equiv à #balls = (c for c in self.children if isinstance(c, Ball))
                balls.append(c)
        
        for ball in balls:
            #bounce ball off left or right
            if (ball.x < self.x and ball.velocity_x < 0) or (ball.right > self.right and ball.velocity_x > 0):       # (note: X axis is pointing *right*, Y axis is pointing *up*)
                ball.velocity_x *= -1
            #bounce ball off bottom or top
            if (ball.y < self.y and ball.velocity_y < 0) or (ball.top > self.top and ball.velocity_y > 0):
                ball.velocity_y *= -1
            
            #bounce other balls --- N^2 c'est moche change it
            for other_ball in balls:
                ball.collide(other_ball)
                other_ball.update(dt)

            ball.update(dt)

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
