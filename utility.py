# encoding: utf-8

'''

Created on 10/ott/2015



@author: Andrea

'''



import csv
import datetime

VERSION = 4.0

def return_now_postfix():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

class unit_class(object):
    def __init__(self):
        self.Hz = 1
        self.KHz = 1000
        self.MHz = 1e+6
        self.GHz = 1e+9
        
    def return_unit_list(self):
        return [self.return_unit_str(self.Hz), self.return_unit_str(self.KHz), self.return_unit_str(self.MHz), self.return_unit_str(self.GHz)]
    
    def return_unit(self, unit_str):
        if unit_str.upper() == "Hz".upper():
            return self.Hz
        elif unit_str.upper() == "KHz".upper():
            return self.KHz
        elif unit_str.upper() == "MHz".upper():
            return self.MHz
        elif unit_str.upper() == "GHz".upper():
            return self.GHz
        
    def return_unit_str(self, unit_v):
        if unit_v == self.Hz:
            return "Hz"
        elif unit_v == self.KHz:
            return "KHz"
        elif unit_v == self.MHz:
            return "MHz"
        elif unit_v == self.GHz:
            return "GHz"
        
    def unit_conversion(self, value, initial_unit, destination_unit):
        return value / (destination_unit/initial_unit)
    
def writelineonfilesettings(f, parameter, value):
    
    if type(value) is str or type(value) is unicode:
        value = '"{}"'.format(value)
        value = value.replace("\\", "\\\\")
    f.write("{} = {}\n".format(parameter, value))
    
def buildcsvrow(tuplevalue):

    rowresult = []

    for v in tuplevalue:

        if v == "OFF":

            rowresult.append(v)

        else:
            if type(v) is str:
                rowresult.append(v.replace(".", ","))
            else:
                rowresult.append(str(v).replace(".", ","))

    return rowresult

def save_harmonic(filename, values):
    
    writemode = "wb"

    f = open(filename + ".csv", writemode)
    #Freq LO(unit), Level LO(DBm), Fundamental, 2 harmonic, 3 harmonic, ..., AMP_marker (dBm) = Spurius Level (1)]
    s_unit = values[0][1]
    harmonic_number = max([eval(row[12]) for row in values])
    harmonic_list = [str(x) + " Harmonic" for x in range(2, harmonic_number+1)]
    
    header = ["Freq(" + s_unit + ")", "Level (dBm)", "Fundamental"] + harmonic_list + ["AMP_marker (dBm)"]

    harmonic = {}
    for row in values:
        freq = eval(row[0])
        level = eval(row[2])
        if freq in harmonic: #freq
            if level in harmonic[freq]: #level
                if len(harmonic[freq][level]) == eval(row[12])-1:
                    harmonic[freq][level].append(row[10])
                else:
                    print("Error in row")
            else:
                harmonic[freq][level] = [row[10]]
        else:
            harmonic[freq] = {level : [row[10]]}
        
        
    values_harmonic = []
    e = harmonic.keys()
    e.sort()
    for k in e:
        fh = harmonic[k].keys()
        fh.sort()
        for j in fh:
            values_harmonic.append([str(k), str(j)] + harmonic[k][j])
            
    #header = ["Freq LO", "unit", "Level LO", "LO Calibration", "Freq RF", "unit", "Level RF", "RF Calibration", "Spurius Freq", "unit", "Spurius Level"]

    create_csv(f, header, [], values_harmonic)

    f.close()
    
def save_spurius(filename, values):
    
    writemode = "wb"

    f = open(filename + ".csv", writemode)
    header = ["Freq LO", "unit", "Level LO", "LO Calibration", "Freq RF", "unit", "Level RF", "RF Calibration", "Spurius Freq", "unit", "Spurius Level"]

    create_csv(f, header, [], values)

    f.close()

def save_data(file_format, filename, values, misure_number, frequency_unit, fsv_att = False):

        #data on file

    if file_format == "csv":

        writemode = "wb"

    else:

        writemode = "w"

    f = open(filename + "." + file_format, writemode)

    header = ["Freq(" + frequency_unit + ")", "Level(dBm)", "Attenuation(dB)"]
    
    if fsv_att:
        header.append("FSV Attenuation(dB)")
    values_headers = []

    for v in range(0, misure_number):

        values_headers.append("Power Level(dB)")

    header_string = "   ".join(header) + "   ".join(values_headers) + "\n"

    if file_format == "csv":

        create_csv(f, header, values_headers, values)
        

    elif file_format == "txt":

        f.write(header_string)

        for line in values:

            row= "   ".join(line) + "\n"

            f.write(row)

    

    f.close()

    
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

def open_csv_file(filepointer, header, values_headers):
    csvwriter = csv.writer(filepointer, dialect=csv.excel, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(['sep=,'])
    csvwriter.writerow(header+values_headers)
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
    header = ["date", "time"] + ["val"+ str(i) for i in range(0, values_number) ]
    f = open(filename_txt, "r")
    f_csv = open(filename_csv, "wb")
    writer_csv = open_csv_file(f_csv, header, [])
    for row in f:
        add_csv_row(writer_csv, row.split())
    f_csv.close()
    f.close()