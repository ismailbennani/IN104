from ..utils.world import Body, World
from ..solvers.solver import ISolver
from math import floor
from .constants import G
from ..utils.vector import Vector, Vector2




def gravitational_force(body1, body2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
  
    pos1 = body1.position
    pos2 = body2.position
    m1 = body1.mass
    m2 = body2.mass
    v1 = body1.velocity
    v2 = body2.velocity
   
    distance = (pos2-pos1).norm()
    dist_min = body1.draw_radius + body2.draw_radius
    
    #vecteur unitaire directeur de la force, dirigé de pos1 vers pos2
    u = (pos2 - pos1)/distance 
    
    # densité de Dirac de l'accéleration lors de la colision, correspondant à 
    # la dérivée du saut de vitesse pendant le choc, d'après la formule des sauts.
    if  distance <= dist_min : #cas du choc
        F = (v2.dot(u) - (2*m1/(m1 + m2)) * v1.dot(u)) * u
   
    # composante "continue" de l'accélération, dérivée de la vitesse au sens 
    # classique, d'après la formule des sauts.
    else : # cas d'une interaction à distance
        F = (G*m2/(distance**2)) * u
        
    return F

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

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """

        raise NotImplementedError


class DummyEngine(IEngine):
    
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
        
        
        n = floor(len(y0)/4)
        y0_prime = Vector(4*n)
        
        """ Vecteur qui contiendra les coordonnées de l'accélération"""
        F = Vector2(0,0)
       
        for i in range(n) :
            y0_prime[2*i] = y0[2*(n+i)]
            y0_prime[2*i + 1] = y0[2*(n+i) + 1]
            
            body1 = self.world.get(i)
            
            for k in range(n) :
                if k != i :

                    body2 = self.world.get(k)

                    F += gravitational_force( body1, body2)
            
            y0_prime[2*(n+i)] = F.get_x()
            y0_prime[2*(n+i) +  1] = F.get_y()
            
            """ remise à 0 de l'accélération"""
            F.set_x(0)
            F.set_y(0)
            
        return y0_prime
    
    
    
    def make_solver_state(self):
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

            body = self.world._bodies[i]
            y0[2*i] = body.position.get_x()
            y0[2*i + 1] = body.position.get_y()
            
            y0[2*(n+i)] = body.velocity.get_x()
            y0[2*(n+i) + 1] = body.velocity.get_y()
        
            """ Proposition de Simon
            for k in range(n):
                if k!=i:
                    
                    if Vector.norm(Vector2(y0[2*i], y0[2*i+1])-Vector2(y0[2*k],y0[2*k+1]) :
                                   y0[2*(n+i)] =
                                   y0[2*(n+i)+1] =
            """
            
      
        return y0

    pass
