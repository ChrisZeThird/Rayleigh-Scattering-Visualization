# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:54:01 2022

@author: ChrisZeThird

I concive that this script is a bit of a mess. Most of the important steps are commented, but not systematically. The script starts by defining the equation
of a circle and then settings different radius and 2 dots positions, which later will be used as the observation and light source points.
A big part of the code will be repetitive so once you figured what part means, understanding the rest will be a piece of cake.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

import intersection as inter # correspond to the file interesection.py 

theta = np.linspace(start=0,stop=2*np.pi,num=100) # array of angles to make a full circle

""" Function """

def make_circle(r,theta):
    x = np.cos(theta)*r
    y = np.sin(theta)*r
    return x,y

""" Parameters """

r1 = 10
r2 = 7

## Light source 

r = 12
theta0 = np.pi/2
x0, y0 = make_circle(r,theta0)

## Observation point

r_o = 12
theta_o = np.pi
x_o, y_o = make_circle(r_o,theta_o)

## Planet + Atmosphere

x1,y1 = make_circle(r1,theta) # atmosphere
x2,y2 = make_circle(r2,theta) # planet

""" Creating the lines between the original points """

## making the lines
a,b = inter.line(x0,y0,x_o,y_o)
N = 5
X0 = np.linspace(start=x0,stop=x_o,num=N,endpoint=True) # creating a linspace avoid an infinite line of equation ax+b, and doesn't require any additional arguments to truncate it
line = a*X0 + b

## finding the intersection
inter1 = inter.intersection(x0,y0,x_o,y_o,r1) # crossing atmosphere
inter2 = inter.intersection(x0,y0,x_o,y_o,r2) # crossing earth

""" Ploting the values """

## Figure settings

val_max = max(r1,r2,r) + 5

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-val_max, val_max])
ax.set_ylim([-val_max, val_max])

plt.subplots_adjust(bottom=.35)

ax.set_aspect('equal')

## Ploting the figures

ax.plot(x1,y1,c='skyblue') # atmosphere
ax.plot(x2,y2,c='grey') # earth (center)

t, = ax.plot(X0,line,c='grey',marker='o') # line between source and observation point
p, = ax.plot(x0,y0,c='green', marker='o') # light source positioning
q, = ax.plot(x_o,y_o,'bo') # observation point positioning


dots1 = inter.dots_plot2(inter1,ax)
dots2 = inter.dots_plot2(inter2,ax)

## Creating sliders and button for the light source

ax_theta = plt.axes([0.2,0.1,0.5,0.03])
slider_theta = Slider(ax=ax_theta, label='Angle [rad]', valmin=0, valmax=2*np.pi, valinit=theta0, color='green')

ax_radius = plt.axes([0.2,0.15,0.5,0.03])
slider_radius = Slider(ax=ax_radius, label='Radius', valmin=10, valmax=val_max, valinit=r, color='green')
    
reset_button_ax_theta  = fig.add_axes([0.75, 0.1, 0.2, 0.04])
reset_button_ax_radius = fig.add_axes([0.75, 0.15, 0.2, 0.04])
reset_button_theta     = Button(reset_button_ax_theta, 'Reset Src. Angle', color='yellowgreen', hovercolor='green')
reset_button_radius    = Button(reset_button_ax_radius, 'Reset Src. Radius',color='yellowgreen', hovercolor='green')

def reset_button_on_clicked_theta(mouse_event):
    slider_theta.reset()
    
def reset_button_on_clicked_radius(mouse_event):
    slider_radius.reset()
    
reset_button_theta.on_clicked(reset_button_on_clicked_theta)
reset_button_radius.on_clicked(reset_button_on_clicked_radius)

## Creating sliders and buttons for the observation point

ax_theta_o = plt.axes([0.2,0.2,0.5,0.03])
slider_theta_o = Slider(ax=ax_theta_o, label='Angle [rad]', valmin=0, valmax=2*np.pi, valinit=theta_o)

ax_radius_o = plt.axes([0.2,0.25,0.5,0.03])
slider_radius_o = Slider(ax=ax_radius_o, label='Radius', valmin=10, valmax=15, valinit=r_o)

reset_button_ax_theta_o  = fig.add_axes([0.75, 0.2, 0.2, 0.04])
reset_button_ax_radius_o = fig.add_axes([0.75, 0.25, 0.2, 0.04])
reset_button_theta_o     = Button(reset_button_ax_theta_o, 'Reset Obs. Angle', color='lightsteelblue', hovercolor='blue')
reset_button_radius_o    = Button(reset_button_ax_radius_o, 'Reset Obs. Radius', color='lightsteelblue', hovercolor='blue')

def reset_button_on_clicked_theta_o(mouse_event):
    slider_theta_o.reset()
    
def reset_button_on_clicked_radius_o(mouse_event):
    slider_radius_o.reset()
    
reset_button_theta_o.on_clicked(reset_button_on_clicked_theta_o)
reset_button_radius_o.on_clicked(reset_button_on_clicked_radius_o)
    

## Update function common to all of the sliders

def update(val):
    current_theta = slider_theta.val
    current_radius = slider_radius.val
    
    current_theta_o = slider_theta_o.val
    current_radius_o = slider_radius_o.val
    
    x_prime,y_prime = make_circle(current_radius,current_theta) # new light source postion
    p.set_xdata(x_prime)
    p.set_ydata(y_prime)
    
    x_o_prime,y_o_prime = make_circle(current_radius_o,current_theta_o) # new light source postion
    q.set_xdata(x_o_prime)
    q.set_ydata(y_o_prime)
    
    A,B = inter.line(x_prime,y_prime,x_o_prime,y_o_prime) # new line equation between the new points of observation and of light source
    X = np.linspace(start=x_prime,stop=x_o_prime,num=N,endpoint=True)
    Line = A*X + B
    t.set_xdata(X)
    t.set_ydata(Line)
    
    global dots1
    global dots2

    
    inter1 = inter.intersection(x_prime,y_prime,x_o_prime,y_o_prime,r1)
    if dots1 is not None:
        for l in dots1:
            ax.lines.remove(l) # removes former lines corresponding to the intersecitons with the outter circle before computing the new one
    
    
    dots1 = inter.dots_plot2(inter1,ax)    
        
    inter2 = inter.intersection(x_prime,y_prime,x_o_prime,y_o_prime,r2)    
    if dots2 is not None:
        for l in dots2:
            ax.lines.remove(l) # removes former lines corresponding to the intersecitons with the central circle before computing the new one
    
    dots2 = inter.dots_plot2(inter2,ax)    
    if len(inter2)>0:
        for l in dots2:
            l.set_color('red')
            # t.set_color('red')
    else:
        t.set_color('grey')
        
    
    fig.canvas.draw_idle()

slider_theta.on_changed(update)
slider_radius.on_changed(update)

slider_theta_o.on_changed(update)
slider_radius_o.on_changed(update)

plt.show()
