#!/usr/bin/python

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import math
from CONSTANTES import *

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

def physical_collision2(ball, other_ball) :
    i = [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]
    j = [other_ball.x, other_ball.x + other_ball.width, other_ball.y, other_ball.y + other_ball.height]
    dx = i[0] - j[0]
    dy = i[2] - j[2]

    dist = math.hypot(dx, dy)
    if dist < (i[1]-i[0])/2 + (j[1] - j[0])/2 :
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent
        
        ball.angle = 2 * tangent - ball.angle
        other_ball.angle = 2 * tangent - other_ball.angle

        ball.x += math.sin(angle)
        ball.y -= math.cos(angle)
        other_ball.x -= math.sin(angle)
        other_ball.y += math.cos(angle)

        b_vel = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
        o_vel = math.sqrt(other_ball.velocity_x**2 + other_ball.velocity_y**2)
                                                                                                           
        ball.velocity_x = math.sin(angle)*b_vel
        ball.velocity_y = -math.cos(angle)*b_vel
        other_ball.velocity_x = -math.sin(angle)*o_vel
        other_ball.velocity_y = math.cos(angle)*o_vel

        ball.set_col((1,0,1))
        other_ball.set_col((1,0,1))
        
        return True

def physical_wall_collisions2(ball, wall) :
    if (ball.x < wall.x and ball.velocity_x < 0) or (ball.right > wall.right and ball.velocity_x > 0):
        ball.velocity_x *= -1
    if (ball.y < wall.y and ball.velocity_y < 0) or (ball.top > wall.top and ball.velocity_y > 0):
        ball.velocity_y *= -1


def physical_collision(balls, other_balls, i, j) :
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
        
        return True

def physical_wall_collisions(balls, i, wall) :
    if (balls[i].x < wall.x and balls[i].velocity_x < 0) or (balls[i].right > wall.right and balls[i].velocity_x > 0):
        balls[i].velocity_x *= -1
    if (balls[i].y < wall.y and balls[i].velocity_y < 0) or (balls[i].top > wall.top and balls[i].velocity_y > 0):
        balls[i].velocity_y *= -1

