# -*- coding: utf-8 -*-
# le \ permet de continuer la ligne précédentes à la ligne suivantes
# les il signifie le programme


# =============================================================================
# importations

import folium
import webbrowser
import re
# =============================================================================

"""

Quelques renseignements:

les trames NMEA sont très diversifiés, en effets il en existe plus d'une
trentaine qui sont toutes différentes le premier élément de chaque trame
fournit des informations sur le type d'équipement utilisé et le type de trame
l'heure d'envoie de la réponse, la latitude, la longitude, le type de
positionnement le nombre de satélites mobilisés pour le calcul, la précision
horizontale l'altitude puis différentes informations souvent vide dans les
requêtes GPS et enfin la somme de contrôle de parité, un simple XOR sur les
caractères entre $ et *

L'heure UTC (Universel Temps coordonné ou Universal Temps coordinated) est
l'heure de référence internationale. Cette heure est calculée au Bureau
International des Poids et Mesure (BIPM) grâce à plusieurs horloges réparties
dans des laboratoires nationaux.

"""


def verif_format_tram(string: str) -> bool:
    # on définie le format d'une trame GPS
    regex = "^[$][A-Z]*," + \
        "[0-9]*[.][0-9]*," + \
        "[0-9]*[.][0-9]*," + \
        "[NS]," + \
        "[0-9]*[.][0-9]*," + \
        "[EW]," + \
        "[0-9]," + \
        "[0-9]+," + \
        "[0-9]+[.][0-9]+," + \
        "[0-9]+[.][0-9]+," + \
        "M," + \
        "[0-9]+[.][0-9]+," + \
        "M," + \
        ".*," + \
        "[*][0-9A-F][0-9A-F]"

    # re.search(regex, string) est un Match_object si le regex est correct
    # sinon re.search(regex, string) est None
    return re.search(regex, string) is not None


class Object_gps:

    def __init__(self, trame: str = "") -> None:
        """constructeur"""

        # assertion
        assert isinstance(trame, str), \
            "argument trame must be a str, not {}".format(type(trame))
        if trame == "":
            trame = \
                "$GPGGA,085508.375,4804.399,N,00508.792,E,1,12,1.0,0.0" + \
                ",M,0.0,M,,*65"

        else:
            assert not verif_format_tram(trame), "tram non valide"

        # le programme sépare les différents élément
        list_elt = trame.split(",")

        # le programe affectes les élements dans des variables locales
        # spécialisées pour nous aider
        # l'heure internationale sous la forme hhmmss.sss
        heure_UTC = list_elt[1]

        # DM pour Degres Minutes latitude sous la forme DDMM.MMMM
        latitude_DM = "".join(list_elt[2:4])

        # longitude sous la forme DDDMM.MMMM
        longitude_DM = "".join(list_elt[4:6])

        self.type_de_trame = list_elt[0]

        self.heure = "{heure}: {minutes}: {secondes}".format(
            heure=heure_UTC[:2],
            minutes=heure_UTC[2:4],
            # le programe arrondit les secondes à l'unité
            secondes=round(float(heure_UTC[4:]))
        )

        self.latitude = "{degres}°{minutes}' {secondes}\" {hemisphere}".format(
            degres=int(latitude_DM[:2]),
            minutes=int(latitude_DM[2:4]),
            # il calcule les secondes à partir des dix-millièmes de
            # minutes puis le programe arrondi ce nombre à 3 chiffres après
            # la virgule
            secondes=round(float(latitude_DM[4:-1]) * 60, 3),
            hemisphere=latitude_DM[-1]
        )

        self.longitude = "{degres}°{minutes}' {secondes}\" {E_ou_W}".format(
            degres=int(longitude_DM[:3]),
            minutes=int(longitude_DM[3:5]),
            # même méthode que pour la latitude
            secondes=round(float(longitude_DM[5:-1]) * 60, 3),
            E_ou_W=longitude_DM[-1]
        )

        self.type_de_positionnement = list_elt[6]

        self.nombre_de_satelites = int(list_elt[7])

        self.précision_horizontal_ou_hdop = float(list_elt[8])

        self.altitude = "{alt} m".format(
            alt=float(list_elt[9])
        )

        self.list_lat_longDD = [
            int(latitude_DM[:2]) + float(latitude_DM[2:-1]) / 60,
            int(longitude_DM[:3]) + float(longitude_DM[3:-1]) / 60
        ]

    # getters, méthodes qui renvoie les différentes valeurs :
    def get_type_of_trame(self) -> str:
        """getter du type de trame"""
        return self.type_de_trame

    def get_type_of_pos(self) -> str:
        """getter du type de positionnement"""
        return self.type_de_positionnement

    def get_heure_hh_mm_ss(self) -> str:
        """getteur de l'heure UTC"""
        return self.heure

    def get_latitude_dms(self) -> str:
        '''getter de la latitude en degrés minutes secondes'''
        return self.latitude

    def get_longitude_dms(self) -> str:
        """getter de la longitude en degrés minutes secondes"""
        return self.longitude

    def get_nombre_de_satelites(self) -> int:
        """getter du nombre de satalites solicités par le calcul"""
        return self.nombre_de_satelites

    def get_list_lat_long_dd(self) -> list:
        """getter de la liste qui contient la latitude en degré décimal et \
        la longitude en degré décimal
        """
        return self.list_lat_longDD


