import yaml
import datetime


# import the YAML definition of the layers
input_filename = r'../sky130_stackup.yaml'
with open(input_filename) as file:
    layers = yaml.load(file, Loader=yaml.FullLoader)


# some simulation settings
chip = [512, 512]
fft  = [256, 256]

colours = ['red', 'blue', 'green', 'yellow', 'orange', 'grey', 'white', 
            'cyan', 'purple', 'brown', 'navy', 'lightblue', 'wheat']


###########################################################
# create output header
tek_string  = "; Auto-Generated from " + input_filename + "\n"
tek_string += ";  at " + datetime.datetime.now().strftime("%Y%m/%d, %H:%M:%S") + "\n"*3


###########################################################
# create chip section

# create the analysis size and names
tek_string += "\
; ---------------------------------------------------------------------------------------\n\
; Define the chip specs\n\
; ---------------------------------------------------------------------------------------\n\
\n\
<chip>\n"
tek_string += "    chipx     = %d\n" % chip[0]
tek_string += "    chipy     = %d\n" % chip[1]
tek_string += "    fftx      = %d\n" % fft[0]
tek_string += "    ffty      = %d\n" % fft[1]
tek_string += "    TechFile  = sky130.tek"
tek_string += "    TechPath  = ."

# determine what layers eddy currents should be calculated on
eddy_threshold = 1000
for i, layer in enumerate(layers['medium']):
    if layers['medium'][layer]['rho'] < eddy_threshold:
        tek_string += "    eddy  = %d\n" % i


###########################################################
# create chip medium layers

# create the analysis size and names
tek_string += "\
; ---------------------------------------------------------------------------------------\n\
; Define the cross section layers\n\
; ---------------------------------------------------------------------------------------\n\n"

for i, layer in enumerate(layers['medium']):
    
    tek_string += "<layer> %d  ; %s\n" % (i, layers['medium'][layer]['name'])
    tek_string += "    rho = %f\n" % (layers['medium'][layer]['rho'])
    tek_string += "    t   = %f\n" % (layers['medium'][layer]['t'])
    tek_string += "    eps = %f\n\n" % (layers['medium'][layer]['eps'])


###########################################################
# create chip medium layers

# create the analysis size and names
tek_string += "\
; ---------------------------------------------------------------------------------------\n\
; Define the metal and via layers\n\
; ---------------------------------------------------------------------------------------\n\n"

for i, layer in enumerate(layers['conductors']):
    tek_string += "<metal> %d  ; %s\n" % (i, layers['conductors'][layer]['description'])
    tek_string += "    layer = %d\n" % (layers['conductors'][layer]['medium'])
    tek_string += "    rsh   = %f\n" % (layers['conductors'][layer]['rsh'])
    tek_string += "    t     = %f\n" % (layers['conductors'][layer]['t'])
    tek_string += "    d     = %f\n" % (layers['conductors'][layer]['d'])
    tek_string += "    name  = %s\n" % (layers['conductors'][layer]['name'])
    tek_string += "    color = %s\n\n" % (colours[i])

for i, layer in enumerate(layers['vias']):
    tek_string += "<via> %d  ; %s\n" % (i, layers['vias'][layer]['description'])
    tek_string += "    top       = %d\n" % (i+1)
    tek_string += "    bottom    = %d\n" % (i)
    tek_string += "    r         = %d\n" % (layers['vias'][layer]['r'])
    tek_string += "    width     = %f\n" % (layers['vias'][layer]['width'])
    tek_string += "    space     = %f\n" % (layers['vias'][layer]['space'])
    tek_string += "    overplot1 = %f\n" % (layers['vias'][layer]['overplot1'])
    tek_string += "    overplot2 = %f\n" % (layers['vias'][layer]['overplot2'])
    tek_string += "    name      = %s\n" % (layers['vias'][layer]['name'])
    tek_string += "    color     = %s\n\n" % (colours[len(layers['conductors'])+i])


###########################################################
# write to output file
output_filename = r'sky130.tek'
with open(output_filename, 'w') as file:
    file.write(tek_string)