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

#!/usr/bin/env python3
import argparse

import tkinter as tk
from PIL import Image
import yaml
from pathlib import Path

import math
import io

from legende import legende

EPAISSEUR_DU_TRAIT = 6
# CARRE_COTES = 800


def dessiner_trait(canvas, w_c, y_c, r, O):
    # Convertir l'angle O en radians
    angle_rad = math.radians(O)

    # Calculer les coordonnées de l'extrémité du trait
    x_end = w_c + r * math.cos(angle_rad)
    y_end = y_c + r * math.sin(angle_rad)

    # Dessiner le trait
    canvas.create_line(w_c, y_c, x_end, y_end, fill="black", width=EPAISSEUR_DU_TRAIT)


def tracer_droite_cercles(canvas, x_c, y_c, O, R1, R2):
    # Convertir l'angle O en radians
    angle_rad = math.radians(O)

    # Calculer les coordonnées des points sur les cercles
    x1 = x_c + R1 * math.cos(angle_rad)  # Point sur le cercle de rayon R1
    y1 = y_c + R1 * math.sin(angle_rad)

    x2 = x_c + R2 * math.cos(angle_rad)  # Point sur le cercle de rayon R2
    y2 = y_c + R2 * math.sin(angle_rad)

    # Tracer la droite entre les deux points
    canvas.create_line(x1, y1, x2, y2, fill="black", width=EPAISSEUR_DU_TRAIT)


def arc_cercle(canvas, x_c, y_c, R, start_angle, end_angle):
    # Calculer l'angle d'extension
    extent = end_angle - start_angle

    # Calculer les coordonnées du rectangle englobant
    x0 = x_c - R
    y0 = y_c - R
    x1 = x_c + R
    y1 = y_c + R

    # Dessiner l'arc de cercle
    canvas.create_arc(
        x0,
        y0,
        x1,
        y1,
        start=start_angle,
        extent=extent,
        outline="black",
        width=EPAISSEUR_DU_TRAIT,
        style=tk.ARC,
    )


def cercle(canvas, x_c, y_c, R):
    x0 = x_c - R
    y0 = y_c - R
    x1 = x_c + R
    y1 = y_c + R
    canvas.create_oval(
        x0, y0, x1, y1, outline="black", fill="", width=EPAISSEUR_DU_TRAIT
    )


def courrone(canvas, x0, y0, r, phase, couleurs):
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
            fill=couleurs[i]["code"],
            outline="",
        )


def centre(canvas, x0, y0, Rp, phase, couleur):
    for i in range(3):
        start_angle = phase + i * 120
        # Tracer le secteur
        canvas.create_arc(
            x0 - Rp,
            y0 - Rp,
            x0 + Rp,
            y0 + Rp,
            start=start_angle,
            extent=120,
            fill=couleur[i]["code"],
            outline="",
        )


# Fonction pour dessiner un cercle avec des secteurs colorés
def crercle_chromatique_reorganise(
    canvas,
    couleursPrimaire,
    couleursSecondairesAlternees,
    couleursTertiaires,
    Rt,
    Rs,
    Rp,
):
    # Créer un canvas
    canvas.pack()

    x0 = Rt
    y0 = Rt

    courrone(canvas, x0, y0, Rt, 30, couleursTertiaires)
    courrone(canvas, x0, y0, Rs, 60, couleursSecondairesAlternees)
    centre(canvas, x0, y0, Rp, 30, couleursPrimaire)

    cercle(canvas, x0, y0, Rt)
    cercle(canvas, x0, y0, Rs)
    arc_cercle(canvas, x0, y0, Rp, 0, 60)
    arc_cercle(canvas, x0, y0, Rp, 120, 180)
    arc_cercle(canvas, x0, y0, Rp, 240, 300)
    for i in range(6):
        tracer_droite_cercles(canvas, x0, y0, 30 + 60 * i, Rt, Rs)

    for i in range(6):
        tracer_droite_cercles(canvas, x0, y0, 60 * i, Rs, Rp)

    for i in range(3):
        dessiner_trait(canvas, x0, y0, Rp, -30 + 120 * i)


