# StarSystemSimulation

## Introduction

**This is a Work In Progress**

This project aims at simulating (semi) realistically a star systems in 3D, and try out some things like: 
removing a planet or a sun, making binary system and watch how they evolve, ...

![screenshot](./screenshot/screenshot.png)

## How it works:

We start by creating a star system, which could be realistic or not. The current implementation uses Sol as an example.

The simulation of Sol is made by querying Nasa JPL Horizons API through `astroquery` to get the position and velocity of
the various objects in the system.

We then compute the position of each object through n-body simulation.

## Interfaces

There are three interfaces possible, one using `matplotlib`, the other using `panda3d`, and the latest which only display text informations

### Configuration:

take a look at https://github.com/entropyqueen/StarSystemSimulation/blob/main/config.py 

### Panda3d

`python3 main.py panda3d`

https://user-images.githubusercontent.com/2721112/210183033-ddf1c996-5aae-417b-9097-2993e893436a.mp4

The keymap can be changed in config.py.
Here is the default keymap:

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
- increase camera movement speed: `=`
- decrease camera movement speed: `-`
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

Launch with
`python3 main.py matplotlib`

https://user-images.githubusercontent.com/2721112/210183047-ba376825-266e-4abc-a464-29387ae990bf.mp4


### Text

```
$ python3 ./main.py text
===============================================================
Body: #0
Sun: (mass: 333030.0 earthMass)
coords:	[ 1.30297237e-08  2.63768106e-09 -3.24993834e-10] AU
distance:	1.330e-08 AU
velocity:	1.330e-08 AU / d
accel:		1.330e-08 AU / d2
f:			5.300e+23 N
------------
Body: #1
Mercury: (mass: 0.055 earthMass)
coords:	[0.02847986 0.30423792 0.02224997] AU
distance:	3.064e-01 AU
velocity:	3.420e-02 AU / d
accel:		3.130e-03 AU / d2
f:			2.060e+22 N
------------
Body: #2
Venus: (mass: 0.815 earthMass)
coords:	[ 0.59716654 -0.41408386 -0.04014279] AU
distance:	7.278e-01 AU
velocity:	2.010e-02 AU / d
accel:		5.583e-04 AU / d2
f:			5.446e+22 N
------------
Body: #3
Earth: (mass: 1.0 earthMass)
coords:	[-2.21619282e-01  9.57839114e-01 -4.98688282e-05] AU
distance:	9.831e-01 AU
velocity:	1.749e-02 AU / d
accel:		3.061e-04 AU / d2
f:			3.664e+22 N
------------
Body: #4
Mars: (mass: 0.107 earthMass)
coords:	[0.02050098 1.56735053 0.03234596] AU
distance:	1.568e+00 AU
velocity:	1.354e-02 AU / d
accel:		1.206e-04 AU / d2
f:			1.544e+21 N
------------
Body: #5
Ceres: (mass: 0.00016 earthMass)
coords:	[-2.36748925  0.82847643  0.46229517] AU
distance:	2.551e+00 AU
velocity:	1.118e-02 AU / d
accel:		4.551e-05 AU / d2
f:			8.715e+17 N
------------
Body: #6
Jupiter: (mass: 317.8 earthMass)
coords:	[ 4.83311509  1.06843807 -0.11257051] AU
distance:	4.951e+00 AU
velocity:	7.919e-03 AU / d
accel:		1.207e-05 AU / d2
f:			4.592e+23 N
------------
Body: #7
Saturn: (mass: 95.16 earthMass)
coords:	[ 8.15581203 -5.49125699 -0.22909235] AU
distance:	9.835e+00 AU
velocity:	5.412e-03 AU / d
accel:		3.065e-06 AU / d2
f:			3.490e+22 N
------------
Body: #8
Uranus: (mass: 14.54 earthMass)
coords:	[13.36099443 14.43455643 -0.11957652] AU
distance:	1.967e+01 AU
velocity:	3.840e-03 AU / d
accel:		7.663e-07 AU / d2
f:			1.334e+21 N
------------
Body: #9
Neptune: (mass: 17.15 earthMass)
coords:	[29.76172288 -2.93335823 -0.62548531] AU
distance:	2.991e+01 AU
velocity:	3.165e-03 AU / d
accel:		3.314e-07 AU / d2
f:			6.803e+20 N
------------
Body: #10
Pluto: (mass: 0.00218 earthMass)
coords:	[ 16.18535004 -30.63884269  -1.40082392] AU
distance:	3.468e+01 AU
velocity:	3.098e-03 AU / d
accel:		2.465e-07 AU / d2
f:			6.431e+16 N
===============================================================
```

