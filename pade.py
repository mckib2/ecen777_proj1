# function [a,b] = pade(x,p,q)
# %PADE	Model a signal using the Pade approximation method
# %----
# %Usage: [a,b] = pade(x,p,q)
# %
# %	The input sequence x is modeled as the unit sample response of
# %	a filter having a system function of the form
# %		H(z) = B(z)/A(z)
# %	The polynomials B(z) and A(z) are formed from the vectors
# %		b=[b(0), b(1), ... b(q)]
# %		a=[1   , a(1), ... a(p)]
# %	The input q defines the number of zeros in the model
# %	and p defines the number of poles.
# %
# %  see also ACM, COVM, PRONY, SHANKS
# %
# %---------------------------------------------------------------
# % copyright 1996, by M.H. Hayes.  For use with the book
# % "Statistical Digital Signal Processing and Modeling"
# % (John Wiley & Sons, 1996).
# %---------------------------------------------------------------
#
# x   = x(:);
# if p+q>=length(x), error('Model order too large'), end
# X   = convm(x,p+1);
# Xq  = X(q+2:q+p+1,2:p+1);
# a   = [1;-Xq\X(q+2:q+p+1,1)];
# b   = X(1:q+1,1:p+1)*a;

import numpy as np
from convm import convm

def pade(x,p,q):
    '''PADE	Model a signal using the Pade approximation method

    Usage: [a,b] = pade(x,p,q)

    	The input sequence x is modeled as the unit sample response of
    	a filter having a system function of the form
    		H(z) = B(z)/A(z)
    	The polynomials B(z) and A(z) are formed from the vectors
    		b=[b(0), b(1), ... b(q)]
    		a=[1   , a(1), ... a(p)]
    	The input q defines the number of zeros in the model
    	and p defines the number of poles.

      see also ACM, COVM, PRONY, SHANKS

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
    Xq = X[q+1:q+p+1,1:p+1]
    sol = np.linalg.lstsq(-Xq,X[q+1:q+p+1,0],rcond=None)[0]
    a = np.concatenate(([1],sol))
    b = X[:q+1,:p+1].dot(a)

    return(a,b)
