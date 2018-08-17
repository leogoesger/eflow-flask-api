from datetime import datetime
import numpy as np


class MatrixConversion:

    def __init__(self, flow_array, date_array, start_date):
        self.flow_array = flow_array
        self.date_array = date_array
        self.start_date = start_date

        self.julian_array = []
        self.year_array = []  # Without duplicate, 1901, 1902, 1903
        self.years_array = []  # With duplicate, 1901, 1901, 1902, 1903
        self.flow_matrix = None
        self.get_date_arrays()
        self.get_flow_matrix()

    def get_date_arrays(self):

        for index, date in enumerate(self.date_array):

            current_date = datetime.strptime(date, "%m/%d/%Y")
            self.julian_array.append(current_date.timetuple().tm_yday)
            self.years_array.append(current_date.year)

            if index == 0:
                julian_start_date_first_year = datetime.strptime(
                    "{}/{}".format(self.start_date, current_date.year), "%m/%d/%Y").timetuple().tm_yday
                if(current_date.timetuple().tm_yday < julian_start_date_first_year):
                    first_year = current_date.year - 1
                else:
                    first_year = current_date.year

            if index == len(self.date_array) - 1:
                julian_start_date_last_year = datetime.strptime(
                    "{}/{}".format(self.start_date, current_date.year), "%m/%d/%Y").timetuple().tm_yday
                if(current_date.timetuple().tm_yday >= julian_start_date_last_year):
                    last_year = current_date.year + 1
                else:
                    last_year = current_date.year

        self.year_array = list(range(first_year, last_year))

    def get_position(self, year, julian_date, year_ranges, julian_start_date, days_in_year):
        row = julian_date - julian_start_date
        if (row < 0):
            row = row + days_in_year

        if(year > year_ranges[-1]):
            column = -1
        else:
            column = year_ranges.index(year)
            if (julian_date < julian_start_date):
                column = column - 1

        return row, column

    def get_flow_matrix(self):

        number_of_columns = len(self.year_array)

        flow_matrix = np.zeros((366, number_of_columns))
        flow_matrix.fill(None)

        for index, julian_date in enumerate(self.julian_array):
            if(self.years_array[index] % 4 == 0):
                days_in_year = 366
            else:
                days_in_year = 365

            julian_start_date = datetime.strptime(
                "{}/{}".format(self.start_date, self.years_array[index]), "%m/%d/%Y").timetuple().tm_yday
            row, column = self.get_position(
                self.years_array[index], julian_date, self.year_array, julian_start_date, days_in_year)

            flow_matrix[row][column] = self.flow_array[index]

        self.flow_matrix = flow_matrix
