import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from const import RECT_SIZE, DOT_NUMBER
from shapes import Dot, Triangle
import math

def is_left(A, B, P):
    AB = ((B[0] - A[0]), (B[1] - A[1]))
    AP = ((P[0] - A[0]), (P[1] - A[1]))

    Vx = AB[0]
    Vy = AB[1]
    Wx = AP[0]
    Wy = AP[1]

    current_result = Vx * Wy - Vy * Wx
    
    return current_result > 0



def generate_random_dots():
     dots = []
     for i in range(DOT_NUMBER):
          center = (random.randint(-RECT_SIZE, RECT_SIZE) + SCREEN_WIDTH / 2, random.randint(-RECT_SIZE, RECT_SIZE) + SCREEN_HEIGHT / 2)
          dots.append(Dot(center))
     return dots

def is_extrem_edge(dots, i, j):
    is_positive = None
    for (index, dot) in enumerate(dots):
        if i == index or j == index:
            continue
        current_is_positive = is_left(dots[i].center, dots[j].center, dot.center) > 0
        if is_positive is None:
            is_positive = current_is_positive
        elif is_positive != current_is_positive:
            return False
    return True

def sort_extrem_edges(edges):
    if not edges:
        return []

    sorted_edges = [edges.pop(0)]


    while edges:
        last_edge = sorted_edges[-1]

        for index, edge in enumerate(edges):
            if edge[0] == last_edge[1]:  
                sorted_edges.append(edge)
                edges.pop(index)
                break
            elif edge[1] == last_edge[1]:  
                sorted_edges.append((edge[1], edge[0])) 
                edges.pop(index)
                break

    return sorted_edges


def get_convex_hull_points(dots):


    extrem_edges = []
    
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            if is_extrem_edge(dots, i, j):
                extrem_edges.append((i, j))

    sorted_edges = sort_extrem_edges(extrem_edges[:])

    convex_hull_dots = [dots[sorted_edges[0][0]]]
    for edge in sorted_edges:
        convex_hull_dots.append(dots[edge[1]])

    return convex_hull_dots


def FindCircumcenter(A,B,C):
    mid_AB = ((A.center[0] + B.center[0]) / 2, (A.center[1] + B.center[1]) / 2)
    mid_AC = ((A.center[0] + C.center[0]) / 2, (A.center[1] + C.center[1]) / 2)
    
    AB = (B.center[0] - A.center[0], B.center[1] - A.center[1])
    AC = (C.center[0] - A.center[0], C.center[1] - A.center[1])

    perpendicular_AB =  ((-AB[1], AB[0]))
    perpendicular_AC = ((-AC[1], AC[0]))
    
    # b1 = mid_AB + t*perpendicular_AB
    # b2 = mid_AC + t*perpendicular_AC  
    
    # Résolution des équations
    A1 = perpendicular_AB[0]
    B1 = -perpendicular_AC[0]
    C1 = mid_AC[0] - mid_AB[0]
    
    A2 = perpendicular_AB[1]
    B2 = -perpendicular_AC[1]
    C2 = mid_AC[1] - mid_AB[1]
    
    det = A1 * B2 - A2 * B1
    if det == 0:
        raise ValueError("Les points sont colinéaires, pas de cercle circonscrit.")
    
    t1 = (C1 * B2 - C2 * B1) / det
    t2 = (A1 * C2 - A2 * C1) / det
    
    circumcenter = (mid_AB[0] + t1 * perpendicular_AB[0], mid_AB[1] + t1 * perpendicular_AB[1])
    
    return circumcenter  


def detectIllegalEdge(triangle1, radius, center, listTriangle):
    for triangle in listTriangle:
        if triangle.triangle_dots != triangle1.triangle_dots:

            common_points = list(set(triangle1.triangle_dots) & set(triangle.triangle_dots))
            if len(common_points) == 2:

                for dot in triangle.triangle_dots:
                    if dot not in triangle1.triangle_dots:
                        distanceCenter = math.sqrt((center[0] - dot.center[0]) ** 2 + (center[1] - dot.center[1]) ** 2)
                        if distanceCenter < radius:
                            print("oui")
                                  
                            unique_point1 = [dot for dot in triangle1.triangle_dots if dot not in common_points][0]
                            unique_point2 = [dot for dot in triangle.triangle_dots if dot not in common_points][0]
                            
                            unique_point1.selected =True
                            unique_point2.selected =True

                            new_triangle1 = Triangle([common_points[0], unique_point1, unique_point2])
                            
                            new_triangle1.selected =True
                            new_triangle2 = Triangle([common_points[1], unique_point1, unique_point2])
                            new_triangle2.selected = True
                            
                            
    
    
                            return triangle1,triangle, new_triangle1, new_triangle2
    return None,None,None,None


                    
