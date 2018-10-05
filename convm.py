import numpy as np

def convm(x,p):
    '''Generates a convolution matrix.

    USAGE	X = convm(x,p)

    	Given a vector x of lenght N, an N+p-1 by p convolution
    	matrix of the following form is generated

                  |  x(0)  0      0     ...      0    |
                  |  x(1) x(0)    0     ...      0    |
                  |  x(2) x(1)   x(0)   ...      0    |
             X =  |   .    .      .              .    |
                  |   .    .      .              .    |
                  |   .    .      .              .    |
                  |  x(N) x(N-1) x(N-2) ...  x(N-p+1) |
    	          |   0   x(N)   x(N-1) ...  x(N-p+2) |
                  |   .    .      .              .    |
                  |   .    .      .              .    |
    	          |   0    0      0     ...    x(N)   |

    ---------------------------------------------------------------
     copyright 1996, by M.H. Hayes.  For use with the book
     "Statistical Digital Signal Processing and Modeling"
     (John Wiley & Sons, 1996).
    ---------------------------------------------------------------
    '''


    N = np.max(x.shape) + 2*p - 2
    x = x.flatten()
    x = np.pad(x,(p-1,p-1),mode='constant')

    X = np.zeros((N-p+1,p),dtype=x.dtype)
    for ii in range(p):
        X[:,ii] = x[p-ii-1:N-ii]
    return(X)
