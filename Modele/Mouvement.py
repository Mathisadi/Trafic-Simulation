# @Autor : Mathis Adinolfi
# @Date of creation : 02/10/2024

# Bibliothèques utilisées
import copy
from .Repere import *
from .Code_route import changement_bloc
from .Intersections import chemin_intersection
from .Update_route import update_grille


# Objectif définir une fonction qui déplace les voitures et met à jour le trafic


def mouvement_pieton(route, trafic):
    """
    Fonction qui permet de gérer le mouvement des piétons sur la route.
    Les piétons sont générés sur les cases de départ piétons et se déplacent sur les cases de passage piétons.
    Les piétons sont supprimés de la route quand ils finissent de traverser.

    Parameters:
    route (2D list): La route sur laquelle on simule le mouvement des piétons.
    trafic (2D list): Le trafic actuel de la route.

    Returns:
    route (2D list): La route mise à jour.
    trafic (2D list): Le trafic mis à jour.
    """

    # Dans un premier temps : on bouge les piétons aux abords de la route
    # On teste tous les éléments
    for x in range(len(route)):
        for y in range(len(route[x])):
            if route[x][y] != 0:
                if route[x][y][0] == "Depart_pieton":
                    if route[x][y][4] and trafic[x][y][0] == 1:
                        # On se déplace sur le passage piéton adjacent
                        dir_pieton = route[x][y][1]
                        dx, dy = repere[dir_pieton]
                        nx, ny = x + dx, y + dy

                        # On met à jour le passage piéton
                        route[nx][ny][2][dir_pieton] = 4
                        route[nx][ny][3][dir_pieton] = True
                        
                        # On enlève le piéton du trottoir
                        trafic[x][y][0] = 0

    # Dans un second temps : on bouge les piétons sur les passages piétons
    # On teste tous les éléments
    for x in range(len(route)):
        for y in range(len(route[x])):
            if route[x][y] != 0:
                if route[x][y][0] == "Pieton":
                    for dir_pieton in route[x][y][1]:
                        if route[x][y][2][dir_pieton] == 0 and route[x][y][3][dir_pieton]:
                            # On se déplace sur le bloc adjacent
                            dx, dy = repere[dir_pieton]
                            nx, ny = x + dx, y + dy

                            # Si c'est un passage piéton on le met à jour
                            if route[nx][ny][0] == "Pieton":
                                route[nx][ny][2][dir_pieton] = 4
                                route[nx][ny][3][dir_pieton] = True
                                                                
                            # On enléve le piéton du passage
                            route[x][y][3][dir_pieton] = False

    return route, trafic


