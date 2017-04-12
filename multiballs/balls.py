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


DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 1


class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    angle = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos

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

            angle = 0.5 * math.pi + tangent

            #self.x += math.sin(angle)
            #self.y -= math.cos(angle)
            self.velocity_x += math.sin(angle)
            self.velocity_y -= math.cos(angle)
            p2.velocity_x -= math.sin(angle)
            p2.velocity_y += math.cos(angle)

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def update(self, dt):
        balls = []
        for c in self.children:
            if isinstance(c,Ball) :
                balls.append(c)
        #balls = (c for c in self.children if isinstance(c, Ball))
        for ball in balls:
            # bounce of walls
            # (note: Y axis is pointing *up*)
            if ball.x < 0 or ball.right > self.width:
                ball.velocity_x *= -1
            if ball.y < 0 or ball.top > self.height:
                ball.velocity_y *= -1

            #bounce other balls
            for other_ball in balls:
                ball.collide(other_ball)
                other_ball.update(dt)

            ball.update(dt)

#    def on_touch_up(self, touch):
#        """Touch (or click) 'up' event: releasing the mouse button
#        or lifting finger.
#     f   """
#        ball = Ball()
#        ball.center = (touch.x, touch.y)
#        ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),
#                         -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
#        self.add_widget(ball)

    def start_balls(self):
        for i in range(0,100):
            ball = Ball()
            r = randint(-100,100)
            ball.center = (400+r,400+r)
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)

class BallsApp(App):
    """Represents the whole application."""

    def build(self):
        """Entry point for creating app's UI."""
        root = BallsContainer()
        root.start_balls()
        Clock.schedule_interval(root.update, DELTA_TIME)
        return root


if __name__ == '__main__':
    BallsApp().run()
