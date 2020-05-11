from scipy.integrate import quad as integrate
from math import ceil, floor, sin, pi, radians, atan, cos
import matplotlib.pyplot as plt
import numpy as np


def draw_plot(x_arguments, y_values, title="", x_label="", y_label="", figsize=None,
              is_grid=True, vlines=False, xticks=False, in_radians=False):
    plot = plt.figure(figsize=figsize).gca()

    if not vlines:
        plot.plot(x_arguments, y_values)
    else:
        if in_radians:
            plot.plot(x_arguments, list(map(lambda y: y * radians, y_values)), marker='.')
        else:
            plot.plot(x_arguments, y_values, marker='.')
        plot.vlines(x_arguments, 0, y_values)

    if xticks:
        plt.xticks(x_arguments)

    plot.set_title(title)
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)
    plt.grid(b=is_grid)
    plt.show()


def input_signal_function(t, t_i, amplitude, period):
    period_time_point = abs(t) - (ceil(abs(t) / period) - 1) * period


    if t > 0:
        if period_time_point < (t_i / 4):
            value = 4 * amplitude * period_time_point / t_i
        elif period_time_point < (t_i - t_i / 4):
            value = 4 * amplitude * (period_time_point - t_i / 2) / t_i
        elif period_time_point < t_i:
            value = (4 * amplitude * (period_time_point - t_i) / t_i)
        else:
            value = 0
    else:
        period_time_point = period - period_time_point
        if period_time_point < (t_i / 4):
            value = 4 * amplitude * period_time_point / t_i
        elif period_time_point < (t_i - t_i / 4):
            value = 4 * amplitude * (period_time_point - t_i / 2) / t_i
        elif period_time_point < t_i:
            value = (4 * amplitude * (period_time_point - t_i) / t_i)
        else:
            value = 0

    return value


def plot_input_signal(input_signal, start, end, step=1, title='Input Signal'):
    time_points = []
    values = []

    while start < end:
        time_points.append(start)
        values.append(input_signal(start))
        start += step

    draw_plot(time_points, values, title, 't', 's(t)', figsize=(8, 2))


def main():
    period = 33.3 * (10 ** -3)
    t_i = period * 2 / 3
    amplitude = 3.5
    delta_frequency = 350
    number_of_harmonics = 12

    omega = 2 * pi / period
    print(f'ω = {omega}')
    f1 = 1 / period
    print(f'f1 = {f1}')

    a0 = 0
    ak = lambda k: 2.23 * sin( pi * k / 3) / k + 1.06 * cos( 4 * pi * k / 3) / ( k * k )
    bk = lambda k: -2.23 * cos( pi * k / 3 ) / k - 2.23 * cos( pi * k ) + 1.06 * sin( pi * k / 3 ) / k**2
    original_input_signal = lambda t: input_signal_function(t, t_i, amplitude, period)

    coefficients_b = [bk(k + 1) for k in range(number_of_harmonics)]

    coefficients_a = [ak(k + 1) for k in range(number_of_harmonics)]

    sqrt_ak_bk = [(ak(k+1) + bk(k+1))**(1/2) for k in range(number_of_harmonics)]

    calculated_input_signal = lambda t: sum(
        [coefficients_a[k] * cos ( (k + 1 ) * omega * t) + coefficients_b[k] * sin((k + 1) * omega * t) for k in range(number_of_harmonics)]
    )

    plot_input_signal(input_signal=original_input_signal, start=-60, end=60, step=0.1,
                      title='Original Input Signal')

    

    plot_input_signal(input_signal=calculated_input_signal, start=-60, end=60, step=0.1,
                      title='Calculated Input Signal')

    psi = [atan ( ak(k+1) / bk(k+1) ) for k in range(number_of_harmonics)]
    print('\n\tψ(t) values:')
    for k in range(len(psi)):
        print('ψ%d = %.3f' % (k + 1, psi[k]))

    # draw_plot(list(np.arange(number_of_harmonics + 1)), [0] + [abs(a) for a in coefficients_a],
    #           title='Amplitude Spectre', x_label='k', y_label='A, v', vlines=True, xticks=True)
    # draw_plot(list(np.arange(number_of_harmonics + 1)), [0] + [abs(b) for b in coefficients_b],
    #           title='Amplitude Spectre', x_label='k', y_label='A, v', vlines=True, xticks=True)
    # draw_plot(list(np.arange(1, number_of_harmonics + 1)), psi,
    #           title='Phase Frequency Spectre', x_label='k', y_label='ψ, rad', vlines=True, xticks=True, in_radians=True)
    draw_plot(list(np.arange(number_of_harmonics + 1)), [abs(sqrt_ak_bk[0])] + [abs(ab) for ab in sqrt_ak_bk],
              title='Amplitude Spectre', x_label='k', y_label='A, v', vlines=True, xticks=True)

    print('\n\tCalculations')
    harmonics_quantity = floor(delta_frequency / f1)
    print('Harmonics quantity n = %d' % harmonics_quantity)
    signal_power = 0.5 * sum([coefficients_a[i] ** 2 + coefficients_b[i]**2 for i in range(harmonics_quantity)])
    print('Power of signal P = %.3f' % signal_power)
    full_average_signal_power = 1 / period * integrate(lambda t: calculated_input_signal(t) ** 2, 0, period)[0]
    print('Full average power of signal S^2 = %.3f' % full_average_signal_power)
    absolute_error = abs(full_average_signal_power - signal_power)
    print('Absolute error Δ = %.3f' % absolute_error)
    relative_error = absolute_error / full_average_signal_power * 100
    print('Relative error δ = %.3f' % relative_error, '%')


if __name__ == '__main__':
    main()