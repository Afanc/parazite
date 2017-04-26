#choix_test = raw_input("Quelles variables voulez-vous tester\n")
choix_xls = raw_input("Voulez-vous enregistrer les resultats dans un fichier xls separe ?\n"
                      "0 = Non\n"
                      "1 = Oui\n")

try :
    number_of_particles = raw_input("Nombre d'hotes sains au depart : (env. 200) \n") #200
    number_of_particles = int(number_of_particles)
    #number_of_particles_resistant = raw_input("Definissez la probabilite de mortalite des hotes sains (en chance sur 10000 par cycle)\n")10
    number_of_particles_infected = raw_input("Nombre d'hotes infectes au depart (env. 10)\n") #10
    number_of_particles_infected = int(number_of_particles_infected)
    population_max = raw_input("Nombre maximal d'hotes que peut supporter ce milieu (env. 300) \n") #300
    population_max = int(population_max)

    sane_mortality = raw_input("Probabilite de mortalite des hotes sains (en chance sur 10000 par cycle) env. 5\n ") #5
    sane_mortality = int(sane_mortality)
    sane_fertility = raw_input("Probabilite de se dupliquer des hotes sains (en chance sur 10000 par cycle) env. 40\n") #40
    sane_fertility = int(sane_fertility)
    dead_but_contagious_time = raw_input("Probabilite qu'un parasite survivent sur un cadavre (en chance sur 10000 par cycle) env. 500\n" ) #500
    dead_but_contagious_time = int(dead_but_contagious_time)
    #print("Valeurs choisies :\n" + "- nb d'hotes sains initial : " + number_of_particles + "\n")
         # +"- nb d'infectes initial: " + str(number_of_particles_infected) + "\n"
         # +"- nb max d'individus : " + str(population_max) + "\n"
          #+"- mortalite des hotes sains: " + str(sane_mortality) + "\n"
          #+"- fertilite des hotes sains : " + str(sane_fertility) +"\n")
except :
    number_of_particles = 200
    number_of_particles_infected = 10
    population_max = 300
    sane_mortality = 5
    sane_fertility = 40
    dead_but_contagious_time = 10


infected_mortality_range_test = range(10,110,10)
infectiosity_value_range_test = range(5,105,5)

