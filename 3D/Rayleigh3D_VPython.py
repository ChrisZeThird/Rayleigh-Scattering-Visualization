# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:34:41 2023

@author: ChrisZeThird
"""

""" Import libraries """

import vpython as vp
    
""" Create Canvas """

canvas = vp.canvas(width=1080, height=720)
scene = vp.scene


""" Define methods for objects properties """

def atm_opacity(wavelength):
    return atm_density * (550 / wavelength)**4

def light_color(wavelength):
    r, g, b = 0, 0, 0
    if wavelength >= 400 and wavelength < 440:
        r = -(wavelength - 440) / (440 - 400)
        b = 1.0
    elif wavelength >= 440 and wavelength < 490:
        g = (wavelength - 440) / (490 - 440)
        b = 1.0
    elif wavelength >= 490 and wavelength < 510:
        g = 1.0
        b = -(wavelength - 510) / (510 - 490)
    elif wavelength >= 510 and wavelength < 580:
        r = (wavelength - 510) / (580 - 510)
        g = 1.0
    elif wavelength >= 580 and wavelength < 645:
        r = 1.0
        g = -(wavelength - 645) / (645 - 580)
    elif wavelength >= 645 and wavelength <= 700:
        r = 1.0
    return vp.vector(r, g, b)


""" Create objects """

# Define the planet
planet_radius = 5
planet = vp.sphere(radius=planet_radius, texture=vp.textures.earth, shininess=0)

# Define the atmosphere
atm_thickness = 3.0  # You can modify this using a slide cursor
atm_density = 0.5  # You can modify this using a slide cursor
atm_radius = planet.radius+atm_thickness
atm = vp.sphere(radius=atm_radius, opacity=0.25)
atm.opacity_function = atm_opacity

# Define the light source
light_type = 'red'  # You can modify this using a drop-down menu
light_size = 2  # You can modify this using a slide cursor
light_intensity = 1.0  # You can modify this using a slide cursor
pos_drift = 50

light_xpos = atm_radius+pos_drift
light_ypos = atm_radius+pos_drift
light_zpos = atm_radius+pos_drift

light_pos = vp.vector(light_xpos, light_ypos, light_zpos)
wavelength = 400
light = vp.local_light(pos=light_pos, color= light_color(wavelength), radius=light_size)
light.color_function = light_color

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

# Create the slider to rotate the light source around
def set_rotation_angle(slider):
    # light.rotate(angle=slider.value, axis=vp.vector(0, 1, 0), origin=planet.pos)
    
    # Calculate the rotation angle
    angle = vp.radians(slider.value)
    
    # Calculate the new position of the object
    x = atm_radius+pos_drift * vp.cos(angle)
    y = 0
    z = atm_radius+pos_drift * vp.sin(angle)
    
    # Set the position of the object
    light.pos = vp.vector(x, y, z)

# Create slider to change light source wavelength
def WL_cursor(slider):
    val = slider.value
    new_wavelength = light_color(val)
    global light
    light.color = new_wavelength
    
# Create the slider
slider_angle = vp.slider(wtitle='Rotate light source', min=0, max=360, step=1, value=0, bind=set_rotation_angle, right=15)
canvas.append_to_caption('Slide the cursor to move the light source.')
canvas.append_to_caption('\n\n')

slider_WL = vp.slider(wtitle='Change light source color', min=400, max=700, length=250, bind=WL_cursor, right=15)
canvas.append_to_caption('Slide the cursor to change the color of the light source.')
canvas.append_to_caption('\n\n')

# Define the white light button
def white():
    global light
    light.color = vp.color.white

white_button = vp.button(bind=white, text="White light", right=15)
canvas.append_to_caption('\n\n')

""" Run the simulation """

while True:
    vp.rate(30)
    
    # Update the atmosphere
    atm.radius = planet.radius+atm_thickness
    atm.opacity = 0.25*atm_density
    
    # Update the light source
    light.radius = light_size
    light.intensity = light_intensity
    light.pos = light.pos

    # Update the camera
    vp.scene.center = planet.pos
