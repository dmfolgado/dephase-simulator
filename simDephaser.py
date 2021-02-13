import numpy as np
import scipy.interpolate as it


def linear_dephasing(t, alpha):
    return t * alpha


def non_linear_dephasing(t):
    nlt = np.cumsum(np.abs(np.random.rand(len(t))))
    # alternative method: nlt = np.cumsum(np.concatenate((np.zeros(int(len(t1) / 4)), np.bartlett(int(len(t1) / 2)), np.zeros(int(len(t1) / 4)))))
    nlt /= nlt[-1]

    return t + nlt


def init_time_lag(t, delta):
    return t + delta


class SimDephaser:
    def __init__(self, streams,
                 max_init_time_lag=10,
                 linear_dephasing=1.05,
                 non_linear_dephasing=1,
                 n_repeat=10,
                 sampling_frequency=50):

        self.n_repeat = n_repeat
        self.sampling_frequency = sampling_frequency
        self.streams = self.get_unsync_streams(streams)
        self.t = self.get_base_time_vector()
        self.init_time_lag = np.random.randint(max_init_time_lag) if max_init_time_lag > 0 else 0
        self.linear_dephasing = linear_dephasing
        self.non_linear_dephasing = non_linear_dephasing

        self.nt = self.get_unsync_time_vector()
        self.streams_interp = self.get_unsync_streams_interpolated()

    def get_base_time_vector(self):
        return np.arange(0, len(self.streams[0])/self.sampling_frequency, (1/self.sampling_frequency))

    def get_unsync_time_vector(self):
        _t = linear_dephasing(self.t, self.linear_dephasing)

        if self.non_linear_dephasing:
            _t = non_linear_dephasing(_t)

        _t = init_time_lag(_t, self.init_time_lag)

        return _t

    def get_unsync_streams(self, streams):
        return np.tile(streams[0], self.n_repeat), np.tile(streams[1], self.n_repeat)

    def get_unsync_streams_interpolated(self):
        # TODO: We still need to think a better solution for the cases where an offset is present
        _nt = self.nt - self.nt[0]
        return it.interp1d(_nt, self.streams[1])(np.arange(0, _nt[-1], self.t[1]))
