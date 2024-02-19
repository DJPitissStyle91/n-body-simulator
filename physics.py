#this file does not contain many functions, as it is slower and the sole purpose of this file is already calculating forces and collisions

import math
import body

GRAVITATIONAL_CONSTANT=6.6743e-11
COULOMB_CONSTANT=8.9875e9

#this function calculates the interactions between body1 and body2
def interact(body1, body2):

    #positions of bodies are assigned to respective variables
    x_1,y_1,z_1 = body1.x_pos, body1.y_pos, body1.z_pos
    x_2,y_2,z_2 = body2.x_pos, body2.y_pos, body2.z_pos

    #masses of bodies are assigned to respective variables as well as the sum of masses
    m1 = body1.mass
    m2 = body2.mass
    mass = m1 + m2

    #radii of bodies are assigned to respective variables
    r1 = body1.radius
    r2 = body2.radius

    #differences in x, y, and z positions are calculated
    Dx = x_1 - x_2
    Dy = y_1 - y_2
    Dz = z_1 - z_2

    #distance and distance squared between the bodies are calculated
    dist2 = Dx*Dx + Dy*Dy + Dz*Dz
    dist = math.sqrt(dist2)

    #components of the unit vector pointing from the first body to the second
    x = Dx/dist
    y = Dy/dist
    z = Dz/dist
        
    #charges of bodies are assigned to respective variables
    q1 = body1.charge
    q2 = body2.charge

    fixed1 = body1.is_fixed
    fixed2 = body2.is_fixed

    #if the distance between the bodies is less than the sum of their radii, then there is a collition
    if dist < r1 + r2:

        #components of the velocity vectors of the bodies are assigned to respective variables
        v1_x, v1_y, v1_z = body1.v_x, body1.v_y, body1.v_z
        v2_x, v2_y, v2_z = body2.v_x, body2.v_y, body2.v_z

        #velocities of the bodies along the unit vector are calculated
        v1_r = v1_x*x + v1_y*y + v1_z*z
        v2_r = v2_x*x + v2_y*y + v2_z*z

        #components of the velocities along the unit vector are calculated
        v1_rx, v1_ry, v1_rz = v1_r*x, v1_r*y, v1_r*z
        v2_rx, v2_ry, v2_rz = v2_r*x, v2_r*y, v2_r*z

        #velocity changes only along the unit vector, we can subtract the velocity along the unit vector to get the constant component of the velocity
        v1_tx, v1_ty, v1_tz = v1_x - v1_rx, v1_y - v1_ry, v1_z - v1_rz
        v2_tx, v2_ty, v2_tz = v2_x - v2_rx, v2_y - v2_ry, v2_z - v2_rz

        #velocity of the center of mass along the unit vector is calculated
        vd_r = (v1_r*m1 + v2_r*m2)/mass

        if body1.is_fixed:
            vd_r = v1_r

        if body2.is_fixed:
            vd_r = v2_r

        #final velocities along the unit vector are calculated
        v1f_r = -v1_r + 2*vd_r
        v2f_r = -v2_r + 2*vd_r

        #finally we add the final velocities along the unit vector to the constant components of the velocity
        if not body1.is_fixed:
            body1.v_x, body1.v_y, body1.v_z = v1_tx + v1f_r*x, v1_ty + v1f_r*y, v1_tz + v1f_r*z
        if not body2.is_fixed:
            body2.v_x, body2.v_y, body2.v_z = v2_tx + v2f_r*x, v2_ty + v2f_r*y, v2_tz + v2f_r*z

        #if the bodies are conductive, then the charges of the bodies are redistributed in proportion to their surface areas
        if body1.is_conductive and body2.is_conductive:

            q = q1 + q2

            r1s = r1*r1
            r2s = r2*r2

            sum_rs = r1s + r2s

            body1.charge = q * r1s / sum_rs
            body2.charge = q * r2s / sum_rs

    #if the bodies are not at the same point in space, then the force between them is calculated
    if dist2 > 0:

        #gravitational and electrical forces are calculated
        gravitational_force = -(GRAVITATIONAL_CONSTANT*m1*m2)/dist2
        electrical_force = (COULOMB_CONSTANT*q1*q2)/dist2

        #the net force is calculated
        force = gravitational_force + electrical_force

        #the components of the force are calculated
        f_x, f_y, f_z = force*x, force*y, force*z

        #the accelerations of the bodies are calculated and added to their cumulative accelerations from previous calculations
        if not body1.is_fixed:
            body1.a_x, body1.a_y, body1.a_z = body1.a_x + f_x/m1, body1.a_y + f_y/m1, body1.a_z + f_z/m1
        if not body2.is_fixed:
            body2.a_x, body2.a_y, body2.a_z = body2.a_x - f_x/m2, body2.a_y - f_y/m2, body2.a_z - f_z/m2

#this function moves bodies according to their velocities and changes their velocities according to their accelerations, finally their accelerations are reset to be calculated again
def apply(body, dt):

    body.x_pos, body.y_pos, body.z_pos = body.x_pos + body.v_x*dt, body.y_pos + body.v_y*dt, body.z_pos + body.v_z*dt
    body.v_x, body.v_y, body.v_z = body.v_x + body.a_x*dt, body.v_y + body.a_y*dt, body.v_z + body.a_z*dt
    body.a_x, body.a_y, body.a_z = 0, 0, 0

#this function takes a list of bodies, and calculates their interactions and applies them
def iterate_all_bodies(bodies, dt):

    #the interaction function is called for each body couple
    for body1_idx in range(len(bodies)-1):
        for body2 in bodies[body1_idx+1:]:
            interact(bodies[body1_idx], body2)

    #calculated interactions are applied to each body
    for body in bodies:
        apply(body, dt)
