# Copyright (C) 2026, Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Some interesting plots from microprocessors trend data.

See https://github.com/karlrupp/microprocessor-trend-data
"""

import numpy as np
from aptapy.models import Exponential
from aptapy.plotting import apply_stylesheet, plt, setup_gca

from common import DATA_DIR, savefigs

apply_stylesheet("aptapy-xkcd")


def plot_transistors():
    """Plot the number of transistors in microprocessors over time.
    """
    input_file_path = DATA_DIR / "karlrupp_microp_50y_transistors.dat"
    year, num_transistors = np.loadtxt(input_file_path, unpack=True)
    num_transistors *= 1000  # Original data is in thousands of transistors
    plt.figure()
    plt.plot(year, num_transistors, "o")
    model = Exponential(location=1970)
    model.prefactor.freeze(1500.)
    model.scale.minimum = -3.
    model.scale.set(-2.5)
    model.fit(year, num_transistors)
    print(model)
    model.plot()
    setup_gca(logy=True, xlabel="Anno di commercializzazione",
              ylabel="Numbero di transistor")
    plt.gca().grid(True, linestyle="--", linewidth=0.6)
    savefigs("microprocessor_transistors")


def plot_clock_frequency():
    """Plot the clock frequency of microprocessors over time.
    """
    input_file_path = DATA_DIR / "karlrupp_microp_50y_freq.dat"
    year, clock_frequency = np.loadtxt(input_file_path, unpack=True)
    plt.figure()
    plt.plot(year, clock_frequency, "o")
    setup_gca(logy=True, xlabel="Anno di commercializzazione",
              ylabel="Frequenza di clock (MHz)")
    plt.gca().grid(True, linestyle="--", linewidth=0.6)
    savefigs("microprocessor_clock_frequency")


def plot_num_cores():
    """Plot the number of cores in microprocessors over time.
    """
    input_file_path = DATA_DIR / "karlrupp_microp_50y_cores.dat"
    year, num_cores = np.loadtxt(input_file_path, unpack=True)
    plt.figure()
    plt.plot(year, num_cores, "o")
    setup_gca(logy=True, xlabel="Anno di commercializzazione",
              ylabel="Numbero di core")
    plt.gca().grid(True, linestyle="--", linewidth=0.6)
    savefigs("microprocessor_num_cores")


def run():
    plot_transistors()
    plot_clock_frequency()
    plot_num_cores()


if __name__ == "__main__":
    run()
    plt.show()
