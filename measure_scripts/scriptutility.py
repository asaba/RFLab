'''
Created on 07/mag/2016

@author: sabah
'''

from utility import unit_class, csv

unit = unit_class()

def calibrate(input_power, input_frequency, input_frequency_unit, calibration_table, round_freq = False):
    #Correct input_power by calibration_table for input frequency
    #Return the tuple (calibrated_power, "CAL") if frequency in calibration table
    #Else return (input power, "NOCAL")
    calibrated_power = input_power
    calibration_result = "NOCAL"
    
    if round_freq:
        if len(calibration_table) > 0:
            #build dictionary of Freq: pow
            power_dict ={}
            for t in calibration_table[1:]:
                power_dict[unit.unit_conversion(eval(t[0].replace(",", ".")), unit.return_unit(t[1]), input_frequency_unit)] = eval(t[2].replace(",", "."))
                
            calibration_value = power_dict[min(power_dict, key=lambda x:abs(x-input_frequency))]
            calibration_result = "CAL"
            if input_power > 0:
                calibrated_power = input_power + calibration_value
            else:
                calibrated_power = input_power - calibration_value
        
    else:
        #check if input frequency is present in calibration_table
        for t in calibration_table:
            t_unit = unit.return_unit(t[1].strip())
            t_frequency = unit.unit_conversion(eval(t[0].replace(",", ".")), t_unit, input_frequency_unit)
            if input_frequency == t_frequency:
                calibration_value = eval(t[2].replace(",", "."))
                #result power lever = input power level - calibrated power level
                calibrated_power = input_power - calibration_value
                calibration_result = "CAL"
        
    return calibrated_power, calibration_result


def readcalibrationfile(filename):
    #open the calibration file and return the table of value without header
    #the table format is: [frequency, frequency unit, power output, datetime]
    #return empty table if error
    result = []
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        return result[2:] #remove separator and header
    except:
        return []