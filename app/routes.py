import numpy as np
from app import app
from flask import request, jsonify
from calculations.MatrixConversion import MatrixConversion
from calculations.Metrics import Metrics


@app.route('/api', methods=['GET', 'POST'])
def index():
    req_body = request.get_json()
    matrix = MatrixConversion(
        req_body["flows"], req_body["dates"], req_body["start_date"])

    result = {}
    result["flow_matrix"] = np.where(
        np.isnan(matrix.flow_matrix), None, matrix.flow_matrix).tolist()
    result["start_date"] = matrix.start_date

    calculated_metrics = Metrics(
        matrix.flow_matrix, matrix.years_array, None, None)

    result["year_ranges"] = calculated_metrics.year_ranges
    result["DRH"] = calculated_metrics.drh

    result["all_year"] = {}
    result["all_year"]["average_annual_flows"] = calculated_metrics.average_annual_flows
    result["all_year"]["standard_deviations"] = calculated_metrics.standard_deviations
    result["all_year"]["coefficient_variations"] = calculated_metrics.coefficient_variations

    result["winter"] = {}
    result["winter"]["timings"] = calculated_metrics.winter_timings
    result["winter"]["durations"] = calculated_metrics.winter_durations
    result["winter"]["magnitudes"] = calculated_metrics.winter_magnitudes
    result["winter"]["frequencys"] = calculated_metrics.winter_frequencys

    result["fall"] = {}
    result["fall"]["timings"] = calculated_metrics.fall_timings
    result["fall"]["magnitudes"] = calculated_metrics.fall_magnitudes
    result["fall"]["web_timings"] = calculated_metrics.fall_wet_timings
    result["fall"]["durations"] = calculated_metrics.fall_durations

    result["summer"] = {}
    result["summer"]["magnitudes_ten"] = calculated_metrics.summer_10_magnitudes
    result["summer"]["magnitudes_fifty"] = calculated_metrics.summer_50_magnitudes
    result["summer"]["durations_flush"] = calculated_metrics.summer_flush_durations
    result["summer"]["durations_wet"] = calculated_metrics.summer_wet_durations
    result["summer"]["no_flow_counts"] = calculated_metrics.summer_no_flow_counts

    result["spring"] = {}
    result["spring"]["timings"] = calculated_metrics.spring_timings
    result["spring"]["magnitudes"] = calculated_metrics.spring_magnitudes
    result["spring"]["durations"] = calculated_metrics.spring_durations
    result["spring"]["rocs"] = calculated_metrics.spring_rocs

    result["fall_winter"] = {}
    result["fall_winter"]["baseflows"] = calculated_metrics.wet_baseflows

    return jsonify(result), 200
