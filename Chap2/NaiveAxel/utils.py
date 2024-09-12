import pygame
import random

BLUE = (0, 0, 255)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (self.x,self.y), 5)
        
class Triangle:
    def __init__(self, a , b ,c):
         self.a = a,
         self.b = b,
         self.c = c

    def draw(self, surface):

        pygame.draw.polygon(surface, BLUE, [(self.a[0].x,self.a[0].y),(self.b[0].x,self.b[0].y), (self.c.x,self.c.y)], 5)

class Function : 
    def ExtremeEdges(points):
        listP = []
        for i in range(len(points)):
            for j in range(len(points)):
                if i == j:
                    continue
                    
                all_same_side = True
                is_positif = None
                    
                A = points[i]
                B = points[j]
                for index in range(len(points)):
                        
                    if index == i or index == j:
                        continue
                        
                    P = points[index]

                    AB = (B.x - A.x, B.y - A.y)
                    AP = (P.x - A.x, P.y - A.y)

                    Vx = AB[0]
                    Vy = AB[1]
                    Wx = AP[0]
                    Wy = AP[1]

                    current_result = Vx * Wy - Vy * Wx
                    current_is_positif = current_result > 0

                    if is_positif is None:
                        is_positif = current_is_positif
                    elif current_is_positif != is_positif:
                        all_same_side = False
                    
                if all_same_side: 
                    listP.append(A)
                    listP.append(B)
        return listP
        
    def compare_points(p):
        return (p.x, p.y)
    
    
    def remove_duplicates(points):
        seen = set()
        unique_points = []
        for point in points:
            if (point.x, point.y) not in seen:
                unique_points.append(point)
                seen.add((point.x, point.y))
        return unique_points
    
    
    def sortVertices(listP):
        finalList = Function.remove_duplicates(listP)
                        
        return sorted(finalList, key=Function.compare_points)
    
    
    def TriangulatePolygon (points):
        Triangulation = []
        total_points_number = len(points)
    
        
        
        for index in range(len(points)):
            indexA = (index+1) % total_points_number
            indexB = (index+2) % total_points_number
            
            P = points[1]
            A = points[indexA]
            B = points[indexB]
            
            print (P)
            print (A)
            

            
            Triangulation.append(Triangle(A,B,P))
            
     
            
            
        return Triangulation

