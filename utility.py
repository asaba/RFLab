# encoding: utf-8

'''

Created on 10/ott/2015



@author: Andrea

'''

import csv
import openpyxl
import os
import datetime
from numpy import arange

VERSION = "5.6"

inkscape_exec = "C:\\Program Files\\Inkscape\\inkscape.com"

human_readable_frequency_unit = int(1e+9)  # GHz


def return_now_postfix():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def buildfitsfileslist(rootpath):
    result = []
    for root, dirs, files in os.walk(rootpath):
        for name in files:
            if str(name[-4:]) == ".svg":
                result.append(os.path.join(root, name))
    return result


class unit_class(object):
    def __init__(self):
        self.dBm = -2
        self.dB = -1
        self.Hz = 1
        self.KHz = 1000
        self.MHz = int(1e+6)
        self.GHz = int(1e+9)

    def return_unit_list(self):
        return [self.return_unit_str(self.dBm),
                self.return_unit_str(self.dB),
                self.return_unit_str(self.Hz),
                self.return_unit_str(self.KHz),
                self.return_unit_str(self.MHz),
                self.return_unit_str(self.GHz)]

    def return_unit_index_str(self, unit_str):
        unit_str = str(unit_str)
        if unit_str.upper() == "dBm".upper():
            return -2
        elif unit_str.upper() == "dB".upper():
            return -1
        elif unit_str.upper() == "Hz".upper():
            return 0
        elif unit_str.upper() == "KHz".upper():
            return 1
        elif unit_str.upper() == "MHz".upper():
            return 2
        elif unit_str.upper() == "GHz".upper():
            return 3

    def return_unit_index_value(self, unit_value):
        if unit_value == self.dBm:
            return 0
        elif unit_value == self.dB:
            return 1
        elif unit_value == self.Hz:
            return 2
        elif unit_value == self.KHz:
            return 3
        elif unit_value == self.MHz:
            return 4
        elif unit_value == self.GHz:
            return 5

    def return_unit_index(self, unit_x):
        if type(unit_x) is str:
            return self.return_unit_index_str(unit_x)
        else:
            return self.return_unit_index_value(unit_x)

    def return_unit(self, unit_str):
        unit_str = str(unit_str)
        if unit_str.upper() == "dBm".upper():
            return self.dBm
        elif unit_str.upper() == "dB".upper():
            return self.dB
        elif unit_str.upper() == "Hz".upper():
            return self.Hz
        elif unit_str.upper() == "KHz".upper():
            return self.KHz
        elif unit_str.upper() == "MHz".upper():
            return self.MHz
        elif unit_str.upper() == "GHz".upper():
            return self.GHz

    def return_unit_str(self, unit_v):
        if unit_v == self.dBm:
            return "dBm"
        elif unit_v == self.dB:
            return "dB"
        elif unit_v == self.Hz:
            return "Hz"
        elif unit_v == self.KHz:
            return "KHz"
        elif unit_v == self.MHz:
            return "MHz"
        elif unit_v == self.GHz:
            return "GHz"

    def unit_conversion(self, value, initial_unit, destination_unit):
        if initial_unit < 0 or destination_unit < 0:
            return value
        return value / (destination_unit / float(initial_unit))

    def convertion_to_base(self, value, initial_unit):
        # if value is a text convert to number
        if type(value) is str or type(value) is unicode:
            value = eval_if(value)
        if initial_unit < 0:
            return value
        return int(round(self.unit_conversion(value, initial_unit, self.Hz)))

    def convertion_from_base(self, value, destination_unit):
        if destination_unit < 0:
            return value
        return self.unit_conversion(value, self.Hz, destination_unit)

    def return_human_readable_str(self, value, initial_unit=1):
        if initial_unit < 0:
            return str(value) + self.return_unit_str(initial_unit)
        else:
            return str(
                self.unit_conversion(value, initial_unit, human_readable_frequency_unit)) + " " + self.return_unit_str(
                human_readable_frequency_unit)


def writelineonfilesettings(f, parameter, value):
    if type(value) is str or type(value) is unicode:
        value = '"{}"'.format(value)
        value = value.replace("\\", "\\\\")
    f.write("{} = {}\n".format(parameter, value))


def buildcsvrow(tuplevalue):
    rowresult = []

    for v in tuplevalue:

        if str(v) == "OFF":

            rowresult.append(v)

        else:
            if type(v) is str:
                rowresult.append(v.replace(".", ","))
            else:
                rowresult.append(str(v).replace(".", ","))

    return rowresult


def save_harmonic(filename, values, save_xlsx=True):
    writemode = "wb"

    f = open(filename + ".csv", writemode)
    # Freq LO(unit), Level LO(DBm), Fundamental, 2 harmonic, 3 harmonic, ..., AMP_marker (dBm) = Spurius Level (1)]
    s_unit = values[0][1]
    harmonic_number = max([eval(row[12]) for row in values])
    harmonic_list = [str(x) + " Harmonic" for x in range(2, harmonic_number + 1)]

    header = ["Freq(" + s_unit + ")", "Level (dBm)", "Fundamental"] + harmonic_list + ["AMP_marker (dBm)"]

    harmonic = {}
    for row in values:
        freq = eval(row[0])
        level = eval(row[2])
        if freq in harmonic:  # freq
            if level in harmonic[freq]:  # level
                if len(harmonic[freq][level]) == eval(row[12]) - 1:
                    harmonic[freq][level].append(row[10])
                else:
                    print("Error in row")
            else:
                harmonic[freq][level] = [row[10]]
        else:
            harmonic[freq] = {level: [row[10]]}

    values_harmonic = []
    e = harmonic.keys()
    e.sort()
    for k in e:
        fh = harmonic[k].keys()
        fh.sort()
        for j in fh:
            values_harmonic.append([str(k), str(j)] + harmonic[k][j])

    # header = ["Freq LO", "unit", "Level LO", "LO Calibration", "Freq RF", "unit", "Level RF", "RF Calibration", "Spurius Freq", "unit", "Spurius Level"]

    create_csv(f, header, [], values_harmonic)

    f.close()

    if save_xlsx:
        f = filename + ".xlsx"
        create_xlsx(f, header, [], values)


