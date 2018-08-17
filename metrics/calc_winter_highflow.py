import numpy as np
from utils.helpers import median_of_time, median_of_magnitude
from utils.FlowExceedance import FlowExceedance
from params import winter_params


def calc_winter_highflow_annual(matrix, exceedance_percent):
    max_nan_allowed_per_year = winter_params['max_nan_allowed_per_year']
    max_zero_allowed_per_year = winter_params['max_zero_allowed_per_year']

    exceedance_value = {}
    freq = {}
    duration = {}
    timing = {}
    magnitude = {}

    for i in exceedance_percent:
        exceedance_value[i] = np.nanpercentile(matrix, 100 - i)
        freq[i] = []
        duration[i] = []
        timing[i] = []
        magnitude[i] = []

    for column_number, _ in enumerate(matrix[0]):

        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number] == 0) > max_zero_allowed_per_year:
            for percent in exceedance_percent:
                freq[percent].append(None)
                duration[percent].append(None)
                timing[percent].append(None)
                magnitude[percent].append(None)
            continue

        exceedance_object = {}
        exceedance_duration = {}
        current_flow_object = {}

        """Init current flow object"""
        for percent in exceedance_percent:
            exceedance_object[percent] = []
            exceedance_duration[percent] = []
            current_flow_object[percent] = None

        """Loop through each flow value for the year to check if they pass exceedance threshold"""
        for row_number, flow_row in enumerate(matrix[:, column_number]):

            for percent in exceedance_percent:
                if bool(flow_row < exceedance_value[percent] and current_flow_object[percent]) or bool(row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]):
                    """End of an object if it falls below threshold, or end of column"""
                    current_flow_object[percent].end_date = row_number + 1
                    current_flow_object[percent].get_max_magnitude()
                    exceedance_duration[percent].append(
                        current_flow_object[percent].duration)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        """Begining of an object"""
                        exceedance_object[percent].append(
                            FlowExceedance(row_number, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                    else:
                        """Continuing an object"""
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1

        for percent in exceedance_percent:
            freq[percent].append(len(exceedance_object[percent]))
            if not np.nanmedian(exceedance_duration[percent]) or np.isnan(np.nanmedian(exceedance_duration[percent])):
                duration[percent].append(None)
            else:
                duration[percent].append(
                    np.nanmedian(exceedance_duration[percent]))

            if not median_of_time(exceedance_object[percent]) or np.isnan(median_of_time(exceedance_object[percent])):
                timing[percent].append(None)
            else:
                timing[percent].append(
                    median_of_time(exceedance_object[percent]))

            if not median_of_magnitude(exceedance_object[percent]) or np.isnan(median_of_magnitude(exceedance_object[percent])):
                magnitude[percent].append(None)
            else:
                magnitude[percent].append(
                    median_of_magnitude(exceedance_object[percent]))

    return timing, duration, freq, magnitude
