import numpy as np
from convm import convm

def prony(x,p,q):
    '''Model a signal using Prony's method.

    Usage: [a,b,err] = prony(x,p,q)

    	The sequence x is modeled as the unit sample response of
    	a filter having a system function of the form
    		H(z) = B(z)/A(z)
    	The polynomials B(z) and A(z) are formed from the vectors
    		b=[b(0), b(1), ... b(q)]
    		a=[1   , a(1), ... a(p)]
    	The input q defines the number of zeros in the model
    	and p defines the number of poles.  The modeling error
    	is returned in err.

    ---------------------------------------------------------------
     copyright 1996, by M.H. Hayes.  For use with the book
     "Statistical Digital Signal Processing and Modeling"
     (John Wiley & Sons, 1996).
    ---------------------------------------------------------------
    '''

    x = x.flatten()
    N = x.size
    assert (p + q) < N,'Model order too large'

    X = convm(x,p+1)
    Xq = X[q:N+p-1,:p]
    sol = np.linalg.lstsq(-Xq,X[q+1:N+p,0],rcond=None)[0]
    a = np.concatenate(([1],sol))
    b = X[:q+1,:p+1].dot(a)
    err = np.linalg.multi_dot((x[q+1:N].T,X[q+1:N,:p+1],a))
    return(a,b,err)

if __name__ == '__main__':

    # Example 4.4.1
    N = 10
    x = np.ones(N)
    p,q = 1,1
    a,b,err = prony(x,p,q)

    # Check to make sure we did alright
    assert a[0] == 1
    assert a[1] == -(N-2)/(N-1)
    assert b[0] == x[0]
    assert np.isclose(b[1],1/(N-1))
    assert np.isclose(err,(N-2)/(N-1))
