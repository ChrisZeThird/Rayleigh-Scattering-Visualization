# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:34:41 2023

@author: ChrisZeThird
"""

""" Import libraries """

import vpython as vp

import numpy as np
import sys

""" Create Canvas """

canvas = vp.canvas(width=1080, height=720)
scene = vp.scene

""" Create objects """

# Define the planet
planet_radius = 5
planet_texture = 'planet.jpg'  # You can replace this with your own custom picture
planet = vp.sphere(radius=planet_radius, texture=vp.textures.earth, shininess=0)

# Define the atmosphere
atm_thickness = 3.0  # You can modify this using a slide cursor
atm_density = 0.5  # You can modify this using a slide cursor
atm_radius = planet.radius+atm_thickness
atm = vp.sphere(radius=atm_radius, opacity=0.25)

# Define the light source
light_type = 'sun'  # You can modify this using a drop-down menu
light_wavelength = 550  # You can modify this using a slide cursor
light_size = 0.1  # You can modify this using a slide cursor
light_intensity = 1.0  # You can modify this using a slide cursor
pos_drift = 50
light_pos = vp.vector(atm_radius+pos_drift, atm_radius+pos_drift, atm_radius+pos_drift)
if light_type == 'sun':
    light = vp.local_light(pos=light_pos, color=vp.color.white)
elif light_type == 'red_dwarf':
    light = vp.local_light(pos=light_pos, color=vp.color.red)
elif light_type == 'white_dwarf':
    light = vp.local_light(pos=light_pos, color=vp.color.white, radius=0.1)

# Define the camera
scene.autoscale = False
scene.range = 10
scene.forward = vp.vector(0, 0, -1)
scene.up = vp.vector(0, 1, 0)
scene.caption = 'Click and drag on the light source to move it. Use the drop-down menu and slide cursors to adjust its properties.'

""" Define the event handlers """

def on_light_down(evt):
    global light_dragging, light_drag_pos
    light_dragging = True
    light_drag_pos = evt.pos

def on_light_move(evt):
    global light_dragging, light_drag_pos
    if light_dragging:
        light.pos += evt.pos - light_drag_pos
        light_drag_pos = evt.pos

def on_light_up(evt):
    global light_dragging
    light_dragging = False

# Bind the event handlers
vp.scene.bind('mousedown', on_light_down)
vp.scene.bind('mousemove', on_light_move)
vp.scene.bind('mouseup', on_light_up)

def on_mouse_down(event):
    global dragging, last_mouse_pos
    obj = scene.mouse.pick
    if obj == light:
        dragging = True
        last_mouse_pos = scene.mouse.pos

canvas.bind('mousedown', on_mouse_down)

# Create a slider that controls the x position of the sphere
def set_x_position(slider):
    light.pos.x = slider.value
    
slider = vp.slider(min=-25, max=25, length=250, bind=set_x_position)

# Define the exit function
def exit_simulation():
    canvas.delete()
    # sys.exit()

# Create the exit button
exit_button = vp.button(bind=exit_simulation, text="Exit Simulation")
# exit_button.background = "#FF0000"  # Set button background color to red
# exit_button.foreground = "#FFFFFF"  # Set button text color to white
# exit_button.pos = scene.title_anchor + vp.vec(100, 0, 0)  # Position the button on the canvas


""" Run the simulation """

while True:
    vp.rate(30)
    
    # Update the atmosphere
    atm.radius = planet.radius+atm_thickness
    atm.opacity = 0.25*atm_density
    
    # Update the light source
    light.radius = light_size
    light.intensity = light_intensity
    if light_type == 'sun':
        light.color = vp.color.white
    elif light_type == 'red_dwarf':
        light.color = vp.color.red
    elif light_type == 'white_dwarf':
        light.color = vp.color.white
    
    # Update the camera
    vp.scene.center = planet.pos
    
    # Update the planet texture
    planet.texture = planet_texture