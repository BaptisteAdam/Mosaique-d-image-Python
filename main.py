"""
Projet - Traitement d'images
Main
"""
import time
import sys
from PIL import Image
import mosaique_par_decoupage as mos
import creation_fichier_dimage as crea

REPERTOIRE = "./Cat"
REPERTOIRE_FILE_RGB = "traitement images RGB.txt"
REPERTOIRE_FILE_HSV = "traitement images HSV.txt"
STOP = False

TRAITEMENT_TYPE = input("RGB ou HSV ? (RGB si laissé vide)\n>>> ")
REPONSE = input("Voulez vous générez les informations de la bibliotheque d'image ? oui/non\n>>> ")

#Création des données sur le repertoire
if REPONSE == "oui":
    REPERTOIRE = input("Entrez le repertoire de la bibliotheque d'images\n>>> ")
    try:
        if TRAITEMENT_TYPE == "HSV" or TRAITEMENT_TYPE == "hsv":
            crea.creation_fichier_hsv(REPERTOIRE_FILE_HSV, REPERTOIRE)
        else:
            crea.creation_fichier_rgb(REPERTOIRE_FILE_RGB, REPERTOIRE)
    except FileNotFoundError as error_1:
        print("Ce repertoire n'existe pas.")
        print(error_1)
        STOP = True
elif REPONSE != "non":
    print("ceci n'est pas une reponse valide")
    STOP = True
if STOP:
    sys.exit()

IMAGE = input("quelle image voulez vous traiter ?\n>>> ")

#Choix des paramètres
PRECISION = 20 #normale
PRECISION_TYPE = input("Choisissez la précision : petite/normale/grande\n>>> ")
if PRECISION_TYPE == "petite" or PRECISION_TYPE == "petit":
    PRECISION = 30
elif PRECISION_TYPE == "grande" or PRECISION_TYPE == "grand":
    PRECISION = 10

TAILLE = 50 #normale
TAILLE_TYPE = input("Choisissez la taille de la mosaïque : petite/normale/grande\n>>> ")
if TAILLE_TYPE == "petite" or TAILLE_TYPE == "petit":
    TAILLE = 20
elif TAILLE_TYPE == "grande" or TAILLE_TYPE == "grand":
    TAILLE = 100

#Debut du traitement
try:
    TEMPS1 = time.time()
    IM_O = Image.open(IMAGE)
    if TRAITEMENT_TYPE == "HSV" or TRAITEMENT_TYPE == "hsv":
        MOSAIQUE = IMAGE[:len(IMAGE)-4] + "_m_hsv.jpg"
        RESULTATS = mos.mosaique(REPERTOIRE_FILE_HSV, IM_O, TAILLE, PRECISION, True)
    else:
        MOSAIQUE = IMAGE[:len(IMAGE)-4] + "_m_rgb.jpg"
        RESULTATS = mos.mosaique(REPERTOIRE_FILE_RGB, IM_O, TAILLE, PRECISION, False)
    RESULTATS.save(MOSAIQUE)
    TEMPS2 = time.time()-TEMPS1
    print("Temps d'execution = %f min" %(TEMPS2/60))
except FileNotFoundError as error_2:
    print("Ce fichier n'existe pas.")
    print(error_2)


