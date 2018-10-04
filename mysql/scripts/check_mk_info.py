#!/usr/bin/python3.5


def perfometer_check_mk_info(row, check_command, perf_data):
    number = int(perf_data[0][1])
    color = "#00ff00"
    return number, perfometer_linear(100,color)

perfometers['check_mk-check_mk_info'] = perfometer_check_mk_info