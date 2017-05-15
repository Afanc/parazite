# -*- coding: utf-8 -*- 

#Permet de nettoyer le dossier data de tout les fichiers trop petits et pas interessant
#A lancer en fin de simulation ou a intégrer dans main pour qu'il se lance seul à la fin

import os
from CONSTANTES import * 

 
def delete_useless_files(nb_of_files_to_keep = 5) : 
    
    all_data_files = os.listdir("data")
    list_of_all_data_size = []
    nb_of_initial_files = len(all_data_files)   
    print ("Nombre de fichiers initial : " + str(nb_of_initial_files))
    
    try:
        
        for data_file_name in all_data_files: 
            data_file_stat = os.stat("data/"+ data_file_name)
            list_of_all_data_size.append(data_file_stat.st_size)
            
        list_of_all_data_size.sort()
        min_size = list_of_all_data_size[-nb_of_files_to_keep]

           
        for data_file_name in all_data_files: 
            data_file_stat = os.stat("data/"+ data_file_name)     
            if data_file_stat.st_size < min_size  : 
                os.remove("data/"+ data_file_name) 
    except:
        pass
    
    nb_of_final_files = len(os.listdir("data"))
    nb_of_deleted_files = nb_of_initial_files - nb_of_final_files
    print ("Nombre de fichiers après tri : " + str(nb_of_final_files))
    print ("Nombre de fichiers supprimés : " + str(nb_of_deleted_files))
 
delete_useless_files(NB_FILES_TO_KEEP) 


