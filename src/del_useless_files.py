# -*- coding: utf-8 -*- 

#Permet de nettoyer le dossier data de tout les fichiers trop petits et pas interessant
#A lancer en fin de simulation ou a intégrer dans main pour qu'il se lance seul à la fin

import os
import shutil 
from CONSTANTES import * 

if os.path.exists("data"): 
    shutil.rmtree("data") #efface le dossier data pour supprimer les anciennes données
    
os.makedirs("data") # recrée le dossier data
 
def delete_useless_files(size = 1) : 
    
    all_data_files = os.listdir("data")
    nb_of_initial_files = len(all_data_files)   
    print ("Nombre de fichiers initial : " + str(nb_of_initial_files))
 
    for data_file_name in all_data_files: 
        data_file_stat = os.stat("data/"+ data_file_name) 
        if data_file_stat.st_size < size  : 
            os.remove("data/"+ data_file_name) 
     
    nb_of_final_files = len(os.listdir("data"))
    nb_of_deleted_files = nb_of_initial_files - nb_of_final_files
    print ("Nombre de fichiers après tri : " + str(nb_of_final_files))
    print ("Nombre de fichiers supprimés : " + str(nb_of_deleted_files))
 
delete_useless_files(MIN_SIZE_FOR_DATA) 


