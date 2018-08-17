import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array


def median_of_time(lt):
    n = len(lt)
    if n < 1:
        return None
    elif n % 2 == 1:
        return lt[n//2].start_date
    elif n == 2:
        first_date = lt[0].start_date
        second_date = lt[1].start_date
        return (first_date + second_date) / 2
    else:
        first_date = lt[n//2 - 1].start_date
        second_date = lt[n//2 + 1].start_date
        return (first_date + second_date) / 2


def median_of_magnitude(object_array):
    flow_array = []

    for obj in object_array:
        flow_array.append(obj.max_magnitude)

    return np.nanmedian(np.array(flow_array, dtype=np.float))


def find_index(arr, item):
    for index, element in enumerate(arr):
        if element == item:
            return index


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    """
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


def replace_nan(flow_data):
    for index, flow in enumerate(flow_data):
        if index == 0 and np.isnan(flow):
            flow_data[index] = 0
        elif np.isnan(flow):
            flow_data[index] = flow_data[index-1]
    return flow_data


def crossings_nonzero_all(data):
    non_zero_array = []
    for index, element in enumerate(data):
        if index == len(data) - 5:
            return non_zero_array
        elif data[index + 1] > 0 and element < 0:
            non_zero_array.append(index)
        elif data[index + 1] < 0 and element > 0:
            non_zero_array.append(index)


def calculate_average_each_column(matrix):
    average = []

    index = 0
    for _ in matrix[0]:
        average.append(np.nanmean(matrix[:, index]))
        index = index + 1

    return average
