# encoding: utf-8

'''
Created on 01/12/2015

@author: Andrea

Cable calibration

'''

import sys
import numpy as np
import time
import datetime
#from utility_v02 import save_data, save_settings
from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix, human_readable_frequency_unit,\
    Generic_Range
from scriptutility import readcalibrationfile, calibrate, calibrationfilefunction, Frequency_Range
import pyvisa
#from utility import unit_class_my

from debug import SMB_class, PM5_class
from instrumentmeasures import readPM5

        

#create dummy class and objects for debugging
if "SMB_RF" not in globals():

    #print("SMB_LO or SMB_RF not defined")
    SMB_RF = SMB_class()
    

if "PM5" not in globals():

    #print("PM5 not defined")
    PM5 = PM5_class()  
    PM5_delay = 0
else:
    PM5_delay = 1




VERSION = 1.0

unit = unit_class()

#imposta i valori del sintetizzatore
#0 dbm per la potenza fissa
synthetizer_fix_power = 0 #dBm


#synthetizer_frequency_min = 4600
#synthetizer_frequency_max = 4700
#synthetizer_frequency_step = 100
#synthetizer_frequency_unit = unit.MHz
synthetizer_frequency = Frequency_Range(4600, 4700, 100, unit.MHz)
synthetizer_level = Generic_Range(0, 10, 1) 
#synthetizer_level_min = 0 #dBm
#synthetizer_level_max = 10 #dBm
#synthetizer_level_step = 1 #dBm
pm5_misure_number = 1
pm5_misure_delay = 1


result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"
calibration_cable_file_name = "C:\\Users\\Labele\\Desktop\\IP1\\misure calibrate\\CableLO_20160505122636.csv" 
#result_file_name = "D:\\Users\\Andrea\\Documents\\Lavoro\\2015\\INAF\\MisureLNA\\test_cable"
#Freqeunza strat , stop step

def measure_100GHz_cal(SMB = SMB_RF,
                    PM5 = PM5,
                    synthetizer_frequency = synthetizer_frequency,
                    synthetizer_level = synthetizer_level,
                    calibration_cable_file_name = calibration_cable_file_name,
                    pm5_misure_number = pm5_misure_number,
                    pm5_misure_delay = pm5_misure_delay,
                    result_file_name = result_file_name,
                    createprogressdialog = None
                    ):

    dialog = createprogressdialog


    calibration_LO = readcalibrationfile(calibration_cable_file_name)
    calibration_function_LO, calibration_function_LO_unit = calibrationfilefunction(calibration_LO)

    values = [] #variable for results

    #reset the synthetizer SMB100A
    SMB.write("*rst")
    
    #synthetizer_frequency_min = unit.convertion_to_base(synthetizer_frequency_min, synthetizer_frequency_unit)
    #synthetizer_frequency_max = unit.convertion_to_base(synthetizer_frequency_max, synthetizer_frequency_unit)
    #synthetizer_frequency_step = unit.convertion_to_base(synthetizer_frequency_step, synthetizer_frequency_unit)
    
    frequency_range = synthetizer_frequency.return_range()
    level_range = synthetizer_level.return_arange()


    maxcount = len(frequency_range) * len(level_range)
    count = 0
    
    SMB.write("OUTP ON")
    for f in frequency_range: #frequency loop
        #set SMB100A frequency
        f_value = str(f)
        current_frequency = f_value + unit.return_unit_str(unit.Hz) 
        current_frequency_human_readable = str(unit.convertion_from_base(f_value, human_readable_frequency_unit)) + unit.return_unit_str(human_readable_frequency_unit)  
        command = "FREQ " + current_frequency #Ex. FREQ 500kHz
        SMB.write(command)

        
        time.sleep(1) 
        for l in level_range:
            current_LO_level, calibration_LO_result =  calibrate(l, f,  unit.Hz, calibration_LO, calibration_function = calibration_function_LO, calibration_function_unit = calibration_function_LO_unit)
            
            current_level = str(current_LO_level)
            command = "POW " + current_level
            SMB.write(command)
            
            
            
            data_now = str(datetime.datetime.now())       
            values.append([f_value, unit.return_unit_str(unit.Hz), str(l), current_level, calibration_LO_result] + readPM5(PM5, pm5_misure_number, pm5_misure_delay) + [data_now])
            #turn off RF
            
            
            count +=1
            
            if not createprogressdialog is None:
                import wx
                wx.MicroSleep(500)
                message = "{lo_freq} {lo_level}dB".format(lo_freq = current_frequency_human_readable, lo_level = current_level)
                newvalue = int(float(count)/maxcount * 100)
                if newvalue >= 100:
                    createprogressdialog = False
                    #dialog.Update(newvalue, message)
                    #wx.MicroSleep(500)
                    dialog.Close()
                else:
                    dialog.Update(newvalue, message)
                    
                if f == frequency_range[-1] and l == level_range[-1]:
                    dialog.Destroy()


    #turn off RF
    SMB.write("OUTP OFF")
    PM5.closeport()
    #Output [Frequenza, output power meter(Loss), time]

    print("Misure completed\n")
   
    #build header for data table on file
    header = ["Frequency", "Unit", "Input Level", "Calibrated Level", "Calibration"]
    values_headers = []
    for v in range(0, pm5_misure_number):
        values_headers.append("Power (mW)")
    values_headers.append("Time")
    #save data on file
    try:
        f_csv = open(result_file_name + "_" + return_now_postfix() + ".csv", "wb")
        create_csv(f_csv, header, values_headers, values)
        f_csv.close()
    except:
        #on error print data on standard output
        print(values)


#create dummy class and objects for debugging
if "SMB_LO" not in globals():

    #print("SMB_LO not defined")
    SMB_LO = SMB_class()
    
if "PM5" not in globals():

    #print("PM5 not defined")
    PM5 = PM5_class()  
    PM5_delay = 0
else:
    PM5_delay = 1

if __name__ == "__main__":
    sys.exit(measure_100GHz_cal(SMB = SMB_LO, PM5 = PM5))