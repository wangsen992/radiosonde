import numpy as np
import pandas as pd
import scipy.optimize as optimize
from scipy.interpolate import interp1d

# define constants
R = 287.058
Cpd = 1005.7
Cpv = 1875
g = 9.81

varsIncluded = ['timestamp', 'Pressure', 'Temperature',
                'Humidity', 'WindDir', 'WindSpeed', 'Height',
                'WindNorth', 'WindEast']

iso_format = '%Y-%m-%d %H:%M:%S.%f'

def Lw(T):
    return (2.501 - 0.00237 * T) * 10**6

def gradx(f, x):
    '''
    Compute gradient of variable with non-uniform
    height with central differencing.

    Formula based on Lagrange Interpolation.
    ref: A First Course in Numerical Methods. Ascher & Greif
         pg. 419
    '''

    f_x0, f_xw, f_xe = f[1:-2], f[0:-3], f[2:-1]
    h0, h1 = x[1:-2] - x[0:-3], x[2:-1] - x[1:-2]
    f_grad = (h1 - h0)/(h1 * h0) * f_x0 \
             + 1 / (h0 + h1) * (h0/h1 * f_xe - h1/h0 * f_xw)
    return f_grad, x[1:-2]

def extract_var(sl, v, resolution=1.):
            
    out_dict = {}
    for s in sl:
        z = np.arange(np.ceil(s.index.min()),
                      np.floor(s.index.max()),
                      resolution)
        f = interp1d(s.index, s[v].values)
        out_dict[s.timestamp.iloc[0].strftime("%m-%d %H-%M")] = \
                pd.Series(f(z), index=z)
    return pd.DataFrame(out_dict)

def plot_vertical(sonde_df, ax=None, *args, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    for t in sonde_df.columns:
        ax.plot(sonde_df[t].values, sonde_df.index, label=t)
        ax.legend()
    return ax

