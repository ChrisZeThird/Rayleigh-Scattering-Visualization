# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 10:20:54 2023

@author: ChrisZeThird
"""
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D


# Constants
radius_planet = 0.6         # Radius of planet
radius_atmosphere = 1.2     # Radius of atmosphere
height_atmosphere = 0.5     # Height of atmosphere
num_particles = 4000        # Number of particles in atmosphere
radius_particles = 20       # Radius of the particles in atmosphere

""" Define particles """

# Generate random positions for particles in atmosphere
theta = np.random.uniform(0, 2*np.pi, num_particles)
phi = np.random.uniform(0, np.pi, num_particles)
r = radius_atmosphere * np.cbrt(np.random.uniform(0, 1, num_particles))
x = r * np.sin(phi) * np.cos(theta)
y = r * np.sin(phi) * np.sin(theta)
z = r * np.cos(phi)

# Removes particles if they are inside the radius of the planet
indices = np.sqrt(x**2 + y**2 + z**2) > radius_planet
x_filtered = x[indices]
y_filtered = y[indices]
z_filtered = z[indices]

num_particles_effective = len(x_filtered)

# Set up light source initial position
r_light = 3.0
theta0 = 0
phi0 = 0

x_light = r_light * np.sin(phi0) * np.cos(theta0)
y_light = r_light * np.sin(phi0) * np.sin(theta0)
z_light = r_light * np.cos(phi0)
light_pos = np.array([x_light, y_light, z_light])

# Calculate scattering
def calculate_scattering(num_particles,x_particles,y_particles,z_particles,light_pos):
    colors = []
    for i in range(num_particles_effective):
        pos = np.array([x_particles[i], y_particles[i], z_particles[i]])
        direction = pos - light_pos
        direction = direction / np.linalg.norm(direction)
        angle = np.arccos(np.dot(direction, np.array([0, 0, 1])))
        color = np.exp(-0.5*(angle/0.2)**2)
        colors.append(color)
    return colors

colors = calculate_scattering(num_particles_effective,x_filtered,y_filtered,z_filtered,light_pos)

""" Set planet and atmosphere positions """

# Set planet position
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x_planet = radius_planet * np.cos(u) * np.sin(v)
y_planet = radius_planet * np.sin(u) * np.sin(v)
z_planet = radius_planet * np.cos(v)

# Set atmosphere position
x_atmosphere = radius_atmosphere * np.cos(u) * np.sin(v)
y_atmosphere = radius_atmosphere * np.sin(u) * np.sin(v)
z_atmosphere = radius_atmosphere * np.cos(v) 

""" Create figure """

# Set figure
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.set_axis_off() # remove axis 

# Set plot limits
lim = radius_atmosphere + 0.1
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)

ax.plot_surface(x_planet, y_planet, z_planet, color='blue') # plot planet
ax.plot_surface(x_atmosphere, y_atmosphere, z_atmosphere, color='white', alpha=0.2) # plot atmosphere
particles_scatter = ax.scatter(x_filtered, y_filtered, z_filtered, c=colors, s=radius_particles, alpha=0.5) # plot particles

# Set sliders to change light source position

theta_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
theta_slider = Slider(theta_slider_ax, 'Theta', 0, 2 * np.pi, valinit=0)
phi_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03])
phi_slider = Slider(phi_slider_ax, 'Phi', 0, np.pi, valinit=0)
button_ax = plt.axes([0.8, 0.015, 0.1, 0.04])
button = Button(button_ax, 'Reset', color='lightgray', hovercolor='0.975')

def update(val):
    theta = theta_slider.val
    phi = phi_slider.val
    
    x_light = r_light * np.sin(phi) * np.cos(theta)
    y_light = r_light * np.sin(phi) * np.sin(theta)
    z_light = r_light * np.cos(phi)
    
    # ax.clear()
    global colors, particles_scatter
    light_pos  = np.array([x_light, y_light, z_light])
    colors = calculate_scattering(num_particles_effective,x_filtered,y_filtered,z_filtered,light_pos)
    
    # Redraw scatter plot
    particles_scatter.remove()
    particles_scatter = ax.scatter(x_filtered, y_filtered, z_filtered, c=colors, s=radius_particles, alpha=0.5) # plot particles
    
    # rgba_colors = np.zeros((len(colors), 4))
    # rgba_colors[:, :3] = np.array(colors)[:, np.newaxis]
    # # rgba_colors[:, 3] = 0.5  # set alpha to 0.5
    # particles_scatter.set_facecolor(rgba_colors)

    fig.canvas.draw_idle()

def reset(event):
    theta_slider.reset()
    phi_slider.reset()
    
theta_slider.on_changed(update)
phi_slider.on_changed(update)
button.on_clicked(reset)

plt.show()
