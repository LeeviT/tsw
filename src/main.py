import numpy as np
import matplotlib.pyplot as plt
from class_defs import Point
from class_defs import Input
from class_defs import Source
import matplotlib.animation as animation


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
            elif line[0] == 'freq':
                freq = int(line[2])

    # init input values
    input_values = Input(n_points, t_steps, K1, K2, K3, density1, density2, density3, dt, dx)

    # create source object
    s = Source(source_id, freq)

    # list of discretization points
    list_points = []

    # empty array for visu purposes
    visu_t = []

    # c(x), density(x), K(x) array
    c = np.zeros(input_values.get_n_points())
    density = np.zeros(input_values.get_n_points())
    K = np.zeros(input_values.get_n_points())

    # set velocity structure to arrays in respect of the regions
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

    # add all the Point objects to a array
    for i in range(0, n_points):
        list_points.append(Point(i, K[i], density[i], c[i], 0.0, input_values))

    # init images array
    fig = plt.figure()
    images = []

    # loop over all the time steps
    for t in range(0, t_steps):

        # compute stuff, except on boundaries
        for n in range(1, n_points - 1):
            # solve p_t for the current point
            list_points[n].solve_p_t(t, input_values, list_points[n - 1], list_points[n + 1], s)

        # init temporary array
        tmp_p_t = []

        # append t_p to temporary array
        for n in range(0, n_points):
            tmp_p_t.append(list_points[n].get_p_t()[t])

        # plot wave every 20th time step and add it to a image array
        if t % 20 == 0:
            plt.dpi = 100
            # plot interfaces as dots if regions > 1
            if regions == 2:
                plt.plot(interface1_id, 0, 'o', color='k')
            elif regions == 3:
                plt.plot(interface1_id, 0, 'o', color='k')
                plt.plot(interface2_id, 0, 'o', color='g')
            # set title and labels
            plt.title("Three regions")
            plt.xlabel('x')
            plt.ylabel('pressure (Pa)')
            image_t, = plt.plot(tmp_p_t, 'r', animated=True, linewidth=3)
            images.append([image_t])

        visu_t.append(tmp_p_t)

    # animation stuff
    anim = animation.ArtistAnimation(fig, images, interval=50)
    anim.save('animation.mp4', writer='ffmpeg')

    # x-t domain plotting stuff
    fig, ax = plt.subplots(1, 1)
    plt.rcParams["image.origin"] = 'lower'
    plt.rcParams["image.cmap"] = 'inferno'
    plt.xlabel("x (meters)")
    plt.ylabel("time (seconds)")
    img = ax.imshow(visu_t, extent=[0, input_values.get_n_points() * input_values.get_dx(), 0,
                                    input_values.get_t_steps() * input_values.get_dt() * 500])
    ax.set_xticks([0, 0.2 * input_values.get_n_points() * input_values.get_dx(),
                   0.4 * input_values.get_n_points() * input_values.get_dx(),
                   0.6 * input_values.get_n_points() * input_values.get_dx() - input_values.get_dx(),
                   0.8 * input_values.get_n_points() * input_values.get_dx() - input_values.get_dx(),
                   input_values.get_n_points() * input_values.get_dx() - input_values.get_dx()])
    ax.set_yticks([0, 500 * 0.25 * input_values.get_t_steps() * input_values.get_dt(),
                   500 * 0.5 * input_values.get_t_steps() * input_values.get_dt(),
                   500 * 0.75 * input_values.get_t_steps() * input_values.get_dt(),
                   500 * input_values.get_t_steps() * input_values.get_dt()])
    ax.set_yticklabels([0, 0.25 * input_values.get_t_steps() * input_values.get_dt(),
                        0.5 * input_values.get_t_steps() * input_values.get_dt(),
                        0.75 * input_values.get_t_steps() * input_values.get_dt(),
                        input_values.get_t_steps() * input_values.get_dt()])
    fig.colorbar(img)
    plt.savefig('plot.png', dpi=500)
    plt.show()


main()
