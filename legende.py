#
#   Application to Generate Revisited Chromatic Circles
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

from PIL import Image, ImageDraw, ImageFont, ImageColor


def to_rgb(hc):
    try:
        rgb = ImageColor.getrgb(hc.strip())
        return rgb
    except Exception:
        pass

    return (0, 0, 0)


def couleur_rectangle(draw, font, couleur, x0, y0, w, h):
    draw.rectangle(
        [x0, y0, x0 + w, y0 + h],
        fill=to_rgb(couleur["code"]),
        outline=(0, 0, 0),
    )

    nom = couleur["nom"]
    try:
        bbox = draw.textbbox((0, 0), nom, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except Exception:
        mask = font.getmask(nom)
        tw, th = mask.size

    text_x = x0 + (w - tw) / 2
    text_y = y0 + (h - th) / 2
    draw.text((text_x, text_y), nom, fill=(0, 0, 0), font=font)


def afficher_texte(draw, font, x0, y0, texte):
    draw.text((x0, y0), texte, fill=(0, 0, 0), font=font)


def tracer_ligne(draw, couleur, x1, y1, x2, y2, width=4):
    rgb = to_rgb(couleur["code"])
    draw.line([(x1, y1), (x2, y2)], fill=rgb, width=width)
    pass


def legende(couleursSecondairesAlternees, couleursTertiaires, filename: str):
    font_size = 16
    padding_inbox = 40
    rect_h = 60

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    couleuresPrimaires = [
        couleursSecondairesAlternees[0],
        couleursSecondairesAlternees[2],
        couleursSecondairesAlternees[4],
    ]

    couleuresSecondaires = [
        couleursSecondairesAlternees[1],
        couleursSecondairesAlternees[3],
        couleursSecondairesAlternees[5],
    ]

    couleuresTertiaires = [
        couleursTertiaires[0],
        couleursTertiaires[1],
        couleursTertiaires[2],
        couleursTertiaires[3],
        couleursTertiaires[4],
        couleursTertiaires[5],
    ]

    routesCouleurs = couleuresPrimaires + couleuresSecondaires + couleuresTertiaires

    try:
        # measure text
        dummy = Image.new("RGB", (1, 1))
        dd = ImageDraw.Draw(dummy)
        max_text_w = 0
        for name, _ in routesCouleurs:
            try:
                bbox = dd.textbbox((0, 0), name, font=font)
                w = bbox[2] - bbox[0]
            except Exception:
                w = font.getmask(name).size[0]
            if w > max_text_w:
                max_text_w = w

        rect_w = max_text_w + 2 * padding_inbox

        img = Image.new("RGBA", (1000, 600), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        ####################################################
        ##              COULEURS TERTIAIRES
        ####################################################
        x_couleurs_tertiaires = 750
        y_couleurs_tertiaires = 150

        x0 = x_couleurs_tertiaires - 60

        ########### OCRE ############
        x0ocre = x_couleurs_tertiaires
        y0ocre = y_couleurs_tertiaires
        ocre = couleuresTertiaires[0]
        couleur_rectangle(draw, font, ocre, x0ocre, y0ocre - 20, rect_w, rect_h)

        ########### VERMILLON ############
        x0vermillon = x_couleurs_tertiaires
        y0vermillon = y_couleurs_tertiaires + 70
        vermillon = couleuresTertiaires[5]
        couleur_rectangle(
            draw, font, vermillon, x0vermillon, y0vermillon - 20, rect_w, rect_h
        )

        ########### POURPRE ############
        x0pourpre = x_couleurs_tertiaires
        y0pourpre = y_couleurs_tertiaires + 2 * 70
        pourpre = couleuresTertiaires[4]
        couleur_rectangle(
            draw, font, pourpre, x0pourpre, y0pourpre - 20, rect_w, rect_h
        )

        ###########  INDIGO ############
        x0indigo = x_couleurs_tertiaires
        y0indigo = y_couleurs_tertiaires + 3 * 70
        indifgo = couleuresTertiaires[3]
        couleur_rectangle(draw, font, indifgo, x0indigo, y0indigo - 20, rect_w, rect_h)

        ########### TURQUOISE ############
        x0turquoise = x_couleurs_tertiaires
        y0turquoise = y_couleurs_tertiaires + 4 * 70
        turquoise = couleuresTertiaires[2]
        couleur_rectangle(
            draw, font, turquoise, x0turquoise, y0turquoise - 20, rect_w, rect_h
        )

        ########### TILLEUL ############
        x0tilleul = x_couleurs_tertiaires
        y0tilleul = y_couleurs_tertiaires + 5 * 70
        tilleul = couleuresTertiaires[1]
        couleur_rectangle(
            draw, font, tilleul, x0tilleul, y0tilleul - 20, rect_w, rect_h
        )

        ####################################################
        ##              COULEURS SECONDAIRES
        ####################################################
        x_couleurs_secondaires = 460

        x0 = x_couleurs_secondaires - 30
        y0 = 90

        ########### ORANGE ############
        x0orange = x_couleurs_secondaires
        y0orange = y0ocre + 5
        orange = couleuresSecondaires[2]
        couleur_rectangle(draw, font, orange, x0orange, y0orange, rect_w, rect_h)

        ########### VIOLET ############
        x0violet = x_couleurs_secondaires
        y0violet = y0pourpre + 5
        violet = couleuresSecondaires[1]
        couleur_rectangle(draw, font, violet, x0violet, y0violet, rect_w, rect_h)

        ########### VERT ############
        x0vert = x_couleurs_secondaires
        y0vert = y0turquoise + 5
        vert = couleuresSecondaires[0]
        couleur_rectangle(draw, font, vert, x0vert, y0vert, rect_w, rect_h)

        ####################################################
        ##              COULEURS PRIMAIRES
        ####################################################
        x_couleurs_primaires = 100

        x0jaune = x_couleurs_primaires
        y0jaune = y0violet
        jaune = couleuresPrimaires[0]
        couleur_rectangle(draw, font, jaune, x0jaune, y0jaune, rect_w, rect_h)

        x0rouge = x_couleurs_primaires + 100
        y0rouge = y0vermillon
        rouge = couleuresPrimaires[2]
        couleur_rectangle(draw, font, rouge, x0rouge, y0rouge, rect_w, rect_h)

        x0bleu = x_couleurs_primaires + 100
        y0bleu = y0indigo
        bleu = couleuresPrimaires[1]
        couleur_rectangle(draw, font, bleu, x0bleu, y0bleu, rect_w, rect_h)

        ####################################################
        ##       LIGNES : PRIMAIRES -> TERTIAIRES
        ####################################################
        #
        ## JAUNE OCRE
        x1 = x0jaune + rect_w / 2
        y1 = y0jaune
        x2 = x1
        y_ligne_jaune1 = y0ocre - 10
        tracer_ligne(draw, jaune, x1, y1, x2, y_ligne_jaune1)

        x1 = x0jaune + rect_w / 2
        y1 = y_ligne_jaune1
        x2 = x0ocre
        y2 = y1
        tracer_ligne(draw, jaune, x1, y1, x2, y2)

        ## ROUGE VERMILLON
        x1 = x0rouge + rect_w / 2
        y1 = y0rouge
        x2 = x1
        y_ligne_rouge = y0vermillon + 25
        tracer_ligne(draw, rouge, x1, y1, x2, y_ligne_rouge)

        x1 = x0rouge + rect_w / 2
        y1 = y0vermillon + 25
        x2 = x0vermillon
        y2 = y1
        tracer_ligne(draw, rouge, x1, y1, x2, y2)

        ## BLEU INDIGO
        x1 = x0bleu + rect_w / 2
        y1 = y0bleu
        x2 = x1
        y_ligne_bleu = y0indigo + 25
        tracer_ligne(draw, bleu, x1, y1, x2, y_ligne_bleu)

        x1 = x0bleu + rect_w / 2
        y1 = y0indigo + 25
        x2 = x0indigo
        y2 = y1
        tracer_ligne(draw, bleu, x1, y1, x2, y2)

        ## JAUNE TILLEUL
        x1 = x0jaune + rect_w / 2
        y1 = y0jaune + rect_h
        x2 = x1
        y2 = y0tilleul + 25
        tracer_ligne(draw, jaune, x1, y1, x2, y2)

        x1 = x0jaune + rect_w / 2
        y1 = y0tilleul + 25
        x2 = x0tilleul
        y_ligne_jaune2 = y1
        tracer_ligne(draw, jaune, x1, y1, x2, y_ligne_jaune2)

        ####################################################
        ##      LIGNES : SECONDAIRES -> TERTIAIRES
        ####################################################
        #
        # ORANGE => OCRE
        x1 = x0orange + rect_w
        y1 = y0orange + rect_h / 2
        x2 = x0ocre
        y2 = y1
        tracer_ligne(draw, orange, x1, y1, x2, y2)

        # ORANGE => VERMILLON
        x1 = x0vermillon - 60
        y1 = y0orange + rect_h / 2
        x2 = x1
        y2 = y1 + 40
        tracer_ligne(draw, orange, x1, y1, x2, y2)

        x1 = x2
        y1 = y2
        x2 = x0vermillon
        tracer_ligne(draw, orange, x1, y1, x2, y2)

        # ROUGE => POURPRE
        x1 = x0vermillon - 60
        y1 = y_ligne_rouge
        x2 = x1
        y2 = y1 + 40
        tracer_ligne(draw, rouge, x1, y1, x2, y2)

        x1 = x2
        y1 = y2
        x2 = x0pourpre
        tracer_ligne(draw, rouge, x1, y1, x2, y2)

        # VIOLET => POURPRE
        x1 = x0violet + rect_w
        y1 = y0violet + rect_h / 2
        x2 = x0pourpre
        y2 = y1
        tracer_ligne(draw, violet, x1, y1, x2, y2)

        # VIOLET => INDIGO
        x1 = x0indigo - 60
        y1 = y0violet + rect_h / 2
        x2 = x1
        y2 = y1 + 40
        tracer_ligne(draw, violet, x1, y1, x2, y2)

        x1 = x2
        y1 = y2
        x2 = x0indigo
        tracer_ligne(draw, violet, x1, y1, x2, y2)

        # BLEU => TURQUOISE
        x1 = x0turquoise - 60
        y1 = y_ligne_bleu
        x2 = x1
        y2 = y1 + 40
        tracer_ligne(draw, bleu, x1, y1, x2, y2)

        x1 = x2
        y1 = y2
        x2 = x0turquoise
        tracer_ligne(draw, bleu, x1, y1, x2, y2)

        # VERT => TURQUOISE
        x1 = x0vert + rect_w
        y1 = y0vert + rect_h / 2
        x2 = x0turquoise
        y2 = y1
        tracer_ligne(draw, vert, x1, y1, x2, y2)

        # VERT => TILLEUL
        x1 = x0tilleul - 60
        y1 = y0vert + rect_h / 2
        x2 = x1
        y2 = y1 + 40
        tracer_ligne(draw, vert, x1, y1, x2, y2)

        x1 = x2
        y1 = y2
        x2 = x0tilleul
        tracer_ligne(draw, vert, x1, y1, x2, y2)

        ####################################################
        ##       LIGNES : PRIMAIRES -> TERTIAIRES
        ####################################################

        # BLEU => VERT - VIOLET
        x1 = x0violet + rect_w / 2
        y1 = y0violet + rect_h
        x2 = x0vert + rect_w / 2
        y2 = y0vert
        tracer_ligne(draw, bleu, x1, y1, x2, y2)

        # ROUGE => ORANGE - VIOLET
        x1 = x0orange + rect_w / 2
        y1 = y0orange + rect_h
        x2 = x1
        y2 = y0violet
        tracer_ligne(draw, rouge, x1, y1, x2, y2)

        # JAUNE => VERT
        x1 = x0vert + rect_w / 2
        y1 = y0vert + rect_h
        x2 = x1
        y2 = y_ligne_jaune2
        tracer_ligne(draw, jaune, x1, y1, x2, y2)

        # ORANGE => HAUNE
        x1 = x0orange + rect_w / 2
        y1 = y0orange
        x2 = x1
        y2 = y_ligne_jaune1
        tracer_ligne(draw, jaune, x1, y1, x2, y2)

        ####################################################
        ## LES TROIS ZONZE DE COULEURS
        ####################################################
        # COULEURS PRIMAIRES
        x0 = x_couleurs_primaires - 20
        y0 = y0rouge - 15
        x1 = x0 + 260
        y1 = y0 + 260
        draw.rounded_rectangle(
            [x0, y0, x1, y1], radius=10, fill=None, outline=(0, 0, 0), width=2
        )
        # COULEURS SECONDAIRES
        x0 = x_couleurs_secondaires - 20
        y0 = y0orange - 35
        x1 = x0 + 150
        y1 = y0 + 420
        draw.rounded_rectangle(
            [x0, y0, x1, y1], radius=10, fill=None, outline=(0, 0, 0), width=2
        )

        # COULEURS TERTIAIRES
        x0 = x_couleurs_tertiaires - 20
        y0 = y0ocre - 35
        x1 = x0 + 150
        y1 = y0 + 450
        draw.rounded_rectangle(
            [x0, y0, x1, y1], radius=10, fill=None, outline=(0, 0, 0), width=2
        )

        ####################################################
        ## NOMMER CHAQUE ZONZE DE COULEURS
        ####################################################
        afficher_texte(
            draw,
            font_bold,
            x_couleurs_primaires - 10,
            70,
            "Trois couleurs Primaires",
        )
        afficher_texte(
            draw,
            font_bold,
            x_couleurs_secondaires - 70,
            70,
            "Trois couleurs Secondaires",
        )
        afficher_texte(
            draw,
            font_bold,
            x_couleurs_tertiaires - 60,
            70,
            "Six couleurs Tertiaires",
        )

        img.save(filename)
        print(filename)
    except Exception as e:
        print("ERROR saving image:", e)