def mouvement_entre_blocs(route, direction, trafic, ref_trafic):
    """
    Fonction qui permet de gérer le mouvement des voitures entre les blocs.
    Les voitures sont déplacées si le bloc suivant est vide, sinon elles ne bougent pas.

    Parameters:
    route (2D list): La route sur laquelle on simule le mouvement des voitures.
    direction (2D list): Les directions préférées des utilisateurs pour chaque élément de la route.
    trafic (2D list): Le trafic actuel de la route.
    ref_trafic (2D list): Le trafic actuel de la route au tour précédent.

    Returns:
    route (2D list): La route mise à jour.
    direction (2D list): Les directions mises à jour.
    trafic (2D list): Le trafic mis à jour.
    """

    # Dans un premier temps on fait déplacer les voitures entre les blocs
    deplacement_entre_bloc = changement_bloc(route, direction, trafic)

    # On vient regarder si chaque déplacement entre les blocs est possible
    for k in range(len(deplacement_entre_bloc)):
        # On trouve les nouvelles positions
        x, y, x_dest, y_dest = deplacement_entre_bloc[k]

        # On crée une variable pour savoir si le dépalcement à eu lieu
        est_deplace = False
        
        # Cas le plus simple on arrive sur un bloc fin
        if route[x_dest][y_dest][0] == "Fin":
            trafic[x_dest][y_dest][0] += 1
            trafic[x][y][-1] -= 1
            est_deplace = True
        
        # Cas particulier depart -> un passage piéton
        elif route[x][y][0] == "Depart" and route[x_dest][y_dest][0] == "Pieton":
            # On vérifie si le passage piéton est libre
            d, e = route[x_dest][y_dest][3], route[x_dest][y_dest][1]
            libre = not any([e[i] for i in d])
            # Si conditions vérifiées
            if libre and trafic[x_dest][y_dest][0] == 0: 
                trafic[x_dest][y_dest][0] += 1
                trafic[x][y][-1] -= 1
                est_deplace = True
        
        # Cas particulier !depart -> un passage piéton
        elif route[x][y][0] != "Depart" and route[x_dest][y_dest][0] == "Pieton":
            # On vérifie si le passage piéton est libre
            d, e = route[x_dest][y_dest][3], route[x_dest][y_dest][1]
            libre = not any([e[i] for i in d])
            # Si conditions vérifiées
            if libre and trafic[x_dest][y_dest][0] == 0 and ref_trafic[x_dest][y_dest][0] == 0:
                trafic[x_dest][y_dest][0] += 1
                trafic[x][y][-1] -= 1
                est_deplace = True
        
        # Cas particulier l'arrivée n'est pas un passage piéton ni fin mais le départ est un départ
        elif route[x][y][0] == "Depart":
            if trafic[x_dest][y_dest][0] == 0:
                trafic[x_dest][y_dest][0] += 1
                trafic[x][y][-1] -= 1
                est_deplace = True
                
        # Cas général
        else:
            if trafic[x_dest][y_dest][0] == 0 and ref_trafic[x_dest][y_dest][0] == 0:
                trafic[x_dest][y_dest][0] += 1
                trafic[x][y][-1] -= 1
                est_deplace = True
        
        # Maintenant que l'on vient de faire bouger la voiture il faut s'assurer de reparamétrer la route correctement
        # Notament au niveau des intersections
        if est_deplace:
            if route[x][y][0] == "Intersection" and route[x_dest][y_dest][0] != "Intersection":
                direction[x][y] = []
            elif route[x][y][0] == "Intersection" and route[x_dest][y_dest][0] == "Intersection":
                direction[x_dest][y_dest] = direction[x][y][1::]
                direction[x][y] = []
            elif route[x][y][0] != "Intersection" and route[x_dest][y_dest][0] == "Intersection":
                direction[x_dest][y_dest] = chemin_intersection(route, direction, (x, y))

    return route, direction, trafic


def mouvement_route(route, trafic, ref_trafic):
    """
    Cette fonction permet de gérer le mouvement des voitures dans les routes.

    Args:
        route (2D list): La route actuelle.
        trafic (2D list): Le trafic actuel de la route.
        ref_trafic (2D list): Le trafic actuel de la route au tour précédent.

    Returns:
        route (2D list): La route mise à jour.
        trafic (2D list): Le trafic mis à jour.
    """

    # On trouve la taille de la grille
    n, m = len(route), len(route[0])

    # On test tous les bloc de la grille
    for x in range(n):
        for y in range(m):
            if route[x][y] != 0:
                if route[x][y][0] == "Route":
                    for k in range(2, len(trafic[x][y]) + 1):
                        if (
                            trafic[x][y][-k] == 1
                            and trafic[x][y][-k + 1] == 0
                            and ref_trafic[x][y][-k + 1] == 0
                        ):
                            trafic[x][y][-k + 1] += 1
                            trafic[x][y][-k] -= 1

    return route, trafic


def mouvement(route, direction, trafic, temps):
    """
    Met à jour la route, les directions et le trafic en fonction des conditions actuelles des routes, des directions,
    et du trafic pour un instant donné.

    Args:
        route (2D list): Liste des éléments de la route, représentant l'état de chaque cellule.
        direction (2D list): Liste des préférences de direction pour chaque élément de la route.
        trafic (2D list): Représentation du trafic sur la route, indiquant la présence de voitures et piétons.
        temps (int): Temps écoulé depuis le début de la simulation en secondes.

    Returns:
        tuple: Retourne la route mise à jour, les directions mises à jour, et le trafic mis à jour après le traitement des piétons, des voitures, et des feux rouges.
    """

    # Update des éléments
    route, direction, trafic = update_grille(route, direction, trafic, temps)

    # On garde en copie le trafic
    ref_trafic = copy.deepcopy(trafic)

    # Mouvement des piétons
    route, trafic = mouvement_pieton(route, trafic)

    # Mouvement entre les blocs
    route, direction, trafic = mouvement_entre_blocs(
        route, direction, trafic, ref_trafic
    )

    # Mouvement dans les blocs
    route, trafic = mouvement_route(route, trafic, ref_trafic)

    return route, direction, trafic
