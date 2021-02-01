"""
Projet - Traitement d'images
Mosaïque d'images
"""

import sys
from operator import itemgetter
from random import choice as choice
from PIL import Image


def resize(im, dec):
    """
    redimentionne l'image avec les dimentions passées en parametre
    """
    image = Image.new(im.mode, dec)
    pix = im.load()
    image_pix = image.load()
    dx = dec[0]/im.size[0]
    dy = dec[1]/im.size[1]
    for x in range(dec[0]):
        for y in range(dec[1]):
            image_pix[x, y] = pix[x/dx, y/dy]
    return image


def decouper_image(im, coef):
    """
    Découpe l'image en une multitude de sous images.
    coef images en longueur et coef images en hauteur pour un total de coef² images
    Ces images sont retournée dans une liste.
    """
    sys.stdout.write("-------- découpage --------"+chr(13))
    pix = im.load()
    long = im.size[0]//coef
    larg = im.size[1]//coef
    im_decoupee = []
    for x in range(0, im.size[0], long):
        for y in range(0, im.size[1], larg):
            decoupage = Image.new(im.mode, (long, larg))
            decoup_pix = decoupage.load()
            for xp in range(long):
                for yp in range(larg):
                    if 0 <= x+xp < im.size[0] and 0 <= y+yp < im.size[1]:
                        decoup_pix[xp, yp] = pix[x+xp, y+yp]
            im_decoupee.append(decoupage)
    return im_decoupee


def reconstruire_image(im_decoupee, coef):
    """
    Reconstruis l'image a partir de la liste d'image passée en parametre
    """
    sys.stdout.write("------ reconstruction -----"+chr(13))
    s_long = im_decoupee[0].size[0]
    s_larg = im_decoupee[0].size[1]
    long = s_long*coef
    larg = s_larg*coef
    im = Image.new(im_decoupee[0].mode, (long, larg))
    pix = im.load()
    i = 0
    for x in range(0, long, s_long):
        for y in range(0, larg, s_larg):
            decoup_pix = im_decoupee[i].load()
            for xp in range(s_long):
                for yp in range(s_larg):
                    if 0 <= x+xp < im.size[0] and 0 <= y+yp < im.size[1]:
                        pix[x+xp, y+yp] = decoup_pix[xp, yp]
            i += 1
    return im

#------------------------------------------------------------------------------

def analyse_moy_rgb_separe(repertoire_file, im_decoup, precision):
    """
    Une analyse de l'image passée en parametre utilisant la moyenne de chacun de ses canneaux RGB

    Compare les informations receuillies avec celle stockées dans le fichier "repertoire file"
    pour retournée une image correspondant le plus possible
    """
    pix_decoup = im_decoup.load()
    reponse = im_decoup
    sum_r, sum_g, sum_b, c = 0, 0, 0, 0
    for x in range(im_decoup.size[0]):
        for y in range(im_decoup.size[1]):
            r, g, b = pix_decoup[x, y]
            sum_r += r
            sum_g += g
            sum_b += b
            c += 1
    moy_r, moy_g, moy_b = sum_r//c, sum_g//c, sum_b//c
    with open(repertoire_file, mode='r', encoding='utf8') as f:
        texte = f.read()
        lignes = texte.split('\n')
        stop = 0
        cinq_res = []
        while stop == 0:
            for ligne in lignes:
                data = ligne.split(';')
                if len(data) < 4: continue
                if int(data[0])-precision <= moy_r <= int(data[0])+precision and int(data[1])-precision <= moy_g <= int(data[1])+precision and int(data[2])-precision <= moy_b <= int(data[2])+precision:
                    cinq_res.append(data[3])
                    if len(cinq_res) == 6:
                        stop = 1
                    break
            if stop == 0:
                precision += 5
        f.close()
        reponse = Image.open(choice(cinq_res))
        reponse = resize(reponse, (im_decoup.size[0], im_decoup.size[1]))
    return reponse


