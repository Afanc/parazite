# -*- coding utf-8 -*-

# @ Bastien Vallat
# bastien.vallat@unil.ch

import pygame
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
import csv

background_colour = (255, 255, 255)
(width, height) = (600, 600)
random.seed(186)

# Cree un fichier csv pour y ecrire le nombre de particules par classe par nombre de cycles 
# dans la boucle while principale
#c = csv.writer(open("parasites_data.csv", "wb"))

#Tentative d'ajouter un timer pour controler la duree avant un changement de classe( par ex infecte -> mort )
#def decompte_temps(period):
    #nexttime = time.time() + period
    #for i in count():
        #now = time.time()
        #tosleep = nexttime - now
        #if tosleep > 0:
            #time.sleep(tosleep)
            #nexttime += period
        #else:
            #nexttime = now + period
        #yield i, nexttime


# Met les particules en mouvement au debut de la simulation        
def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None

# Regle sur les collisions des particules et la transmission du parasite/maladie 
def collide(p1, p2):
    
    #Pas de collision contre une particule morte
    if (p1.state != "mort") and (p2.state != "mort"):  

        dx = p1.x - p2.x
        dy = p1.y - p2.y
        
        #calcul de la distance entre le centre des particules
        dist = math.hypot(dx, dy)
        
        #probabilite d'infection concernant l'infection en cas de collision
        #valade si les 2 particules ne sont pas dans l'etat "mort"
        if dist < p1.size + p2.size and p2.state != "mort"  and p2.state != "mort_mais_contagieux" \
                and (p1.state == "malade" or p1.state == "mort_mais_contagieux"):
            chance_transmission = random.randint(1,100)
            if chance_transmission < 90 :
                p2.state = "malade"

        if dist < p1.size + p2.size and p1.state != "mort" and p1.state != "mort_mais_contagieux" \
                and (p2.state == "malade" or p2.state == "mort_mais_contagieux"):
            chance_transmission = random.randint(1, 100)
            if chance_transmission < 90:
               p1.state = "malade"

        # comportement physique des particules en cas de collision
        if dist < p1.size + p2.size :
            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent

            angle1 = 2 * tangent - p1.angle
            angle2 = 2 * tangent - p2.angle
            #speed1 = p2.speed #* elasticity
            #speed2 = p1.speed #* elasticity

            #(p1.angle, p1.speed) = (angle1, speed1)
            #(p2.angle, p2.speed) = (angle2, speed2)

            p1.angle = angle1
            p2.angle = angle2

            p1.x += math.sin(angle)
            p1.y -= math.cos(angle)
            p2.x -= math.sin(angle)
            p2.y += math.cos(angle)

class Particle():
    def __init__(self, (x, y), size, colour, state):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.thickness = 0
        self.speed = 1
        self.angle = 0
        self.state = state # 4 etats : sain, malade, mort_mais_contagieux, mort

    #Dessine la particule
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), (0,0))
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        #self.speed *= drag
    
    #Rebondissement des particules contre les bords
    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            #self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            #self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            #self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            #self.speed *= elasticity

    #etat des particules : sain, malade, mort_mais_contagieux, mort        
    def etat(self):
        if self.state == "mort":
            self.speed = 0
            self.size = 5
            self.colour = (0, 0, 0)

        if self.state == "sain":
            chance_duplication = random.randint(0, 100000)
            chance_mort_sain = random.randint(0, 10000)
            if chance_mort_sain < 5:
                self.state == "mort"

            if chance_duplication < 400 :
                new_particle = Particle((self.x , self.y), self.size, self.colour, self.state)
                new_particle.state = "sain"
                new_particle.angle = random.uniform(0, math.pi * 2)
                new_particle.colour = (0,200,200)
                my_particles.append(new_particle)


        if self.state == "malade":
            self.colour = (200,0,0)
            self.speed *= 0.999
            chance_mort_malade = random.randint(0,1000)
            if chance_mort_malade < 10:
                self.state = "mort_mais_contagieux"

        if self.state == "mort_mais_contagieux":
            self.size = 5
            self.speed = 0
            self.colour = (0,100,0)
            chance_mort_contagieux = random.randint(0,1000)
            if chance_mort_contagieux < 50:
                self.state = "mort"

pygame.font.init()
screen = pygame.display.set_mode((width, height))

#Tentative d'ajouter du texte a l'ecran
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
#myfont = pygame.font.SysFont("monospace", 15)

# render text
#label = myfont.render("Some text!", 1, (255,255,0))
#screen.blit(label, (100, 100))

#Titre de la fenetre du programme
pygame.display.set_caption('Parasites_sim')

#Nombre initial de particules saines, malades ou resistantes(pas encore fait)
number_of_particles =300
number_of_particles_resistant = 10
number_of_particles_infected = 10
my_particles = []


#Creation des particules au lancement du programme
for n in range(number_of_particles):
    size = 10 #random.randint(10, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    colour = (0,0,200)
    if n < number_of_particles_infected :
        state="malade"
    else:
        state="sain"

    particle = Particle((x, y), size, colour, state)
    particle.angle = random.uniform(0, math.pi * 2)

    my_particles.append(particle)



selected_particle = None
running = True

# Variable utilise dans la boucle principale
nb_de_cycles = 0
plot_cycle = []
plot_liste_sain = []
plot_liste_malade = []
plot_liste_mort = []
plot_liste_mmc = []

#Boucle principale
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            plt.show() # Affiche un grahique du nombre de particule si clic gauche
            selected_particle = None

    if selected_particle:
        #(mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour) #efface particules apres mouvement

    #Variables pour le calcul du nombre de particules en temps reel (pas la somme totale)
    #Elles doivent etre remise a zero a chaque cycle
    nb_sain = 0
    nb_malade = 0
    nb_mort = 0
    nb_mort_mais_contagieux = 0

    # Verifie et incremente le nombre de particules
    for i, particle in enumerate(my_particles):
        if particle.state == "malade":
            nb_malade += 1
        if particle.state == "sain":
            nb_sain += 1
        if particle.state == "mort_mais_contagieux":
            nb_mort_mais_contagieux += 1
        if particle.state == "mort":
            nb_mort += 1

        particle.move()
        particle.bounce()
        particle.etat()
        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)
        particle.display()

    nb_de_cycles += 1 
    
    #Calcul du nombre de particules dans la simulation
    if nb_de_cycles % 50 == 0:

        plot_cycle.append(nb_de_cycles)
        plot_liste_sain.append(nb_sain)
        plot_liste_malade.append(nb_malade)
        plot_liste_mort.append(nb_mort)
        plot_liste_mmc.append(nb_mort_mais_contagieux)

        x = np.array(plot_cycle)
        y1 = np.array(plot_liste_sain)
        y2 = np.array(plot_liste_malade)
        y3 = np.array(plot_liste_mort)
        y4 = np.array(plot_liste_mmc)
        plt.plot(x, y1, "b")
        plt.plot(x, y2, "r")
        #plt.plot(x, y3, "black")
        plt.plot(x, y4, "g")
        
        #inscrit le nombre de particules tous les 50 cycles dasn un fichier csv
        #c.writerow([nb_de_cycles, nb_sain, nb_malade, nb_mort])

    pygame.display.flip() #Rafraichissement de l'ecran


