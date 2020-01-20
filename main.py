import numpy as np
import matplotlib.pyplot as plt
from class_defs import Point
from class_defs import Input
from class_defs import Source


def main():

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
            elif line[0] == 'K1':
                K1 = float(line[2])
            elif line[0] == 'K2':
                K2 = float(line[2])
            elif line[0] == 'K3':
                K3 = float(line[2])
            elif line[0] == 'density1':
                density1 = float(line[2])
            elif line[0] == 'density2':
                density2 = float(line[2])
            elif line[0] == 'density3':
                density3 = float(line[2])
            elif line[0] == 'dt':
                dt = float(line[2])
            elif line[0] == 'dx':
                dx = float(line[2])
            elif line[0] == 'source_id':
                source_id = int(line[2])

    # init input values
    input_values = Input(n_points, t_steps, K1, K2, K3, density1, density2, density3, dt, dx)

    # create source object
    s = Source(source_id)

    # list of discretization points
    list_points = []

    # empty array for visu purposes
    visu_t = []

    # c(x), density(x), K(x) array
    c = np.zeros(input_values.get_n_points())
    density = np.zeros(input_values.get_n_points())
    K = np.zeros(input_values.get_n_points())

    # Set velocity structure to arrays
    if regions == 1:
        c[:] = input_values.get_c1()
        density[:] = input_values.get_density1()
        K[:] = input_values.get_K1()
    if regions == 2:
        c[:interface1_id] = input_values.get_c1()
        density[:interface1_id] = input_values.get_density1()
        K[:interface1_id] = input_values.get_K1()
        c[interface1_id:] = input_values.get_c2()
        density[interface1_id:] = input_values.get_density2()
        K[interface1_id:] = input_values.get_K2()
    if regions == 3:
        c[:interface1_id] = input_values.get_c1()
        density[:interface1_id] = input_values.get_density1()
        K[:interface1_id] = input_values.get_K1()
        c[interface1_id:interface2_id] = input_values.get_c2()
        density[interface1_id:interface2_id] = input_values.get_density2()
        K[interface1_id:interface2_id] = input_values.get_K2()
        c[interface2_id:] = input_values.get_c3()
        density[interface2_id:] = input_values.get_density3()
        K[interface2_id:] = input_values.get_K3()

    for i in range(0, n_points):
        list_points.append(Point(i, K[i], density[i], c[i], 0.0, input_values))

    # plt.ion()

    for t in range(0, t_steps):
        # compute stuff, except on boundaries
        for n in range(1, n_points - 1):
            list_points[n].solve_p_t(t, input_values, list_points[n - 1], list_points[n + 1], s)
            # list_points[n].print_point(t)

        # do plotting stuff
        tmp_p_t = []

        # append temp
        for n in range(0, n_points):
            tmp_p_t.append(list_points[n].get_p_t()[t])

        if t == 1200:
            plt.plot(tmp_p_t)
            plt.show()

        visu_t.append(tmp_p_t)

    plt.figure(dpi=1000)
    plt.rcParams["image.cmap"] = 'inferno'
    plt.imshow(visu_t)
    plt.colorbar()
    # plt.savefig('myplot.png', dpi=1200)
    plt.show()


main()
