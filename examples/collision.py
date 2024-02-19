#bodies are initilized and simulation is run here

import physics
import body
import math

def main():

    #target runtime T of the simulation in seconds in simulation time (set 0 to run forever)
    T = 20
    #each timestep of the simulation in seconds in simulation time
    dt = 0.0001
    #time elapsed in seconds in simulation time
    t = 0

    #initialize bodies here (Sun, Earth and Moon are given as examples)
    bodies = [
        body.Body(0, 0, 0, 1, 0, 0, 1, 0, True, 1), #body 1
        body.Body(1, 0.1, 0, 0, 0, 0, 1, 0, True, 1) #body 2
    ]

    #while the iterations, properties of the bodies may be accessed to make other calculations, see body.py for keys
    while t < T or T == 0:
        physics.iterate_all_bodies(bodies, dt)
        t += dt

if __name__ == '__main__':
    main()
