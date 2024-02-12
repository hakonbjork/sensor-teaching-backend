import numpy as np
import statsmodels.api as sm


def compute_entertainment(hr):
    """
    Calculates these features which are correlated with entertainment:
    The average HRE
    The variance of the HR signal σ2
    The maximum HR max
    The minimum HR min
    The difference D between the maximum and the minimum HR
    The correlation coefficient R between HR recordings and the time t in which data were recorded
    This parameter provides a notion of the linearity of the signal (HR data) over time
    The autocorrelation ρ1 (lag equals 1) of the signal, which is used to detect the
    level of non-randomness in the HR data
    The approximate entropy (ApEnm,r)(Pincus 1991) of the signal which quantifies
    the unpredictability of fluctuations in the HR time series.

    :param hr: list of heart rate values
    :type hr: list of float
    :return: 9 different features as described above
    :rtype: (float, float, float, float, float, float, float, float, float)
    """
    def ApEn(U, m, r) -> float:
        """
        Approximate_entropy. Source:
        https://en.wikipedia.org/wiki/Approximate_entropy
        """

        def _maxdist(x_i, x_j):
            return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

        def _phi(m):
            x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
            C = [
                len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0)
                for x_i in x
            ]
            return (N - m + 1.0) ** (-1) * sum(np.log(C))
        N = len(U)
        return abs(_phi(m + 1) - _phi(m))

    hr = np.asarray(hr)
    avg_hr = np.average(hr)
    var_hr = np.var(hr)
    max_hr = np.amax(hr)
    min_hr = np.amin(hr)
    diff = max_hr - min_hr
    p = np.corrcoef(hr, np.arange(len(hr)))
    p1 = sm.tsa.acf(hr, nlags=1, fft=False)
    approximate_entropy = ApEn(hr, 2, 3)
    return avg_hr, var_hr, max_hr, min_hr, diff, p1[0], p1[1], approximate_entropy, p[0][1]
