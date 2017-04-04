from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import Color, Ellipse, Rectangle


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongBall2(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    print type(ball)
    print type(ball2)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
    def serve_ball2(self):
        self.ball2.center = self.center
        self.ball2.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()
    def update2(self, dt):
        self.ball2.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # bounce off top and bottom
        if (self.ball2.y < 0) or (self.ball2.top > self.height):
            self.ball2.velocity_y *= -1

        # bounce off left and right
        if (self.ball2.x < 0) or (self.ball2.right > self.width):
            self.ball2.velocity_x *= -1


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        game.serve_ball2()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.update2, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
