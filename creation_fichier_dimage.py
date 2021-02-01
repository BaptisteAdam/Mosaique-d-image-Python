"""
Projet - Traitement d'images
création fichier d'images
"""

import os
import sys
from operator import itemgetter
from PIL import Image


def scand(path):
    """
    retourne la liste des fichiers dans le repertoire passé en parametres
    """
    return [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]

def creation_fichier_rgb(repertoire_file, repertoire):
    """
    Crée un fichier txt contenant les informations de toute les images du repertoire
    apres les avoir traitées en RGB.
    """
    list_file = scand(repertoire)
    with open(repertoire_file, mode='w', encoding='utf8') as file:
        for indice, image_name in enumerate(list_file):
            if (indice+1)%(10) == 0:
                sys.stdout.write("- creation : "+str(indice+1)+"/"+str(len(list_file))+" -"+chr(13))
            image = os.path.join(repertoire, image_name)
            im_file = Image.open(image)
            im_file = im_file.convert("RGB")
            pix = im_file.load()
            sum_r, sum_g, sum_b, compteur = 0, 0, 0, 0
            for i in range(im_file.size[0]):
                for j in range(im_file.size[1]):
                    red, green, blue = pix[i, j]
                    sum_r += red
                    sum_g += green
                    sum_b += blue
                    compteur += 1
            moy_r, moy_g, moy_b = sum_r//compteur, sum_g//compteur, sum_b//compteur
            file.write(str(moy_r)+";"+str(moy_g)+";"+str(moy_b)+";"+image+"\n")
            im_file.close()

def creation_fichier_hsv(repertoire_file, repertoire):
    """
    Crée un fichier txt contenant les informations de toute les images du repertoire
    apres les avoir traitées en HSV.
    """
    list_file = scand(repertoire)
    with open(repertoire_file, mode='w', encoding='utf8') as file:
        for indice, image_name in enumerate(list_file):
            if (indice+1)%(10) == 0:
                sys.stdout.write("- creation : "+str(indice+1)+"/"+str(len(list_file))+" -"+chr(13))
            image = os.path.join(repertoire, image_name)
            im_file = Image.open(image)
            im_file = im_file.convert("RGB").convert("HSV")
            pix = im_file.load()
            list_nbr_moy = []
            saturation = 0
            moy = 0
            value = 0
            nbr_rouge1, nbr_rouge2, nbr_orange, nbr_jaune, nbr_vert, nbr_vert_bleu, nbr_cyan, nbr_bleu, nbr_magenta, nbr_violet = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            moy_rouge1, moy_rouge2, moy_orange, moy_jaune, moy_vert, moy_vert_bleu, moy_cyan, moy_bleu, moy_magenta, moy_violet = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

            for i in range(im_file.size[0]):
                for j in range(im_file.size[1]):
                    hue, sat, val = pix[i, j]
                    saturation += sat
                    value += val
                    moy += 1

                    if 0 <= hue <= 20:
                        nbr_rouge1 += 1
                        moy_rouge1 += hue
                        continue
                    if 340 < hue <= 360:
                        nbr_rouge1 += 1
                        moy_rouge2 += hue
                        continue
                    if 20 < hue <= 60:
                        nbr_orange += 1
                        moy_orange += hue
                        continue
                    if 60 < hue <= 100:
                        nbr_jaune += 1
                        moy_jaune += hue
                        continue
                    if 100 < hue <= 140:
                        nbr_vert += 1
                        moy_vert += hue
                        continue
                    if 140 < hue <= 180:
                        nbr_vert_bleu += 1
                        moy_vert_bleu += hue
                        continue
                    if 180 < hue < 220:
                        nbr_cyan += 1
                        moy_cyan += hue
                        continue
                    if 220 < hue <= 260:
                        nbr_bleu += 1
                        moy_bleu += hue
                        continue
                    if 260 < hue <= 300:
                        nbr_magenta += 1
                        moy_magenta += hue
                        continue
                    if 300 < hue <= 340:
                        nbr_violet += 1
                        moy_violet += hue
                        continue

            if nbr_rouge1 != 0:
                moy_rouge1 = moy_rouge1//nbr_rouge1
            if nbr_rouge2 != 0:
                moy_rouge2 = moy_rouge2//nbr_rouge2
            if nbr_orange != 0:
                moy_orange = moy_orange//nbr_orange
            if nbr_jaune != 0:
                moy_jaune = moy_jaune//nbr_jaune
            if nbr_vert != 0:
                moy_vert = moy_vert//nbr_vert
            if nbr_vert_bleu != 0:
                moy_vert_bleu = moy_vert_bleu//nbr_vert_bleu
            if nbr_cyan != 0:
                moy_cyan = moy_cyan//nbr_cyan
            if nbr_bleu != 0:
                moy_bleu = moy_bleu//nbr_bleu
            if nbr_magenta != 0:
                moy_magenta = moy_magenta//nbr_magenta
            if nbr_violet != 0:
                moy_violet = moy_violet//nbr_violet

            moy_rouge = 0
            if nbr_rouge1 > nbr_rouge2:
                moy_rouge = moy_rouge1
            else:
                moy_rouge = moy_rouge2
            nbr_rouge = nbr_rouge1 + nbr_rouge2

            saturation = saturation//moy
            value = value//moy

            list_nbr_moy = [[nbr_rouge, moy_rouge], [nbr_orange, moy_orange], [nbr_vert, moy_rouge1], [moy_vert, moy_rouge1], [nbr_vert_bleu, moy_vert_bleu], [nbr_cyan, moy_cyan], [nbr_bleu, moy_bleu], [nbr_magenta, moy_magenta], [nbr_violet, moy_violet]]
            list_nbr_moy.sort(key=itemgetter(0), reverse=True)
            file.write(str(list_nbr_moy[0][1])+";"+str(saturation)+";"+str(value)+";"+image+"\n")

            im_file.close()

#repertoire = "./Cat"
#file = "traitement images-2.txt"
#creation_fichier(file, repertoire)