def addVoronoiEdges(triangle1, listTriangle, voronoi_edges):
    centerT1 = FindCircumcenter(*triangle1.triangle_dots)
    count = 0
    for triangle in listTriangle:
        if triangle != triangle1:

            common_points = list(set(triangle1.triangle_dots) & set(triangle.triangle_dots))
            
            if len(common_points) == 2:
                centerT2 = FindCircumcenter(*triangle.triangle_dots)
                count += 1
                voronoi_edges.append((centerT1, centerT2))    
    # print(count)
    
    # edges = [
    #     (triangle1.triangle_dots[0], triangle1.triangle_dots[1]),
    #     (triangle1.triangle_dots[1], triangle1.triangle_dots[2]),
    #     (triangle1.triangle_dots[2], triangle1.triangle_dots[0])
    # ]
    
    # boundary_size=1000
        
    # if count == 2 :
        # for edge in edges:
        #     if not has_shared_edge(edge, listTriangle):  # Fonction pour détecter si l'arête est partagée
        #         # Calculer le vecteur normal à l'arête
        #         p1, p2 = edge
        #         edge_vector = [p2.center[0] - p1.center[0], p2.center[1] - p1.center[1]]
        #         normal_vector = [-edge_vector[1], edge_vector[0]]  # Perpendiculaire à l'arête
                
        #         # Normaliser le vecteur normal
        #         # length = math.sqrt(normal_vector[0] ** 2 + normal_vector[1] ** 2)
        #         # normal_vector = [normal_vector[0] / length, normal_vector[1] / length]

        #         # Tracer la ligne infinie en prolongeant dans la direction du vecteur normal
        #         point_far = [
        #             centerT1[0] + normal_vector[0] * boundary_size,
        #             centerT1[1] + normal_vector[1] * boundary_size
        #         ]
        #         voronoi_edges.append((centerT1, point_far))
                
                
def has_shared_edge(edge, listTriangle):
    # L'arête est définie par deux points (p1, p2)
    p1, p2 = edge

    # Parcourir tous les triangles pour vérifier si l'arête est partagée
    for triangle in listTriangle:
        # Récupérer toutes les arêtes du triangle
        edges = [
            (triangle.triangle_dots[0], triangle.triangle_dots[1]),
            (triangle.triangle_dots[1], triangle.triangle_dots[2]),
            (triangle.triangle_dots[2], triangle.triangle_dots[0])
        ]

        # Vérifier si l'arête (p1, p2) existe dans le triangle
        for e in edges:
            # Les arêtes sont non orientées, donc on doit vérifier (p1, p2) et (p2, p1)
            if (p1 == e[0] and p2 == e[1]) or (p1 == e[1] and p2 == e[0]):
                return True

    # Si aucune arête correspondante n'a été trouvée, alors elle n'est pas partagée
    return False


def lowest_dot(dots):
    lowest = dots[0]
    for dot in dots[1:]:
        if dot.center[1] > lowest.center[1] or (dot.center[1] == lowest.center[1] and dot.center[0] > lowest.center[0]):
            lowest = dot
    return lowest

def is_left(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def jarvis_march(dots):
    # Trouver le point le plus bas


    # Test si p3 est à gauche du segment (p1, p2)

    hull = []

    start = lowest_dot(dots)
    point_on_hull = start

    while True:
        hull.append(point_on_hull)
        # Sélectionner un point aléatoire pour commencer
        endpoint = dots[0] if dots[0] != point_on_hull else dots[1]

        for i in range(len(dots)):
            # Si le point i est à gauche de la ligne courante, mettre à jour l'endpoint
            if is_left(point_on_hull.center, endpoint.center, dots[i].center) > 0:
                endpoint = dots[i]

        point_on_hull = endpoint
        if point_on_hull == start:
            break

    return hull

def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def polar_angle_sort(points, start):
    def polar_angle(p):
        dx, dy = p.center[0] - start.center[0], p.center[1] - start.center[1]
        return math.atan2(dy, dx)  # atan2 donne l'angle polaire
    return sorted(points, key=polar_angle)


def graham_scan(dots):
    # Trouver le point le plus bas (ou le plus à gauche en cas d'égalité)


    # Initialisation
    start = lowest_dot(dots)
    sorted_dots = polar_angle_sort([dot for dot in dots if dot != start], start)
    hull = [start]

    for dot in sorted_dots:
        while len(hull) > 1 and cross_product(hull[-2].center, hull[-1].center, dot.center) <= 0:
            hull.pop()  # Retire les points avec des virages à droite
        hull.append(dot)

    return hull
