# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:03:32 2022

@author: ChrisZeThird

Source: https://mathworld.wolfram.com/Circle-LineIntersection.html

The point of this script is to define a variety of functions useful to find the intersection of a line with a circle, the length of a line, or simply computer
the equation of a line. Report to the comment above each function to understand its meaning, no docstring was written as most of the variables are explicit.
You'll also find function create the plot of the line and its potential intersection with a circle. This file is necessary to run the other file called "circle.py"
handling all of the figure settings such as sliders, buttons, and updating the line equations and intersections.
"""
import numpy as np
import matplotlib.pyplot as plt

## distance between two points
def d(x1,x2):
    return x2 - x1

## norme of a vector depending on the distance between each coordinates
def norme(d1,d2):
    return np.sqrt(d1**2 + d2**2)

def norme2(x1,x2,y1,y2):
    dx = d(x1,x2)
    dy = d(y1,y2)
    return norme(dx,dy)

## determinent
def D(x1,y1,x2,y2):
    return x1*y2 - x2*y1

## sign function
def sgn(x):
    if x<0:
        return -1
    else:
        return 1
    
## check if a point is on a line between two points
def in_between(x1,y1,x2,y2,x,y):
    """
    Input: 
        x1 -> float, x coordinate of the first point
        y1 -> float, y coordinate of the first point
        x2 -> float, x coordinate of the second point
        y2 -> float, y coordinate of the second point
        x -> float, x coordinate of the third point to check
        y -> float, y coordinate of the third point to check
        
    Output:
        Returns a tuple of the coefficients corresponding to the line equation (a,b): f(x)= ax + b
    
    Source: https://math.stackexchange.com/questions/701584/check-point-is-between-two-points
        """
        
    a,b = line(x1,y1,x2,y2)
    
    if a*x + b != y:
        return False
    else:
        # d0 = np.array([[d(x1,x2)],[d(y1,y2)]])
        
        # normd0 = np.linalg.norm(d0)     
        # v = d0/normd0
        # # print(v.shape)
        
        # d1 = np.array([[d(x,x1)],[d(y,y1)]])
        # # print(d1.shape)
        
        # dot_product = np.dot(np.transpose(v),d1)
        # # print(dot_product[0][0])
        # return (0 <=dot_product[0][0] and dot_product[0][0] <= normd0)   
        
        bool1 = (x1 <= x <= x2) and (y1 <= y <= y2)
        bool2 = (x1 <= x <= x2) and (y2 <= y <= y1)
        bool3 = (x2 <= x <= x1) and (y2 <= y <= y1)
        bool4 = (x2 <= x <= x1) and (y1 <= y <= y2)
        return (bool1 or bool2 or bool3 or bool4)
        
## intersection between lines and circle
def intersection(x1,y1,x2,y2,r):
    """
    Input: 
        x1 -> float, x coordinate of the first point
        y1 -> float, y coordinate of the first point
        x2 -> float, x coordinate of the second point
        y2 -> float, y coordinate of the second point
        r -> float, radius of the circle
    Output:
        A list of coordinates indicating the intersection point(s)
        between the line and the circle. If the result is None, there
        is no intersection point.
    """
    # det = D(x1,y1,x2,y2)
    # dx = d(x1,x2)
    # dy = d(y1,y2)
    # dr = norme(dx,dy)
    # delta = (r**2 * dr**2) - det**2
    # if delta>0:
    #     X1 = (det*dy + np.sign(dy)*dx*np.sqrt(delta))/(dr**2)
    #     Y1 = (-det*dx + abs(dy)*np.sqrt(delta))/(dr**2)
    #     X2 = (det*dy - np.sign(dy)*dx*np.sqrt(delta))/(dr**2)
    #     Y2 = (-det*dx - abs(dy)*np.sqrt(delta))/(dr**2)
    #     return [(X1,Y1),(X2,Y2)]
    # elif delta==0:
    #     X_Prime = det*dy/(dr**2)
    #     Y_Prime = -det*dx/(dr**2)
    #     return [(X_Prime,Y_Prime)]
    
    a,b = line(x1,y1,x2,y2) # getting the coefficients of the line between the points
    det = 4*(a**2)*(b**2) - 4*(a**2 + 1)*(b**2 - r**2)
    
    possible_intersections = []
    
    if det == 0:
        X_prime = -a*b/(a**2 + 1)
        Y_prime = a*(X_prime) + b
        possible_intersections =  [(X_prime,Y_prime)]
        # return [(X_prime,Y_prime)]
    
    elif det > 0:
        X1 = (-2*a*b + np.sqrt(det))/(2*(a**2 +1))
        Y1 = a*X1 + b
        X2 = (-2*a*b - np.sqrt(det))/(2*(a**2 +1))
        Y2 = a*X2 + b
        possible_intersections = [(X1,Y1),(X2,Y2)]
        # return [(X1,Y1),(X2,Y2)]
    
    if len(possible_intersections) > 0:
        for element in possible_intersections[::-1]:
            x,y = element
            if in_between(x1, y1, x2, y2, x, y)==False:
                possible_intersections.remove(element)

        return possible_intersections    
    
    else:
        return []


def dots_plot2(intersect,ax):
    if len(intersect) > 0:
        # print(len(intersect))
        u, = ax.plot(intersect[0][0],intersect[0][1],c='black',marker='o')
        n = len(intersect)
        if n == 1:
            return u
        elif n == 2:
            v, = ax.plot(intersect[1][0],intersect[1][1],c='black',marker='o')
            return u,v

# def dots_remove(dots):
#     if dots is not None:
#         for k in range(len(dots)):
#             l = dots[k]
            
#             dots[k] = l
#         return dots

## creating line between points
def line(x1,y1,x2,y2):
    """
    Input: 
        x1 -> float, x coordinate of the first point
        y1 -> float, y coordinate of the first point
        x2 -> float, x coordinate of the second point
        y2 -> float, y coordinate of the second point
    Output:
        Returns a tuple of the coefficients corresponding to the line equation (a,b): f(x)= ax + b
    """
    return np.polyfit([x1,x2],[y1,y2],1)


    
