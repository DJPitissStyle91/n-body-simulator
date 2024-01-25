#this class has no setters or getters as it is slower than a dictionary
class Body:

    def __init__(self, x_pos, y_pos, z_pos, v_x, v_y, v_z, mass, charge=0, is_conductive=False, radius=0):

        #Check if mass is not zero as it would result in infinite acceleration.
        if mass == 0:
            raise ZeroMassException

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.mass = mass
        self.charge = charge
        self.is_conductive = is_conductive
        self.radius = radius
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0

class ZeroMassException(Exception):
    pass
