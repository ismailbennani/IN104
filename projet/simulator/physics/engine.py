from ..utils.world import Body, World
from ..solvers.solver import ISolver
from math import floor
from .constants import G
from ..utils.vector import Vector, Vector2




def gravitational_force( mass2, pos1, pos2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    
    F = (G*(mass2)/(((pos1-pos2).norm)**3))*(pos2 - pos1)
    
    return  F

    raise NotImplementedError
    

class IEngine(ISolver):
    def __init__(self, world):
        self.world = world
        

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        
    
        raise NotImplementedError

    def make_solver_state(self, t, t0, y0):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """

        raise NotImplementedError



class DummyEngine(IEngine):
    
    def derivatives(self, world, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        
        
        n = floor(len(y0)/4)
        y0_prime = Vector(4*n)
        
        """ Vecteur qui contiendra les coordonnées de l'accélération"""
        F = Vector2(0,0)
       
        for i in range(n) :
            y0_prime[2*i] = y0[2*(n+i)]
            y0_prime[2*i + 1] = y0[2*(n+i) + 1]
            
            pos1 = Vector2( y0[2*i], y0[2*i+1])
            
            for k in range(n) :
                if k != i :
                    body = world.get(i)
                    F += gravitational_force( body.mass, pos1, body.position)
            
            y0_prime[2*(n+i)] = F.get_x()
            y0_prime[2*(n+i) +  1] = F.get_y()
            
            """ remise à 0 de l'accélération"""
            F.set_x(0)
            F.set_y(0)
            
        return y0_prime
    
    
    
    def make_solver_state(self, world, t, t0):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        
        n = self.world.__len__()
        y0 = Vector(4*n)
        
        for i in range(n) :
            body = world._bodies[i]
            y0[2*i] = body.position.get_x
            y0[2*i + 1] = body.position.get_y
            y0[2*(n+i)] = body.velocity.get_x
            y0[2*(n+i) + 1] = body.velocity.get_y
        
        y = ISolver(self.derivatives( world, 0,  y0), t0, y0, max_step_size=0.01)
        y = y.integrate(t)
        
        return y
    
    pass
