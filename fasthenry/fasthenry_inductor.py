import numpy as np
from scipy.io import loadmat
import parse
import subprocess
import matplotlib.pyplot as plt

# set the inductor parameters
def create_inductor(radius, width, spacing, sides, turns, feedlength, substrate=False):

    with open('inductor.inp', 'w') as file:


        file.write('* auto-generated FastHenry inductor description\n')
        file.write('.default z=0 sigma=2.784740e07 nhinc=5 nwinc=7\n')

        if substrate:
            file.write('g1 x1 = -500e-6  y1 = -500e-6  z1 = -5.37e-6\n')
            file.write('+  x2 =  500e-6  y2 = -500e-6  z2 = -5.37e-6\n')
            file.write('+  x3 =  500e-6  y3 =  500e-6  z3 = -5.37e-6\n')
            file.write('+  thick = 1  sigma= 1.5e+4\n')
            file.write('+  seg1 = 100 seg2 = 100\n')

        # pre-calculate the inductor winding pitch
        pitch  = width + spacing
        points = []
        polys = []

        # form the square unit shape
        unit_shape4 = [ [ 1, -1],
                        [ 1,  1],
                        [-1,  1],
                        [-1, -1]]

        # form the octagon unit shape
        l_2 = 1/(1+np.sqrt(2))
        unit_shape8 = [ [ l_2, -1   ],
                        [ 1,   -l_2 ],
                        [ 1,    l_2 ],
                        [ l_2,  1   ],
                        [-l_2,  1   ],
                        [-1,    l_2 ],
                        [-1,   -l_2 ],
                        [-l_2, -1   ]]

        # select the shape
        if sides == 4:
            unit_shape = unit_shape4
        else:
            unit_shape = unit_shape8

        # ### starting point at feed
        points.append([pitch/2+width*(0.5*np.sqrt(2)-np.tan(np.pi/8)),  -radius])

        ### create the loop points
        for loop in range(turns):
            for corner in range(sides):

                if (corner == 6 and sides == 8):
                    points.append([
                                    unit_shape[corner][0]*(radius-loop*pitch),  
                                    unit_shape[corner][1]*(radius-(loop)*pitch)+pitch
                                ])
                    
                elif (corner == 3 and sides == 4) or \
                        (corner == 7 and sides == 8):
                    points.append([
                                    unit_shape[corner][0]*(radius-(loop)*pitch),  
                                    unit_shape[corner][1]*(radius-(loop+1)*pitch)
                                ])
                
                else:
                    points.append([
                                    unit_shape[corner][0]*(radius-loop*pitch),  
                                    unit_shape[corner][1]*(radius-loop*pitch)
                                ])

        ### finished now draw last point
        points.append([-pitch/2 - width*(0.5*np.sqrt(2)-np.tan(np.pi/8)),  -(radius-turns*pitch)])

        segments = []

        n = 0
        for point in points:
            n += 1
            file.write('N%d x=%fe-6 y=%fe-6\n' % (n, point[0], point[1]))

            if n == len(points):
                segments.append('E%d N%d N%d  w=2.0e-6 h=2.0e-6\n' % (n, n, n+1))
            else:
                segments.append('E%d N%d N%d  w=%fe-6 h=1.26e-6\n' % (n, n, n+1, width))


        # drop to layer below
        points = []
        points.append([-pitch/2 - width*(0.5*np.sqrt(2)-np.tan(np.pi/8)),  -(radius-turns*pitch)])
        points.append([-pitch/2,  -radius-2*feedlength])

        for i, point in enumerate(points):
            n += 1
            file.write('N%d x=%fe-6 y=%fe-6 z=-1.35e-6\n' % (n, point[0], point[1]))

        segments.append('E%d N%d N%d  w=%fe-6 h=1.26e-6\n' % (n-1, n-1, n, width))

        for segment in segments:
            file.write(segment)

        #* define one 'port' of the network
        #.external N01 N15
        file.write('.external N%d N%d\n' % (1, n))

        #* frequency range of interest.
        #.freq fmin=1e9 fmax=1e10 ndec=10
        # file.write('.freq fmin=1e9 fmax=100e9 ndec=10\n')
        file.write('.freq fmin=1e6 fmax=100e9 ndec=10\n')
        file.write('.end\n')


def simulate():

    subprocess.call(['fasthenry','inductor.inp'])



def plot(show=True):

    freq = []
    resistance = []
    inductance = []
    Q = []

    input_file = "Zc.mat"

    freq_line = parse.compile("Impedance matrix for frequency = {freq:g} {rows:d} x {cols:d}\n")
    with open(input_file, "r") as f:
        for line in f:
            data = freq_line.parse(line)
            if data != None:
                freq.append(data['freq'])
                g = []
                for x in range(0, data['rows']):
                    line = f.readline().replace('j', '').split()
                    s = np.asarray(line, dtype=float)
                    s = s[::2] + s[1::2] * 1j
                    g.append(s)
                Z = np.stack(g)
                impedance = Z.sum()
                resistance.append(np.real(impedance))
                inductance.append(np.imag(impedance) / (2 * np.pi * data['freq']))
                Q.append(np.imag(impedance) / np.real(impedance))

    plt.subplot(3,1,1)
    plt.semilogx(freq,resistance)
    plt.grid(True, which="both")
    plt.title('Resistance')

    plt.subplot(3,1,2)
    plt.semilogx(freq,[_*1e9 for _ in inductance])
    plt.grid(True, which="both")
    plt.title('Inductance')

    plt.subplot(3,1,3)
    plt.semilogx(freq,Q)
    plt.grid(True, which="both")
    plt.title('Quality Factor')
    plt.tight_layout()

    if show:
        plt.show()


if __name__ == "__main__":

    # set the inductor parameters
    radius      = 55
    width       = 15.0
    spacing     = 1.6
    sides       = 4
    turns       = 2
    feedlength  = 2
    substrate   = False

    create_inductor(
        radius      = radius,
        width       = width,
        spacing     = spacing,
        sides       = sides,
        turns       = turns,
        feedlength  = feedlength
    )
    simulate()
    # plot(show=False)

    # create_inductor(
    #     radius      = 70,
    #     width       = 10,
    #     spacing     = spacing,
    #     sides       = sides,
    #     turns       = 3,
    #     feedlength  = feedlength
    # )
    # simulate()
    plot(show=True)

    # sweep = list(np.linspace(40, 100, 8))
    # for i, radius in enumerate(sweep):

    #     create_inductor(
    #         radius      = radius,
    #         width       = width,
    #         spacing     = spacing,
    #         sides       = sides,
    #         turns       = turns,
    #         feedlength  = feedlength
    #     )
    #     simulate()
    #     plot(show=False)


    # create_inductor(
    #     radius      = radius,
    #     width       = width,
    #     spacing     = spacing,
    #     sides       = sides,
    #     turns       = turns,
    #     feedlength  = feedlength,
    #     substrate   = substrate
    # )
    # simulate()
    # plot(show=False)

    # substrate = True
    # create_inductor(
    #     radius      = radius,
    #     width       = width,
    #     spacing     = spacing,
    #     sides       = sides,
    #     turns       = turns,
    #     feedlength  = feedlength,
    #     substrate   = substrate
    # )
    # simulate()
    # plot(show=False)
    # plt.legend([4,8])



    # plt.legend(sweep)
    # plt.show()