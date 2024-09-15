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

def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def generate_random_dots():
     dots = []
     for i in range(DOT_NUMBER):
          center = (random.randint(-RECT_SIZE, RECT_SIZE) + SCREEN_WIDTH / 2, random.randint(-RECT_SIZE, RECT_SIZE) + SCREEN_HEIGHT / 2)
          dots.append(Dot(center))
     return dots

def get_convex_hull_points(dots):
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


                    