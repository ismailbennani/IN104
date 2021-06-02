from simulator import Body
from simulator import World
from ..solvers.solver import ISolver

from constants import G
from vector import Vector, Vector2




def gravitational_force(self, pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
        
        
        
    """
    __init__(self, Fx=0, Fy=0)
    
    alpha = G*(mass1*mass2)/sqrnorm((pos2-pos1))
    
    Fx.set_x = alpha * self.get_x(pos1) - self.get_x(pos_2)
    Fy.set_y = alpha * self.get_y(pos1) - self.get_y(pos_2)
    
    return  Vector2(Fx, Fy)

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
        mass =[]
        
        for element in World :
            mass.append(element.mass)
        
        
        n = len(y0)
        state = []
        y0 = self.y0
        for i in range (0, n):
            state.append(y0[i+n])
            
            
        for j in range(0,n):
            for k in range (0,n):
                if j!=k:
                    a += (1/mass[j]) * gravitational_force(y0[j] , mass[j] , y0[k] , mass[k])
            state.append(a)
            a=0
            
        return state
    
        raise NotImplementedError

    def make_solver_state(self, t, t0, y0):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        
        y = ISolver().__init__(self.derivatives, t0, y0, max_step_size=0.01)
        y = y.ISolver.integrate(t)
        

        return y

        
        raise NotImplementedError












class DummyEngine(IEngine):
    pass
