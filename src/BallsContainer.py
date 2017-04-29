# -*- coding: utf-8 -*-
#!/usr/bin/python

from random import *

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import math
from datetime import datetime
from quadtree import Quadtree
from CONSTANTES import *

class mainApp(App):                                                                                                    
    """Represents the whole application."""
    def build(self):
        """Entry point for creating app's UI."""
        root = BallsContainer()
        Clock.schedule_once(root.start_balls,1)         #on attend que la fenêtre soit lancée
        Clock.schedule_interval(root.update, DELTA_TIME)
        return root

class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)         #if it's float or int, doesn't work
    velocity_y = NumericProperty(0)
    angle = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    col = ListProperty (BASE_COLOR)
    
    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos

    def get_col(self):
        return self.col
    def set_col(self, a):
        self.col = a


class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def start_balls(self,dt):
        for i in range(0,50):
            ball = Ball()
            ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)

    #@profile
    def update(self,dt):
        quad = Quadtree(0,[self.x,self.x + self.width, self.y, self.y + self.height])
        quad.reset()    #est-ce que ça sert à rien ?
        balls = {}

        for c in self.children: 
            if isinstance(c,Ball) :
                balls[(c.x, c.x + c.width, c.y, c.y + c.height)] = c   #key : position, access : ball

        for i in balls :                                        #obligés de faire un 1e boucle pour toutes les placer
            if balls[i].get_col() != BASE_COLOR:                #petit hack pour les couleurs, on profite des boucles
                balls[i].set_col(BASE_COLOR)

            quad.insert(i)                                      #préparer le quad

        for i in balls:                                         #for each key (=position)
            temp_keys = quad.fetch(i)                           #on fetch les collisions
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

                    balls[i].set_col((1,0,1))
                    other_balls[j].set_col((1,0,1))

            #walls
            if (balls[i].x < self.x and balls[i].velocity_x < 0) or (balls[i].right > self.right and balls[i].velocity_x > 0):
                balls[i].velocity_x *= -1
            if (balls[i].y < self.y and balls[i].velocity_y < 0) or (balls[i].top > self.top and balls[i].velocity_y > 0):
                balls[i].velocity_y *= -1

            #-------------- update balls here -----------------
            balls[i].update(dt)
            #-------------- update balls here -----------------


