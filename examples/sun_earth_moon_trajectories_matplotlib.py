#bodies are initilized and simulation is run here

import physics
import body
import math
import matplotlib.pyplot as plt

def main():

    #target runtime T of the simulation in seconds in simulation time (set 0 to run forever)
    T = 60*60*24*365
    #each timestep of the simulation in seconds in simulation time
    dt = 10
    #time elapsed in seconds in simulation time
    t = 0

    #initialize bodies here (Sun, Earth and Moon are given as examples)
    bodies = [
        body.Body(0, 0, 0, 0, 0, 0, 1.9885e30, 0, True, 6.957e8), #Sun
        body.Body(1.4718e11, 0, 0, 0, -30290, 0, 5.972e24, 0, True, 6.371e6), #Earth
        body.Body(1.475638e11, 0, 0, 0, -31378, 0, 7.348e22, 0, True, 1.7374e6) #Moon
    ]
    coords = [ [] for body in bodies ]

    #while the iterations, properties of the bodies may be accessed to make other calculations, see body.py for keys
    while t < T or T == 0:
        physics.iterate_all_bodies(bodies, dt)
        for body_idx in range(len(bodies)):
            coords[body_idx].append([bodies[body_idx].x_pos, bodies[body_idx].y_pos])
        t += dt

    #plot the trajectories
    for body_idx in range(len(bodies)):
        plt.plot(*zip(*coords[body_idx]))
    plt.show()

if __name__ == '__main__':
    main()
