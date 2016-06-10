'''
Created on 07/mag/2016

@author: sabah
'''

from utility import unit_class, csv, Generic_Range
from scipy.interpolate import UnivariateSpline
from numpy import array, arange

unit = unit_class()

def calibrate(input_power, input_frequency, input_frequency_unit, calibration_table, calibration_function = None, calibration_function_unit= None, round_freq = False):
    #Correct input_power by calibration_table for input frequency
    #Return the tuple (calibrated_power, "CAL") if frequency in calibration table
    #Else return (input power, "NOCAL")
    #If calibration_function spline is present it's used to calculate calibrated_power
    #if round_freq is True 
    calibrated_power = input_power
    calibration_result = "NOCAL"
    
    if calibration_function:
        i_freq = unit.unit_conversion(input_frequency, input_frequency_unit, calibration_function_unit)
        function_result = calibration_function(i_freq)
        return input_power - function_result, "CAL"
    
    if round_freq:
        if len(calibration_table) > 0:
            #build dictionary of Freq: pow
            power_dict ={}
            for t in calibration_table[1:]:
                #power dictionary {Cable Frequency (input_frequency_unit): calibrated power}
                power_dict[unit.unit_conversion(eval(t[0].replace(",", ".")), unit.return_unit(t[1]), input_frequency_unit)] = eval(t[2].replace(",", "."))
            
            #search the narrow value in power_dict keys
            #notes: lambda is equal to def func(x): return abs(x-input_frequency)
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
    
def calibrationfilefunction(calibrationresult):
    #return the spline function for calibration of cable
    #return None, unit.Hz
    if calibrationresult is []:
        return None, unit.Hz
    x_curve = []
    y_curve = []
    #if len()
    calibration_unit = unit.return_unit(calibrationresult[0][1])  
    for row in calibrationresult:
        x_curve.append(unit.convertion_to_base(eval(row[0].replace(",", ".")), calibration_unit))
        y_curve.append(eval(row[2].replace(",", ".")))
    
    return UnivariateSpline(array(x_curve), array(y_curve), s=0), unit.Hz

class Frequency_Range(Generic_Range):
    def __init__(self, a_min, a_max, a_step, a_unit):
        Generic_Range.__init__(self, a_min, a_max, a_step)
        self.unit = a_unit
        if self.unit == unit.dB:
            self.based = True
        else:
            self.based = False
        
    def to_base(self):
        if not self.based:
            self.max = unit.convertion_to_base(self.max, self.unit)
            self.min = unit.convertion_to_base(self.min, self.unit)
            self.step = unit.convertion_to_base(self.step, self.unit)
            self.based = True
        
    def from_base(self):
        if self.based and self.unit != unit.dB:
            return Frequency_Range(unit.convertion_from_base(self.min, self.unit), unit.convertion_from_base(self.max, self.unit), unit.convertion_from_base(self.step, self.unit), self.unit)
        else:
            return self