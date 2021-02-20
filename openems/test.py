import numpy as np
import yaml
from pyems.structure import PCB, Microstrip
from pyems.simulation import Simulation
from pyems.mesh import Mesh
from pyems.pcb import common_pcbs
from pyems.coordinate import Coordinate2, Axis, Box3, Coordinate3
from pyems.field_dump import FieldDump, DumpType
from pyems.utilities import print_table

from pyems.structure import IC
from pyems.structure import Inductor

freq     = np.arange(0e9, 100e9, 1e5)
# freq = np.linspace(1e6, 100e9, 101)
ref_freq = 6e9
unit     = 1e-6

ic_length = 400
ic_width  = 400

sim = Simulation(freq=freq, unit=unit, reference_frequency=ref_freq)

# import the YAML definition of the layers
# input_filename = r'../sky130_stackup.yaml'
input_filename = r'../sky130_stackup_simplest.yaml'
with open(input_filename) as file:
    layers = yaml.load(file, Loader=yaml.FullLoader)


# create the IC layer structure
ic = IC(
    sim         = sim,
    layers      = layers,
    length      = ic_length,
    width       = ic_width
)


# create the inductor
inductor = Inductor(
    ic          = ic,
    position    = Coordinate2(0, 0),
    width       = 18.3,
    spacing     = 1.6,
    turns       = 2,
    radius      = 75,
    # sides       = 8,
    sides       = 4,
    feedlength  = 10,
    layer       = 'met5',
    resolution  = 0.001
)

# create the mesh
Mesh(
    sim             = sim,
    metal_res       = 1 / 20,
    nonmetal_res    = 1 / 10,
    min_lines       = 5,
    expand_bounds   = ((0, 0), (0, 0), (1, 50)),
    # expand_bounds   = ((0, 0), (0, 0), (1, 50)),
    # expand_bounds   = ((2, 2), (2, 2), (1, 50)),
)


# FieldDump(
#     sim=sim,
#     box=Box3(
#         Coordinate3(-ic_length / 2, -ic_width / 2, 0),
#         Coordinate3( ic_length / 2,  ic_width / 2, 200),
#     ),
#     # dump_type=DumpType.current_density_time,
#     dump_type=DumpType.hfield_time,
# )

# sim.view_csx()

sim.run()
# sim.view_field()

# print_table(
#     data=[sim.freq / 1e9, np.abs(sim.ports[0].impedance()), sim.s_param(1, 1)],
#     col_names=["freq", "z0", "s11"],
#     prec=[2, 4, 4],
# )