def charge_les_couleurs(path: str, genre) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    couleurs = data["couleursOrdonees"]

    if genre:
        couleursPrimaire = [
            {"nom": "Jaune", "code": couleurs["Jaune"]},
            {"nom": "Bleu", "code": couleurs["Bleu"]},
            {"nom": "Rouge", "code": couleurs["Rouge"]},
        ]

        couleursSecondairesAlternees = [
            {"nom": "Jaune", "code": couleurs["Jaune"]},
            {"nom": "Vert", "code": couleurs["Vert"]},
            {"nom": "Bleu", "code": couleurs["Bleu"]},
            {"nom": "Violet", "code": couleurs["Violet"]},
            {"nom": "Rouge", "code": couleurs["Rouge"]},
            {"nom": "Orange", "code": couleurs["Orange"]},
        ]

        couleursTertiaires = [
            {"nom": "Ocre", "code": couleurs["Ocre"]},
            {"nom": "Tilleuil", "code": couleurs["Tilleuil"]},
            {"nom": "Turquoise", "code": couleurs["Turquoise"]},
            {"nom": "Indigo", "code": couleurs["Indigo"]},
            {"nom": "Pourpre", "code": couleurs["Pourpre"]},
            {"nom": "Vermillon", "code": couleurs["Vermillon"]},
        ]
    else:
        couleursPrimaire = [
            {"nom": "Jaune", "code": couleurs["Jaune"]},
            {"nom": "Rouge", "code": couleurs["Rouge"]},
            {"nom": "Bleu", "code": couleurs["Bleu"]},
        ]

        couleursSecondairesAlternees = [
            {"nom": "Jaune", "code": couleurs["Jaune"]},
            {"nom": "Orange", "code": couleurs["Orange"]},
            {"nom": "Rouge", "code": couleurs["Rouge"]},
            {"nom": "Violet", "code": couleurs["Violet"]},
            {"nom": "Bleu", "code": couleurs["Bleu"]},
            {"nom": "Vert", "code": couleurs["Vert"]},
        ]

        couleursTertiaires = [
            {"nom": "Tilleuil", "code": couleurs["Tilleuil"]},
            {"nom": "Ocre", "code": couleurs["Ocre"]},
            {"nom": "Vermillon", "code": couleurs["Vermillon"]},
            {"nom": "Pourpre", "code": couleurs["Pourpre"]},
            {"nom": "Indigo", "code": couleurs["Indigo"]},
            {"nom": "Turquoise", "code": couleurs["Turquoise"]},
        ]

    return couleursPrimaire, couleursSecondairesAlternees, couleursTertiaires


def save_canvas_as_png(canvas, filename):
    # Obtenir le postscript du canevas
    canvas.update()  # Assurez-vous que le canevas est à jour
    ps = canvas.postscript(colormode="color")

    # Convertir le postscript en image
    img = Image.open(io.BytesIO(ps.encode("utf-8")))
    img.save(filename, "png")


def parse_args():
    p = argparse.ArgumentParser(description="Paramètres des zones de couleurs")
    p.add_argument(
        "--Rt",
        type=float,
        default=400.0,
        help="rayon des couleurs tertiaires (par défaut 400)",
    )
    p.add_argument(
        "--Rs",
        type=float,
        default=None,
        help="rayon des couleurs secondaires alternées (optionnel)",
    )
    p.add_argument(
        "--Rp",
        type=float,
        default=None,
        help="rayon des couleurs primaires (optionnel)",
    )
    p.add_argument(
        "--orientation",
        choices=["droite", "gauche"],
        default="droite",
        help="orientation (droite|gauche), défaut droite",
    )
    return p.parse_args()



if __name__ == "__main__":
    args = parse_args()

    Rt = args.Rt
    Rs = args.Rs
    Rp = args.Rp
    Orientation = args.orientation

    if Rs is None or Rp is None:
        # avec ces valeurs de Rs et de Rp :
        # 1) la surface des couleurs tertiaires est trois fois celle des couleurs primaires
        # 2) la surface des couleurs secondaires alternées est deux fois celle des couleurs primaires
        Rs = Rt / (2) ** (1 / 2)
        Rp = Rt / (6) ** (1 / 2)

    couleursPrimaire, couleursSecondairesAlternees, couleursTertiaires = (
        charge_les_couleurs(
            "couleurs.yml", True if Orientation.lower() == "droite" else False
        )
    )

    # root = tk.Tk()
    # root.title("Cercle coloré")
    # canvas_cercle = tk.Canvas(root, width=2 * Rt, height=2 * Rt, bg="white")
    # crercle_chromatique_reorganise(
    #     canvas_cercle,
    #     couleursPrimaire,
    #     couleursSecondairesAlternees,
    #     couleursTertiaires,
    #     Rt,
    #     Rs,
    #     Rp,
    # )
    # save_canvas_as_png(canvas_cercle, "Yannick.Hiou.png")
    # root.mainloop()

    legende(couleursSecondairesAlternees, couleursTertiaires,"legende.png")
    
    pass
    
