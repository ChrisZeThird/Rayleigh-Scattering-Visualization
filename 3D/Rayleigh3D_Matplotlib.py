# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 10:20:54 2023

@author: ChrisZeThird
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
radius_planet = 0.6         # Radius of planet
radius_atmosphere = 1.2     # Radius of atmosphere
height_atmosphere = 0.5     # Height of atmosphere
num_particles = 5000        # Number of particles in atmosphere
radius_particles = 15       # Radius of the particles in atmosphere

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

# Set up light source
light_pos = np.array([3.0, 3.0, 3.0])

# Calculate scattering
colors = []
for i in range(num_particles_effective):
    pos = np.array([x_filtered[i], y_filtered[i], z_filtered[i]])
    direction = pos - light_pos
    direction = direction / np.linalg.norm(direction)
    angle = np.arccos(np.dot(direction, np.array([0, 0, 1])))
    color = np.exp(-0.5*(angle/0.2)**2)
    colors.append(color)

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
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.set_axis_off() # remove axis 

# Set plot limits
lim = radius_atmosphere + 0.5
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)

ax.plot_surface(x_planet, y_planet, z_planet, color='blue') # plot planet
ax.plot_surface(x_atmosphere, y_atmosphere, z_atmosphere, color='white', alpha=0.2) # plot atmosphere
ax.scatter(x_filtered, y_filtered, z_filtered, c=colors, s=radius_particles, alpha=0.3) # plot particles

plt.show()
