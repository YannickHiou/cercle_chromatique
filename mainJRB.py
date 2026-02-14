# 
#   Tarot345Scores - Application de gestion des scores de Tarot
#   Copyright (C) 2026  Yannick Hiou <yannick.hiou@gmail.com>
#  
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  
import tkinter as tk
from PIL import Image, ImageDraw
import math
import io

EPAISSEUR_DU_TRAIT = 6
CARRE_COTES = 800

couleursPrimaire = [
    {"couleur":"#FFFF00", "nom":"Jaune"},
    {"couleur":"#FF0000", "nom":"Rouge"},
    {"couleur":"#0000FF", "nom":"Bleu"},
]
couleursSecondairesEtPrimaire =[
    {"couleur":"#FFFF00", "nom":"Jaune"},
    {"couleur":"#e5842d", "nom":"Orange"},
    {"couleur":"#FF0000", "nom":"Rouge"},
    {"couleur":"#551694", "nom":"Violet"},
    {"couleur":"#0000FF", "nom":"Bleu"},
    {"couleur":"#24ea4d", "nom":"Vert"},
]

couleursTertiaires =[
    {"couleur":"#9cbd41", "nom":"Tilleul"},
    {"couleur":"#f3bb3b", "nom":"Ocre"},
    {"couleur":"#db4d25", "nom":"Vermillon"},
    {"couleur":"#ba307d", "nom":"Pourpre"},
    {"couleur":"#2e0097", "nom":"Indifo"},
    {"couleur":"#46a0ad", "nom":"Turquoise"},
]

def dessiner_trait(canvas, w_c, y_c, r, O):
    # Convertir l'angle O en radians
    angle_rad = math.radians(O)

    # Calculer les coordonnées de l'extrémité du trait
    x_end = w_c + r * math.cos(angle_rad)
    y_end = y_c + r * math.sin(angle_rad)

    # Dessiner le trait
    canvas.create_line(w_c, y_c, x_end, y_end, fill='black', width=EPAISSEUR_DU_TRAIT)


def tracer_droite_cercles(canvas,x_c, y_c, O, R1, R2):
    # Convertir l'angle O en radians
    angle_rad = math.radians(O)

    # Calculer les coordonnées des points sur les cercles
    x1 = x_c + R1 * math.cos(angle_rad)  # Point sur le cercle de rayon R1
    y1 = y_c + R1 * math.sin(angle_rad)

    x2 = x_c + R2 * math.cos(angle_rad)  # Point sur le cercle de rayon R2
    y2 = y_c + R2 * math.sin(angle_rad)

    # Tracer la droite entre les deux points
    canvas.create_line(x1, y1, x2, y2, fill='black', width=EPAISSEUR_DU_TRAIT)

def arc_cercle(canvas, x_c, y_c, R, start_angle, end_angle):
    # Calculer l'angle d'extension
    extent = end_angle - start_angle

    # Calculer les coordonnées du rectangle englobant
    x0 = x_c - R
    y0 = y_c - R
    x1 = x_c + R
    y1 = y_c + R

    # Dessiner l'arc de cercle
    canvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent, outline='black', width=EPAISSEUR_DU_TRAIT, style=tk.ARC)


def cercle(canvas, x_c, y_c, R):
    x0 = x_c - R
    y0 = y_c - R
    x1 = x_c + R
    y1 = y_c + R
    canvas.create_oval(x0, y0, x1, y1, outline='black', fill='', width=EPAISSEUR_DU_TRAIT)  # Épaisseur de 4 pixels

def courrone (canvas, x0,y0, r, phase, couleurs ):
    for i in range(6):
        start_angle = phase + i * 60 
        # Tracer le secteur
        canvas.create_arc(
            x0 - r, 
            y0 - r, 
            x0 + r, 
            y0 + r, 
            start=start_angle, 
            extent=60, 
            fill=couleurs[i]["couleur"], 
            outline=''
        )
    
def centre(canvas, x0, y0, rC, phase, couleur):
    for i in range(3):
        start_angle = phase + i * 120
        # Tracer le secteur
        canvas.create_arc(
            x0 - rC, 
            y0 - rC, 
            x0 + rC, 
            y0 + rC, 
            start=start_angle, 
            extent=120, 
            fill=couleur[i]["couleur"], 
            outline=''
        )

# Fonction pour dessiner un cercle avec des secteurs colorés
def crercle_chromatique_reorganise(canvas, coteCarre):
    # Créer un canvas
    canvas.pack()


    # Centre et rayon du cercle
    x0, y0, rA = coteCarre / 2, coteCarre / 2, coteCarre / 2

    courrone(canvas, x0, y0, rA, 30, couleursTertiaires)

    rB = rA/(2)**(1/2)
    courrone(canvas, x0, y0, rB, 60, couleursSecondairesEtPrimaire)
    
    rC = rA /(6)**(1/2)
    centre(canvas, x0, y0, rC, 30, couleursPrimaire)
    
    cercle(canvas, x0,y0, rA)
    cercle(canvas, x0,y0, rB)
    arc_cercle(canvas, x0, y0, rC, 0, 60)
    arc_cercle(canvas, x0, y0, rC, 120, 180)
    arc_cercle(canvas, x0, y0, rC, 240, 300)
    for i in range(6):
        tracer_droite_cercles(canvas, x0, y0, 30 + 60*i, rA, rB)
    
    for i in range(6):
        tracer_droite_cercles(canvas, x0, y0, 60*i, rB, rC)

    for i in range(3):
        dessiner_trait(canvas, x0, y0,rC, -30 + 120*i)

def save_canvas_as_png(canvas, filename):
    # Obtenir le postscript du canevas
    canvas.update()  # Assurez-vous que le canevas est à jour
    ps = canvas.postscript(colormode='color')

    # Convertir le postscript en image
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save(filename, 'png')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cercle coloré")

    canvas = tk.Canvas(root, width=CARRE_COTES, height=CARRE_COTES, bg='white')

    crercle_chromatique_reorganise(canvas, CARRE_COTES)
     
    save_canvas_as_png(canvas, "cercleJRB.png")
    
    root.mainloop()



