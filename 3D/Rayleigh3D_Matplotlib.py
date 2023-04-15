# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 10:20:54 2023

@author: ChrisZeThird
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

""" Constants """
radius_planet = 1.0         # Radius of planet
radius_atmosphere = 2       # Radius of atmosphere
height_atmosphere = 0.5     # Height of atmosphere

rho0 = 1.225                # Air density at sea level
num_particles = 5000        # Number of particles in atmosphere
num_layers = 5             # Number of layers
layer_heights = np.linspace(0, height_atmosphere, num_layers+1)[1:]

""" Generate random positions for particles in each layer """

# Function to calculate air density at a given altitude and random positions for particles in each layer
def generate_particles(num_particles, radius_planet, radius_atmosphere, height_atmosphere):
    """Generate random positions for particles with exponential density profile."""
    # Constants
    r_max = radius_atmosphere   # Maximum radius of atmosphere

    # Generate random positions for particles in a volume closer to the planet's surface
    r_min = radius_planet
    r = (r_max**3 - r_min**3) * np.random.uniform(0, 1, num_particles) + r_min**3
    r = np.cbrt(r)
    phi = np.random.uniform(0, 2*np.pi, num_particles)
    costheta = np.random.uniform(-1, 1, num_particles)
    theta = np.arccos(costheta)

    # Apply probability weighting based on distance from planet's center
    p = np.exp(-(r - radius_planet)/height_atmosphere)
    p /= np.max(p)

    # Select particles based on weighted probability
    selected = np.random.rand(num_particles) < p

    # Calculate positions of selected particles
    r_selected = r[selected]
    phi_selected = phi[selected]
    theta_selected = theta[selected]
    x = r_selected * np.sin(theta_selected) * np.cos(phi_selected)
    y = r_selected * np.sin(theta_selected) * np.sin(phi_selected)
    z = r_selected * np.cos(theta_selected)

    # Calculate scattering color for particles
    direction = np.array([0, 0, 1])
    angle = np.arccos(np.dot(direction, np.array([0, 0, 1])))
    color = np.exp(-0.5*(angle/0.2)**2)
    colors = np.full(np.sum(selected), color)
    
    return x, y, z, colors

x, y, z = [], [], []
colors = []
for i in range(num_layers):
    x_layer, y_layer, z_layer, color_layer = generate_particles(num_particles, radius_planet, radius_atmosphere, height_atmosphere)
    x.append(x_layer)
    y.append(y_layer)
    z.append(z_layer)
    colors.append(color_layer)
    
# Combine all particle positions and colors
x = np.concatenate(x)
y = np.concatenate(y)
z = np.concatenate(z)
colors = np.concatenate(colors)

# Plot planet and atmosphere
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.set_axis_off()

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x_planet = radius_planet * np.cos(u) * np.sin(v)
y_planet = radius_planet * np.sin(u) * np.sin(v)
z_planet = radius_planet * np.cos(v)
x_atmosphere = radius_atmosphere * np.cos(u) * np.sin(v)
y_atmosphere = radius_atmosphere * np.sin(u) * np.sin(v)
z_atmosphere = radius_atmosphere * np.cos(v) # + height_atmosphere

ax.plot_surface(x_planet, y_planet, z_planet, color='navy')
ax.plot_surface(x_atmosphere, y_atmosphere, z_atmosphere, color='white', alpha=0.1)

# Plot particles with colors
ax.scatter(x, y, z, c=colors, s=5, alpha=0.2)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
