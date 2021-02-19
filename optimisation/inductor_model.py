import numpy as np

class InductorModel():


    def __init__(self):
        '''
            Setup the object
        '''

        # define the constants
        self.beta        = 1.66e-3
        self.alpha_1     = -1.330
        self.alpha_2     = -0.125
        self.alpha_3     = 2.500
        self.alpha_4     = 1.830
        self.alpha_5     = -0.022
        self.sigma       = 2.784740e+07
        self.mu          = 4e-7*np.pi
        self.epsilon     = 4*8.85e-12
        self.epsilon_ox  = 4*8.85e-12
        self.omega       = 2e9
        self.t           = 1.26e-6
        self.G_sub       = 1.5e+4
        self.C_sub       = 6.6e-6
        self.t_ox        = 5.371e-6
        self.C_load      = 0.1e-12



    def update(self, values):

        for value in values:
            exec('self.' + str(value) + '=' + str(values[value]) )


    def calculate(self):

        self.delta   = np.sqrt( 2 / (self.omega * self.mu * self.sigma) )
        self.l       = 4*self.n*self.d_avg
        self.L_s     = (self.beta*(1e6*self.d_out)**self.alpha_1 * (1e6*self.w)**self.alpha_2 * (1e6*self.d_avg)**self.alpha_3  * self.n**self.alpha_4 * (1e6*self.s)**self.alpha_5)*1e-9
        self.R_s     = self.l / ( self.sigma * self.w * self.delta * (1 - np.exp(-self.t/self.delta)) )
        self.C_ox    = (self.epsilon_ox*self.l*self.w)/(2*self.t_ox)
        self.C_si    = (self.C_sub * self.l * self.w)/2
        self.R_si    = 2 / (self.G_sub * self.l * self.w)
        self.R_p     = (1 + (self.omega*self.R_si * (self.C_si + self.C_ox))**2) / (self.omega**2 * self.R_si * self.C_ox**2)
        self.R_sp    = (self.L_s*self.omega)**2 / self.R_s
        self.R_tank  = 1.0/(1.0/self.R_p + 1.0/self.R_sp)
        self.C_s     = (self.epsilon * self.n * self.w**2) / (self.t_ox)
        self.C_p     = (self.C_ox + self.omega**2 * self.R_si * (self.C_si + self.C_ox) * self.C_si * self.C_ox) / (1 + (self.omega*self.R_si * (self.C_si + self.C_ox))**2)
        self.C_tot   = self.C_s + self.C_p
        self.C_tank  = self.C_load + self.C_tot
        self.L_tank  = (1 + (self.R_s/(self.L_s*self.omega))**2)*self.L_s

        self.Q_tank  = self.R_tank/(self.omega * self.L_s)