def analyse_teinte(liste_teinte, im_decoup, precision):
    """
    Une analyse de l'image passée en parametre utilisant la moyenne de differentes plages de teinte prédéfinie

    Compare les informations receuillies avec celle stockées dans le fichier "repertoire file"
    pour retournée une image correspondant le plus possible
    """
    pix_decoup = im_decoup.convert("HSV").load()
    reponse = im_decoup.copy()
    filehue = open(liste_teinte, "r")
    f = filehue.read()
    listhue = f.split("\n")

    saturation = 0
    moy = 0
    value = 0

    nbr_rouge1, nbr_rouge2, nbr_orange, nbr_jaune, nbr_vert, nbr_vert_bleu, nbr_cyan, nbr_bleu, nbr_magenta, nbr_violet = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    moy_rouge1, moy_rouge2, moy_orange, moy_jaune, moy_vert, moy_vert_bleu, moy_cyan, moy_bleu, moy_magenta, moy_violet = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for x in range(im_decoup.size[0]):
        for y in range(im_decoup.size[1]):
            hue, sat, val = pix_decoup[x, y]

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

    list_nbr_moy = [[nbr_rouge, moy_rouge], [nbr_orange, moy_orange], [nbr_vert, moy_rouge1], [moy_vert, moy_rouge1], [nbr_vert_bleu, moy_vert_bleu], [nbr_cyan, moy_cyan], [nbr_bleu, moy_bleu], [nbr_magenta, moy_magenta], [nbr_violet, moy_violet]]
    list_nbr_moy.sort(key=itemgetter(0), reverse=True)
    saturation = saturation//moy
    value = value//moy

    stop = 0
    prec = 5
    baseprec = precision
    liste_cinq = []
    while stop == 0:
        for line in listhue:
            data = line.split(';')
            if len(data) < 4: continue
            if list_nbr_moy[0][1] - baseprec <= int(data[0]) <= list_nbr_moy[0][1] + baseprec:
                if saturation - prec <= int(data[1]) <= saturation + prec:
                    if value - prec <= int(data[2]) <= value + prec:
                        #im_rep = Image.open(repertoire+"/"+data[3])
                        liste_cinq.append(data[3])
                        if len(liste_cinq) == 5:
                        #im_rep = resize(im_rep, (im_decoup.size[0], im_decoup.size[1]))
                        #reponse = im_rep
                            stop = 1
                        break
        if stop == 0:
            baseprec += 5
        if baseprec > 50:
            baseprec = precision
            prec += 5

    filehue.close()
    im_rep = Image.open(choice(liste_cinq))
    im_rep = resize(im_rep, (im_decoup.size[0], im_decoup.size[1]))
    reponse = im_rep
    return reponse.convert("RGB")


def mosaique(repertoire_file, im_o, N_decoup, precision, hsv):
    """
    Fonction principale, redimentionne, découpe, traite l'image passée en parametre
    puis fini par la reconsctruire avant de la retourner
    """
    sys.stdout.write("---- redimentionnement ----"+chr(13))
    im_grand = resize(im_o, (int(im_o.size[0]*0.1)*N_decoup, int(im_o.size[1]*0.1)*N_decoup))
    liste_im = decouper_image(im_grand, N_decoup)
    for i, image in enumerate(liste_im):
        if (i+1)%(2*N_decoup) == 0:
            sys.stdout.write("-- traitement : "+str(i+1)+"/"+str(len(liste_im))+" --"+chr(13))
        if hsv:
            liste_im[i] = analyse_teinte(repertoire_file, image, precision)
        else:
            liste_im[i] = analyse_moy_rgb_separe(repertoire_file, image, precision)
    return reconstruire_image(liste_im, N_decoup)


#repertoire = "./Cat"
#repertoire_file = "traitement images.txt"
#im_o = Image.open("cygne.jpg")

#resultats = mosaique(repertoire_file, im_o, 50 , 20)
#resultats.show()

#resultats.save("cygne_m.jpg")
