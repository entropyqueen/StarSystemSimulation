# StarSystemSimulation

## Introduction

**This is a Work In Progress**

This project aims at simulating (semi) realistically a star systems, and try out some things like: 
removing a planet or a sun, making binary system and watch how they evolve, ...

![screenshot](./screenshot/screenshot.png)

## How it works:

We start by creating a star system, which could be realistic or not. The current implementation uses Sol as an example.

The simulation of Sol is made by querying Nasa JPL Horizons API through `astroquery` to get the position and velocity of
the various objects in the system.

We then compute the position of each object through n-body simulation.

## Interfaces

There are two interfaces possible, one using `matplotlib`, the other using `panda3d`

### Panda3d

![video](./videos/panda3d.mp4)

Keymap:

- move camera upward: `r`
- move camera downward: `f`
- move camera forward: `w`
- move camera left: `a`
- move camera backward: `s`
- move camera right: `d`
- rotate camera on Yaw axis: `mouse_x`
- rotate camera on pitch axis: `mouse_y`
- rotate camera right on roll axis: `e`
- rotate camera left on roll axis: `q`
- increase camera movement spee: ````
- decrease camera movement spee: ````
- Zoom in the simulation: `wheel_up`
- Zoom out of the simultaion: `wheel_down`
- select previous object, automatically rotate camera to look in object's direction: `arrow_left`
- select next object, automatically rotate camera to look in object's direction: `arrow_right`
- focus camera on selected object: `l`
- pause the simulation: `p`
- Switch between camera and select mode: `mouse2`
- delete selected object from simulation: `delete`
- quit the simulator: `escape`

### Matplotlib
WIP: I've broken too many things to make panda3d interface so I have to rewrite it

![video](./videos/matplotlib.mp4)