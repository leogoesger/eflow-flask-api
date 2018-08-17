from metrics.calc_drh import calc_drh
from metrics.calc_all_year import calc_all_year
from metrics.calc_winter_highflow import calc_winter_highflow_annual
from metrics.calc_summer_baseflow import calc_start_of_summer, calc_summer_baseflow_durations_magnitude
from metrics.calc_fall_flush import calc_fall_flush_timings_durations
from metrics.calc_spring_transition import calc_spring_transition_timing_magnitude, calc_spring_transition_roc, calc_spring_transition_duration
from metrics.calc_fall_winter_baseflow import calc_fall_winter_baseflow


class Metrics:
    exceedance_percent = [2, 5, 10, 20, 50]

    def __init__(self, flow_matrix, year_ranges, start_year, end_year):
        self.flow_matrix = flow_matrix
        self.year_ranges = year_ranges
        self.start_year = start_year
        self.end_year = end_year

        if(self.start_year and self.end_year):
            self.year_ranges = year_ranges[start_year:end_year]
            self.flow_matrix = flow_matrix[:, start_year:end_year]

        self.all_year()
        self.winter_highflow_annual()
        self.start_of_summer()
        self.fall_flush_timings_durations()
        self.spring_transition_timing_magnitude()
        self.spring_transition_duration()
        self.spring_transition_roc()
        self.fall_winter_baseflow()
        self.summer_baseflow_durations_magnitude()
        self.get_DRH()

    def get_DRH(self):
        drh = calc_drh(self.flow_matrix)
        self.drh = drh

    def all_year(self):
        average_annual_flows, standard_deviations, coefficient_variations = calc_all_year(
            self.flow_matrix)
        self.average_annual_flows = average_annual_flows
        self.standard_deviations = standard_deviations
        self.coefficient_variations = coefficient_variations

    def winter_highflow_annual(self):
        winter_timings, winter_durations, winter_frequencys, winter_magnitudes = calc_winter_highflow_annual(
            self.flow_matrix, self.exceedance_percent)
        self.winter_timings = {}
        self.winter_durations = {}
        self.winter_frequencys = {}
        self.winter_magnitudes = {}

        for percent in self.exceedance_percent:
            self.winter_timings[percent] = winter_timings[percent]
            self.winter_durations[percent] = winter_durations[percent]
            self.winter_frequencys[percent] = winter_frequencys[percent]
            self.winter_magnitudes[percent] = winter_magnitudes[percent]

    def start_of_summer(self):
        summer_timings = calc_start_of_summer(self.flow_matrix)
        self.summer_timings = summer_timings

    def fall_flush_timings_durations(self):
        fall_timings, fall_magnitudes, fall_wet_timings, fall_durations = calc_fall_flush_timings_durations(
            self.flow_matrix, self.summer_timings)
        self.fall_timings = fall_timings
        self.fall_magnitudes = fall_magnitudes
        self.fall_wet_timings = fall_wet_timings
        self.fall_durations = fall_durations

    def summer_baseflow_durations_magnitude(self):
        summer_10_magnitudes, summer_50_magnitudes, summer_flush_durations, summer_wet_durations, summer_no_flow_counts = calc_summer_baseflow_durations_magnitude(
            self.flow_matrix, self.summer_timings, self.fall_timings, self.fall_wet_timings)
        self.summer_10_magnitudes = summer_10_magnitudes
        self.summer_50_magnitudes = summer_50_magnitudes
        self.summer_flush_durations = summer_flush_durations
        self.summer_wet_durations = summer_wet_durations
        self.summer_no_flow_counts = summer_no_flow_counts

    def spring_transition_timing_magnitude(self):
        spring_timings, spring_magnitudes = calc_spring_transition_timing_magnitude(
            self.flow_matrix, self.summer_timings)
        self.spring_timings = spring_timings
        self.spring_magnitudes = spring_magnitudes

    def spring_transition_duration(self):
        spring_durations = calc_spring_transition_duration(
            self.spring_timings, self.summer_timings)
        self.spring_durations = spring_durations

    def spring_transition_roc(self):
        spring_rocs = calc_spring_transition_roc(
            self.flow_matrix, self.spring_timings, self.summer_timings)
        self.spring_rocs = spring_rocs

    def fall_winter_baseflow(self):
        wet_baseflows_10 = calc_fall_winter_baseflow(
            self.flow_matrix, self.fall_wet_timings, self.summer_timings)
        self.wet_baseflows = wet_baseflows_10