def save_spurius(filename, values, save_xlsx=True):
    writemode = "wb"

    f = open(filename + ".csv", writemode)
    header = ["Freq LO", "unit", "Level LO", "LO Calibration", "Freq RF", "unit", "Level RF", "RF Calibration",
              "Spurius Freq", "unit", "Spurius Level"]

    create_csv(f, header, [], values)

    f.close()

    if save_xlsx:
        f = filename + ".xlsx"
        create_xlsx(f, header, [], values)


def save_data(file_format, filename, values, misure_number, frequency_unit, fsv_att=False):
    # data on file

    header = ["Freq(" + frequency_unit + ")", "Level(dBm)", "Attenuation(dB)"]

    if fsv_att:
        header.append("FSV Attenuation(dB)")
    values_headers = []

    for v in range(0, misure_number):
        values_headers.append("Power Level(dB)")

    header_string = "   ".join(header) + "   ".join(values_headers) + "\n"

    if str(file_format) == "csv":
        writemode = "wb"
        f = open(filename + "." + file_format, writemode)
        create_csv(f, header, values_headers, values)
        f.close()

    elif str(file_format) == "txt":
        writemode = "w"
        f = open(filename + "." + file_format, writemode)
        f.write(header_string)
        for line in values:
            row = "   ".join(line) + "\n"
            f.write(row)
        f.close()

    elif str(file_format) == "xlsx":
        f = filename + "." + file_format
        create_xlsx(f, header, values_headers, values)


def save_settings(result_file_name, arguments_values):
    result = []
    result.append("measure_date : " + datetime.datetime.now().strftime("%Y%m%d%H%M%S %d/%m/%Y %H:%M:%S") + "\n")
    for key, value in arguments_values.iteritems():
        result.append(key + " : " + str(value) + "\n")
    now_postfix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    f = open(result_file_name + "_setting_" + now_postfix + ".txt", "w")

    for line in result:
        f.write(line)

    f.close()


def create_csv(filepointer, header, values_headers, values):
    csvwriter = open_csv_file(filepointer, header, values_headers)
    for line in values:
        add_csv_row(csvwriter, line)  # 'Testo', 


def create_xlsx(filename, header, values_headers, values):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(header + values_headers)
    for line in values:
        ws.append(line)  # 'Testo',

    wb.save(filename)


def open_csv_file(filepointer, header, values_headers):
    csvwriter = csv.writer(filepointer, dialect=csv.excel, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(['sep=,'])
    csvwriter.writerow(header + values_headers)
    return csvwriter


def add_csv_row(csvwriter, row):
    csvwriter.writerow(buildcsvrow(row))


def convert_txt_to_csv(filename_txt, filename_csv, txt_separator=None):
    f = open(filename_txt, "r")
    first_row = f.readline()
    f.close()
    if txt_separator:
        row_split = first_row.split(txt_separator)
    else:
        row_split = first_row.split()
    values_number = len(row_split[2:])
    header = ["date", "time"] + ["val" + str(i) for i in range(0, values_number)]
    f = open(filename_txt, "r")
    f_csv = open(filename_csv, "wb")
    writer_csv = open_csv_file(f_csv, header, [])
    for row in f:
        add_csv_row(writer_csv, row.split())
    f_csv.close()
    f.close()


class Generic_Range(object):
    def __init__(self, a_min, a_max, a_step):
        self.max = a_max
        self.min = a_min
        self.step = a_step

    def return_arange(self, step_correction=True):
        if step_correction:
            return arange(self.min, self.max + self.step, self.step)
        else:
            return arange(self.min, self.max, self.step)

    def return_range(self, step_correction=True):
        if step_correction:
            return range(self.min, self.max + self.step, self.step)
        else:
            return range(self.min, self.max, self.step)


def return_max_min_from_data_table_row(data_table_row, x_index, y_index=None, z_index=None):
    x_list = []
    y_list = []
    z_list = []

    for row in data_table_row:
        x_list.append(row[x_index])
        if y_index is not None:
            y_list.append(row[y_index])
        if z_index is not None:
            z_list.append(row[z_index])

    if len(y_list) == 0:
        y_list = [None]
    if len(z_list) == 0:
        z_list = [None]

    return max(x_list), min(x_list), max(y_list), min(y_list), max(z_list), min(z_list)


def return_max_min_from_data_table(data_table, x_index, y_index=None, z_index=None):
    x_u_list = []
    x_d_list = []
    y_u_list = [None]
    y_d_list = [None]
    z_u_list = [None]
    z_d_list = [None]
    for data_table_row in data_table:
        x_u, x_d, y_u, y_d, z_u, z_d = return_max_min_from_data_table_row(data_table_row, x_index, y_index, z_index)
        x_u_list.append(x_u)
        x_d_list.append(x_d)
        y_u_list.append(y_u)
        y_d_list.append(y_d)
        z_u_list.append(z_u)
        z_d_list.append(z_d)
    return max(x_u_list), min(x_d_list), max(y_u_list), min(y_d_list), max(z_u_list), min(z_d_list)


def eval_if(variable):
    if type(variable) is str or type(variable) is unicode:
        return eval(variable.replace(",", "."))
    else:
        return variable


class SplineError(Exception):
    pass


class PointNotFound(Exception):
    pass