def place_marker(target_map: folium.Map, point_choisi: Object_gps) -> None:
    """place un marqeur à l'emplacement de point choisi sur la carte choise"""

    # assertions
    assert isinstance(target_map, folium.Map), \
        "target_map must be a folium.map, not {}".format(type(target_map))
    assert isinstance(point_choisi, Object_gps), \
        "point_choisi must be a Object_gps, not {}".format(type(point_choisi))

    folium.Marker(
        # coordonné du point cible
        point_choisi.get_list_lat_long_dd(),
        popup="<b>notre lycée</b>",
        tooltip="Lycée Charles de Gaulle"
    ).add_to(
        # carte sur laquelle il l'affiche
        target_map
    )


def save(mape: folium.Map, path: str):
    """fct qui save et open une map"""

    assert isinstance(mape, folium.Map), "mape must a folium.Map, not {}" \
        .format(type(mape))
    assert isinstance(path, str), "path must be a str, not {}" \
        .format(type(path))

    mape.save(path)
    webbrowser.open(path)


def carte1(point_choisi: Object_gps):

    # il crée un première carte
    map_fig_1 = folium.Map(
        # centrée sur le point principal
        location=point_choisi.get_list_lat_long_dd(),
        # zoomer au l'échelle de la ville
        zoom_start=15
    )

    # il place le point indiquer par la trame NMEA
    place_marker(map_fig_1, point_choisi)

    # il enregistre la carte 1
    save(map_fig_1, "map1.html")


def carte2(point_choisi: Object_gps):

    # il crée une carte
    map_fig_2 = folium.Map(
        # centrée aussi sur le point
        location=point_choisi.get_list_lat_long_dd(),
        # et un peu plus dézoomer que la première à l'échelle peu supérieur au
        # département
        zoom_start=8
    )

    # il place le point
    place_marker(map_fig_2, point_choisi)

    # il crée un cercle de centre le point de rayon 100 000 m soit 100km
    # il rempli le disque de la couleur spécifier
    folium.Circle(
        location=point_choisi.get_list_lat_long_dd(),
        # rayon du cercle en mètre
        radius=100_000,
        # texte affiché s'il y a un clic sur la zone
        popup="zone autorisée",
        # couleur du cercle
        color="red",
        # si le disque du cercle est rempli
        fill=True,
        # la couleur du disque
        fill_color='red'
    ).add_to(map_fig_2)
    # il ajoute l'élément à la carte (add_to)

    # il sauvegarde la carte 2
    save(map_fig_2, "map2.html")


# programme principal
if __name__ == "__main__":

    # trame NMEA GPS du lycée :
    # "$GPGGA,085508.375,4804.399,N,00508.792,E,1,12,1.0,0.0,M,0.0,M,,*65"

    trame = input("veuillez insérer votre trame NMEA : (sinon entrer) ")

    while not verif_format_tram(trame) and trame != "":
        trame = input(
            "trame non valide, veuillez vérifier votre trame puis resaisissez "
        )

    # point_cloisie est une instance de Object_gps qui décomposent les infos
    # de la trame donnée en argument
    point_choisi = Object_gps(trame)

    carte1(point_choisi)
    carte2(point_choisi)
