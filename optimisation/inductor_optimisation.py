import numpy as np
import inductor_model

from gpkit import Variable, VectorVariable, Model
from gpkit.nomials import Monomial, Posynomial, PosynomialInequality

# define the inductor model fitting parameters
beta        = 1.66e-3
alpha_1     = -1.330
alpha_2     = -0.125
alpha_3     = 2.500
alpha_4     = 1.830
alpha_5     = -0.022
sigma       = 2.784740e+07
mu          = 4e-7*np.pi
epsilon     = 4*8.85e-12
epsilon_ox  = 4*8.85e-12
omega       = 2*np.pi*10e9
t           = 1.26e-6
G_sub       = 1.5e+4
C_sub       = 6.6e-6
t_ox        = 5.371e-6
C_load      = 0.1e-12
omega_max   = 8e9
alpha       = 0.8
Q_tank_min  = 1


# create the variables
s       = Variable("s")
w       = Variable("w")
n       = Variable("n")
d_in    = Variable("d_in")
d_out   = Variable("d_out")
d_avg   = Variable("d_avg")

# d_out = d_avg + 0.5*n*(s+w)

C_min   = Variable("C_min")
C_max   = Variable("C_max")
# d_avg   = 0.5 * (d_out + d_in)


# calculate the inductor properties
delta   = np.sqrt( 2 / (omega * mu * sigma) )
l       = 4*n*d_avg
L_s     = (beta*(1e6*d_out)**alpha_1 * (1e6*w)**alpha_2 * (1e6*d_avg)**alpha_3  * n**alpha_4 * (1e6*s)**alpha_5)*1e-9
R_s     = l / ( sigma * w * delta * (1 - np.exp(-t/delta)) )
C_ox    = (epsilon_ox*l*w)/(2*t_ox)
C_si    = (C_sub * l * w)/2
R_si    = 2 / (G_sub * l *w)
R_p     = (1 + (omega*R_si * (C_si + C_ox))**2) / (omega**2 * R_si * C_ox**2)
R_sp    = (L_s*omega)**2 / R_s
# R_tank  = 1.0/(1.0/R_p + 1.0/R_sp)
G_tank  = 1.0/R_p + 1.0/R_sp

C_s     = (epsilon * n * w**2) / (t_ox)
C_p     = (C_ox + omega**2 * R_si * (C_si + C_ox) * C_si * C_ox) / (1 + (omega*R_si * (C_si + C_ox))**2)
C_tot   = C_s + C_p
C_tank  = C_load + C_tot

# omega_max = (1.0 + 0.5*(1.0 - alpha)) * omega
# omega_min = (1.0 - 0.5*(1.0 - alpha)) * omega

# r = omega_max / omega_min

L_tank = (1 + (R_s/(L_s*omega))**2)*L_s

Q_tank_inv = (omega * L_s * G_tank)

# we want the parallel impedance to be as large as possible
objective = G_tank


# set the constraint set
constraints = [L_tank*C_tank <= 1/(omega**2),
               L_s == 1e-9,
               Q_tank_inv <= 1/4,
               d_out <= 150e-6,
               d_out >= 10e-6,
            #    d_avg <= d_out,
               d_avg + 0.5*w*n + 0.5*s*n <= d_out,
               s <= 50e-6,
               s >= 1.6e-6,
               w <= 50e-6,
               w >= 1.6e-6,
               n <= 2,
               # n >= 0.5,
               ]


# # set the constraint set
# constraints = [L_tank*(C_load + C_tot + C_min) <= 1/(omega_max**2),
#                (r-1)*(C_tot + C_load) / C_max + r*C_min / C_max <= 1,
#                C_min >= alpha * C_max,
#                Q_tank_inv <= 1/4,
#                d_out <= 100e-6,
#                d_out >= 10e-6,
#                s <= 50e-6,
#                s >= 1.6e-6,
#                w <= 50e-6,
#                w >= 1.6e-6,
#                n <= 10,
#                n >= 0.5,
#                ]

m = Model(objective, constraints)


# m.debug()

# solve the model
# sol = m.solve(verbosity=1000)
sol = m.solve()
print(sol.table())


# print(sol)
# print(sol['freevariables'])



inductor_model_obj = inductor_model.InductorModel()
inductor_model_obj.omega = omega
inductor_model_obj.update(sol['freevariables'])
inductor_model_obj.calculate()

print( "Inductance  = %f nH" % (inductor_model_obj.L_s * 1e9) )
print( "Q           = %f" % (inductor_model_obj.Q_tank) )
print( "R_tank      = %f" % (inductor_model_obj.R_tank) )