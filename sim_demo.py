import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from simDephaser import SimDephaser

x = stats.norm.pdf(np.arange(-5, 7, 0.01), 0, 1)
y = stats.norm.pdf(np.arange(-5, 7, 0.01), 4, 0.5)


fig, axs = plt.subplots(5, 1, sharex="all", sharey="all")

D = SimDephaser([x+y, -y], max_init_time_lag=0, linear_dephasing=1, non_linear_dephasing=0)
axs[0].plot(D.t, D.streams[0], color="#6479BC")
axs[0].plot(D.nt, D.streams[1], color="#F0B08D")
axs[0].set_title("Two streams synchronized")

D = SimDephaser([x+y, -y], max_init_time_lag=5, linear_dephasing=1, non_linear_dephasing=0)
axs[1].plot(D.t, D.streams[0], color="#6479BC")
axs[1].plot(D.nt, D.streams[1], color="#F0B08D")
axs[1].set_title("Initial desync only with time lag = {}s".format(D.init_time_lag))

D = SimDephaser([x+y, -y], max_init_time_lag=0, linear_dephasing=1.05, non_linear_dephasing=0)
axs[2].plot(D.t, D.streams[0], color="#6479BC")
axs[2].plot(D.nt, D.streams[1], color="#F0B08D")
axs[2].set_title(r"Linear desync only with $\alpha$ = {}".format(D.linear_dephasing))

D = SimDephaser([x+y, -y], max_init_time_lag=0, linear_dephasing=1, non_linear_dephasing=1)
axs[3].plot(D.t, D.streams[0], color="#6479BC")
axs[3].plot(D.nt, D.streams[1], color="#F0B08D")
axs[3].set_title("Non-linear desync only")

D = SimDephaser([x+y, -y], max_init_time_lag=10, linear_dephasing=1.05, non_linear_dephasing=1)
axs[4].plot(D.t, D.streams[0], color="#6479BC")
axs[4].plot(D.nt, D.streams[1], color="#F0B08D")
axs[4].set_title("The combination of three transformations")

# How to access the time signals from the time to the sample domain
# The current approach does not work well with time lags (e.g. 2 and 5)
D = SimDephaser([x+y, -y], max_init_time_lag=0, linear_dephasing=1, non_linear_dephasing=1)
y = D.streams[0]
z = D.streams_interp

fig.tight_layout()

plt.show()
