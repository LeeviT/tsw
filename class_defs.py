import numpy as np
import math


class Input:

    # initialization function
    def __init__(self, n_points, t_steps, K1, K2, K3, density1, density2, density3, dt, dx):
        self.n_points = n_points
        self.t_steps = t_steps
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.density1 = density1
        self.density2 = density2
        self.density3 = density3
        self.c1 = math.sqrt(self.K1 / self.density1)
        self.c2 = math.sqrt(self.K2 / self.density2)
        self.c3 = math.sqrt(self.K3 / self.density3)
        self.dt = dt
        self.dx = dx

    # getter functions, setters are not needed since this is literally input class and everything is defined in init()
    def get_n_points(self):
        return self.n_points

    def get_t_steps(self):
        return self.t_steps

    def get_K1(self):
        return self.K1

    def get_K2(self):
        return self.K2

    def get_K3(self):
        return self.K3

    def get_density1(self):
        return self.density1

    def get_density2(self):
        return self.density2

    def get_density3(self):
        return self.density3

    def get_c1(self):
        return self.c1

    def get_c2(self):
        return self.c2

    def get_c3(self):
        return self.c3

    def get_dt(self):
        return self.dt

    def get_dx(self):
        return self.dx


class Point:

    # initialization function
    def __init__(self, id, K, density, c, p_t, input_values):
        self.id = id
        self.K = K
        self.density = density
        self.c = c
        # here, p_t is array containing all the p(t) values over the time range of a specific point, init with zeroes
        # which will be however changed at some arbitrary time step if point contains the source as well i.e. there's
        # gaussian function changing p_t(current) value or it's changed by advancing wave
        self.p_t = np.zeros(input_values.get_t_steps() + 1)

    # getters and setters
    def get_id(self):
        return self.id

    def get_K(self):
        return self.K

    def get_density(self):
        return self.density

    def get_c(self):
        return self.c

    def get_p_t(self):
        return self.p_t

    def set_id(self, id_upd):
        self.id = id_upd

    def set_K(self, K_upd):
        self.K = K_upd

    def set_density(self, density_upd):
        self.density = density_upd

    def set_c(self, c_upd):
        self.c = c_upd

    def set_p_t(self, t_step, p_t_upd):
        self.p_t[t_step] = p_t_upd

    # solves future n+1 state of a single grid point
    def solve_p_t(self, t_step, input_values, left_point, right_point, source):
        if t_step == 0:
            p_prev = 0
        else:
            p_prev = self.get_p_t()[t_step - 1]

        if self.get_id() == source.get_source_id():
            source_current = source.s_t(t_step * input_values.get_dt(), input_values.get_dt())
        else:
            source_current = 0

        p_current = self.get_p_t()[t_step]
        left_p_current = left_point.get_p_t()[t_step]
        right_p_current = right_point.get_p_t()[t_step]

        p_future = (pow(self.get_c(), 2) * (pow(input_values.get_dt(), 2) / pow(input_values.get_dx(), 2))) \
                   * (right_p_current - 2 * p_current + left_p_current) + 2 * p_current - p_prev \
                   + pow(input_values.get_dt(), 2) * source_current

        self.set_p_t(t_step + 1, p_future)

    # printing function for debugging
    def print_point(self, t_step):
        print("id=" + str(self.get_id()).strip() + ", " + "K=" + str(self.get_K()).strip() + ", " + "density=" +
              str(self.get_density()).strip() + ", " + "c=" + str(self.get_c()).strip() + ", " + "p_t=" +
              str(self.get_p_t()[t_step]).strip())


class Source:

    # initialization function
    def __init__(self, source_id):
        self.source_id = source_id

    # getters and setters
    def get_source_id(self):
        return self.source_id

    # calculate intensity of source function at a given time step
    def s_t(self, t, dt):
        freq = 20
        t0 = 0.03
        magnitude = -8 * freq * (t - t0) * math.exp(-pow(4 * freq, 2) * pow(t - t0, 2))
        # magnitude = -0.5*math.sin(t*30)
        if abs(magnitude) >= 10e-18:
            # print("t: ", t, ", source: ", magnitude)
            return magnitude
        else:
            return 0
