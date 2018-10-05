import numpy as np
from prony import prony
from convm import convm
from scipy.signal import lfilter

def shanks(x,p,q):
    '''SHANKS	Model a signal using Shanks' method

    Usage: [a,b,err] = shanks(x,p,q)

    	The sequence x is modeled as the unit sample response of
    	a filter having a system function of the form
    		H(z) = B(z)/A(z)
    	The polynomials B(z) and A(z) are formed from the vectors
    		b=[b(0), b(1), ... b(q)]
    		a=[1   , a(1), ... a(p)]
    	The input q defines the number of zeros in the model
    	and p defines the number of poles.  The modeling error
    	is returned in err.

      see also ACM, COVM, PADE, PRONY

    ---------------------------------------------------------------
     copyright 1996, by M.H. Hayes.  For use with the book
     "Statistical Digital Signal Processing and Modeling"
     (John Wiley & Sons, 1996).
    ---------------------------------------------------------------
    '''

    x = x.flatten()
    N = x.size
    assert (p + q) < N,'Model order too large'

    a,_,_ = prony(x,p,q)
    u = np.zeros(N)
    u[0] = 1
    g = lfilter([1],a,u)
    G = convm(g,q+1)
    b = np.linalg.lstsq(G[:N,:],x,rcond=None)[0]
    err = x.T.dot(x) - np.linalg.multi_dot((x.T,G[:N,:q+1],b))

    return(a,b,err)
