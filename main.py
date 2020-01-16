import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from class_defs import Point
from class_defs import Input
from class_defs import Source

# reunaehdot, fixattu vs. absorpoiva
# lähteen sijainti, keskellä vai määriteltävissä
# input ja output


def main():
    plt.figure(dpi=1000)

    # read input file
    with open('input.txt') as input_file:
        for data in input_file:
            line = data.split()
            print(line)
            if line[0] == 't_steps':
                t_steps = int(line[2])
            elif line[0] == 'n_points':
                n_points = int(line[2]) + 1
            elif line[0] == 'regions':
                regions = int(line[2])
            elif line[0] == 'interface1_id':
                interface1_id = int(line[2])
            elif line[0] == 'interface2_id':
                interface2_id = int(line[2])
            elif line[0] == 'K':
                K = float(line[2])
            elif line[0] == 'density':
                density = float(line[2])
            elif line[0] == 'c':
                c = float(line[2])
            elif line[0] == 'p':
                p = float(line[2])
            elif line[0] == 'dt':
                dt = float(line[2])
            elif line[0] == 'dx':
                dx = float(line[2])
            elif line[0] == 'source_id':
                source_id = int(line[2])

    # init input values
    input_values = Input(n_points, t_steps, K, density, c, dt, dx)

    # create source object
    s = Source(source_id)

    # list of discretization points
    list_points = []

    # empty array for visu purposes
    visu_t = []

    for i in range(0, n_points):
        list_points.append(Point(i, K, density, c, p, input_values))

    # plt.ion()

    for t in range(0, t_steps):
        # print("t=", t)
        # compute stuff, except on boundaries
        for n in range(1, n_points - 1):
            list_points[n].solve_p_t(t, input_values, list_points[n - 1], list_points[n + 1], s)
            # list_points[n].print_point(t)

        # do plotting stuff
        tmp_p_t = []

        for n in range(0, n_points):
            tmp_p_t.append(list_points[n].get_p_t()[t])

        if t == 1900:
            plt.plot(tmp_p_t)
            plt.show()

        visu_t.append(tmp_p_t)

    plt.rcParams["image.cmap"] = 'inferno'
    plt.imshow(visu_t)
    plt.colorbar()
    # plt.savefig('myplot.png', dpi=1200)
    plt.show()


main()
