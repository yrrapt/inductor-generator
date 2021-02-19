import inductor_model
import numpy as np


values = {  'n'     :   2.4,
            'w'     :   49e-6,
            's'     :   1.6e-6,
            'd_out' :   200e-6,
            'd_avg' :   139e-6,
         }

inductor_model_obj = inductor_model.InductorModel()

inductor_model_obj.omega = 2*np.pi*10e9

inductor_model_obj.update(values)

inductor_model_obj.calculate()

print( "Inductance  = %f nH" % (inductor_model_obj.L_s * 1e9) )
print( "Q           = %f" % (inductor_model_obj.Q_tank) )
print( "R_tank      = %f" % (inductor_model_obj.R_tank) )