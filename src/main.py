# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

#from BallsContainer import *
from parazite1 import *
from healthy import *
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import math
from datetime import datetime
from quadtree import Quadtree
from CONSTANTES import *

# -------------------- balls container--------------------

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

            
#-----------------------main --------------------------
seed(42)

dico_id = {}    #on ajoute les id de individu dans le dico
list_of_freed_id = [] # on ajoute les id des mort à cette liste

list_of_healhies = []
list_of_parazites = []

def create_id():
    if len(list_of_freed_id) == 0:
        idd = "ID" + str(len(dico_id))
        #regarder si la clé idd est unique dans le dico
    else: 
        idd = list_of_freed_id[-1]
    return idd
    
def add_healthy(nb_sains = NB_SAINS):
    for i in range(nb_sains):
        x = randint(0, MAX_VELOCITY)
        try:
        
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_healhies.append(Healthy([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)], [x , MAX_VELOCITY- x], temp))
                dico_id[temp] = list_of_healhies[-1]
        except: 
            print "could not add health: ID problem"
            
      
def add_parazite(nb_parasite=NB_PARASITE):
    for i in range(nb_parasite):
        x = randint(0, MAX_VELOCITY)
        try:
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_parazites.append(Parazite([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)],randint(0,MAX_VELOCITY), randint(0, MAX_VIRULANCE),1,1, temp))    #changer attributs
                dico_id[temp] = list_of_parazites[-1]
        except: 
            print "could not add parazite: ID problem"
            
            
def start(nb_sains=NB_SAINS, nb_parasite=NB_PARASITE):
    add_healthy()
    add_parazite()

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if random.randrange(0,100) < INFECT_CHANCE:
                nb_parasite    # à faire

def kill(p):
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
        return
    elif isinstance(p, Healthy):
        list_of_healhies.remove(p)
        list_of_freed_id.append(p.getIdd())
        del dico_id[p.getIdd()]
        del p
    elif isinstance(p, Parazite):
        list_of_parazites.remove(p)
        list_of_freed_id.append(p.getIdd())
        del dico_id[p.getIdd()] 
        del p


def guerison(p):
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
    if isinstance(p, Parazite):
        speed = p.getSpeed()
        pos = p.getPosition()
        idd = p.getIdd()
        hourglass = p.getHourglass()
        list_of_healhies.append(Healthy(pos, speed, idd, hourglass))
        list_of_parazites.remove(p)
        del p
        
    
def main():
    print 'le programme de sa mère\n'
    
#start()
if __name__ == '__main__':                                                                                             
    #Gui1App().run()
    print "bravo"



add_healthy(2)
print "A" + str(list_of_healhies[0].getIdd())
print "B" + str(list_of_freed_id)
print "C" + str(dico_id)

kill(list_of_healhies[1])
print "D" + str(list_of_healhies)
print "E" + str(list_of_freed_id)
print "F" + str(dico_id)

#actions_when_collision(list_of_parazites[1],list_of_healhies[2])    #test


#-----------------------------Kivy GUI-----------------------------------------------
if __name__ == '__main__':  
    mainApp().run()
#-----------------------------Kivy GUI-----------------------------------------------


