
class Radiosonde(pd.DataFrame):

    def __init__(self, df, meta, ddz_smooth_window=10):
        pd.DataFrame.__init__(self, index=df['Height'].values)
        self.index.name = 'z'
        setattr(self,'raw_df', df)
        setattr(self, 'meta', meta)
        # compact values for calculation
        # loading variables to numpy array to easier computation
        self['timestamp'] = df['timestamp'].values
        self['z'] = df['Height'].values
        self['U'] = df['WindSpeed'].values
        self['UDir'] = df['WindDir'].values
        self['v'] = df['WindNorth'].values
        self['u'] = df['WindEast'].values
        self['T_K'] = df['Temperature'].values 
        self['T'] = self['T_K'] - 273.15
        self['P'] = df['Pressure'].values
        self['RH'] = df['Humidity'].values
        self['es'] = 6.11 * 10 ** (7.5 * (self['T']) / (self['T'] + 237.3)) # sat vapor pres
        self['e'] = self['RH'] * self['es'] / 100 # vapor pres
        self['r'] = 0.622 * self['e'] / self['P'] # mixing ratio (1000 to convert to kgkg-1)
        self['q'] = self['r'] / (1 + self['r'])
        self['T_v_K'] = self['T_K'] * (1 + 0.61 * self['q'])
        self['T_v'] = self['T_v_K'] - 273.15

        # moist static energy (no contribution from water droplets)
        # Note: only 1.2% drop of g at 40km, so g taken as constant
        self['mse'] = Cpd * self['T_K'] + g * self['z'] \
                    + Lw(self['T']) * self['q']

        # potential temperature for moist air
        self['theta_v'] = self['T_K'] * (1000/self['P']) \
                          ** (0.2854 * (1-0.28e-3 * self['r'] * 1000))

        # dew point temperature
        self['T_D'] = (237.3 * np.log10(self['e']/6.11)) \
                      / (7.5 - np.log10(self['e']/6.11))
        self['T_DK'] = self['T_D'] + 273.15
        self._compute_theta_e()
        self._compute_ddz_vars(ddz_smooth_window=ddz_smooth_window)

    # equivalent potential temperature
    ## Computed with iterative calc on dew point and pressure
    def _compute_theta_e(self):
        '''
        Compute equivalent potential temperature with bolton (1980) method"
        '''
        T_DK = self['T_DK']
        T_K = self['T_K']
        r = self['r']
        T_LK = 1 / (1 / (T_DK - 56) + np.log(T_K/T_DK)/800) + 56
        P = self['P']

        theta_e = T_K * (1000/P) ** (0.2854 * (1 - 0.28e-3 * r)) \
                * np.exp( (3.376 / T_LK - 0.00254) * r * (1 + 0.81e-3 * r))
        self['T_LK'] = T_LK
        self['theta_e'] = theta_e

    def _compute_ddz_vars(self, ddz_smooth_window=10):
        '''
        Compute vertical buoyancy gradient, velocity gradient and gradient
        Richardson number
        '''
        self['dTheta_edz'] = self._ddz('theta_e', ddz_smooth_window)
        self['dTheta_vdz'] = self._ddz('theta_v', ddz_smooth_window)
        self['dUdz'] = self._ddz('U', ddz_smooth_window)
        self['dbdz'] = g / self['theta_e'] * self['dTheta_edz']
        self['Ri_g'] = (g / self['T_v_K'] * self['dTheta_vdz']) \
                    / self['dUdz'] ** 2

    def _ddz(self, varName, ddz_smooth_window=10):
        ser_tmp_sm = self[varName].rolling(ddz_smooth_window).mean()
        dudz, z_grad = gradx(ser_tmp_sm.values, ser_tmp_sm.index.values)
        return pd.Series(dudz, index=z_grad)

    def lcl(self):
        def _lcl_p(P, T_K, r):
            '''
            Inputs:
                * P_0    : Pressure, in hPa
                * T_K0  : Temperature in K
                * r_0    : mixing ratio in kg/kg
            '''
            # constants
            R = 287.058; Cp = 1004; # define constants
            # Compute fixed point
            e = r * P / 0.622
            T_dK = (237.3 * np.log10(e/6.11)) / (7.5 - np.log10(e/6.11)) + 273.15
            return P * (T_dK / T_K) ** (Cp/R)

        T_K = self['T_K'].values[0]
        P = self['P'].values[0]
        r = self['r'].values[0]
        P_lcl = optimize.fixed_point(_lcl_p, x0=P, args=[T_K,r])
        print("This method still needs improvement.")
        return P_lcl.mean()

    def zplot(self, x_vars, ax=None, **kwargs):

        if ax == None:
            fig, ax = plt.subplots(**kwargs)

        for varname in x_vars:
            ax.plot(self[varname].values,
                    self['z'].values,
                    label=varname)

        ax.legend()
        return ax

    def __repr__(self):
        
        return self.meta.__repr__()+'\n\n'

