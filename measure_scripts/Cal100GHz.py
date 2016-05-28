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
from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix
from scriptutility import readcalibrationfile, calibrate
import pyvisa
#from utility import unit_class_my

from debug import SMB_class, PM5_class
from instrumentmeasures import readPM5

        

#create dummy class and objects for debugging
if "SMB_RF" not in globals():

    print("SMB_LO or SMB_RF not defined")
    SMB_RF = SMB_class()
    

if "PM5" not in globals():

    print("PM5 not defined")
    PM5 = PM5_class()  
    PM5_delay = 0
else:
    PM5_delay = 1




VERSION = 1.0

unit = unit_class()

#imposta i valori del sintetizzatore
#0 dbm per la potenza fissa
synthetizer_fix_power = 0 #dBm


synthetizer_frequency_min_unit = unit.MHz
synthetizer_frequency_min = 4600
synthetizer_frequency_max_unit = unit.MHz
synthetizer_frequency_max = 4700
synthetizer_frequency_step_unit = unit.MHz
synthetizer_frequency_step = 100
synthetizer_level_min = 0 #dBm
synthetizer_level_max = 10 #dBm
synthetizer_level_step = 1 #dBm
pm5_misure_number = 1
pm5_misure_delay = 1


result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"
calibration_cable_file_name = "C:\\Users\\Labele\\Desktop\\IP1\\misure calibrate\\CableLO_20160505122636.csv" 
#result_file_name = "D:\\Users\\Andrea\\Documents\\Lavoro\\2015\\INAF\\MisureLNA\\test_cable"
#Freqeunza strat , stop step

def measure_100GHz_cal(SMB = SMB_RF,
                    PM5 = PM5,
                    synthetizer_frequency_min_unit = synthetizer_frequency_min_unit,
                    synthetizer_frequency_min = synthetizer_frequency_min,
                    synthetizer_frequency_max_unit = synthetizer_frequency_max_unit,
                    synthetizer_frequency_max = synthetizer_frequency_max,
                    synthetizer_frequency_step_unit = synthetizer_frequency_step_unit,
                    synthetizer_frequency_step = synthetizer_frequency_step,
                    #synthetizer_fix_power = synthetizer_fix_power, #dBm
                    synthetizer_level_min = synthetizer_level_min,
                    synthetizer_level_max = synthetizer_level_max,
                    synthetizer_level_step = synthetizer_level_step,
                    calibration_cable_file_name = calibration_cable_file_name,
                    pm5_misure_number = pm5_misure_number,
                    pm5_misure_delay = pm5_misure_delay,
                    result_file_name = result_file_name,
                    createprogressdialog = None
                    ):

    dialog = createprogressdialog


    calibration_LO = readcalibrationfile(calibration_cable_file_name)
    #if createprogressdialog:
    #    import wx
    #    
    #    app = wx.App()
    #    dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
    #            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)

    values = [] #variable for results

    #reset the synthetizer SMB100A
    SMB.write("*rst")

    #imposta la modalit� di funzionamento del SMB100A
    #SMB.write("FREQ:MODE FIX")
    #SMB.write("POW:MODE FIX")
    #command = "POW " + str(synthetizer_fix_power)
    #SMB.write(command)
    
    synthetizer_frequency_min = unit.unit_conversion(synthetizer_frequency_min, synthetizer_frequency_min_unit, synthetizer_frequency_min_unit)
    synthetizer_frequency_max = unit.unit_conversion(synthetizer_frequency_max, synthetizer_frequency_max_unit, synthetizer_frequency_min_unit)
    synthetizer_frequency_step = unit.unit_conversion(synthetizer_frequency_step, synthetizer_frequency_step_unit, synthetizer_frequency_min_unit)
    
    frequency_range = np.arange(synthetizer_frequency_min, synthetizer_frequency_max + synthetizer_frequency_step, synthetizer_frequency_step)
    level_range = np.arange(synthetizer_level_min, synthetizer_level_max + synthetizer_level_step, synthetizer_level_step)


    maxcount = len(frequency_range)
    count = 0
    
    SMB.write("OUTP ON")
    for f in frequency_range: #frequency loop
        #set SMB100A frequency
        f_value = str(f)
        current_frequency = f_value + unit.return_unit_str(synthetizer_frequency_min_unit) 
        command = "FREQ " + current_frequency #Ex. FREQ 500kHz
        SMB.write(command)

        
        time.sleep(1) 
        for l in level_range:
            current_LO_level, calibration_LO_result =  calibrate(l, f,  synthetizer_frequency_min_unit, calibration_LO)
            
            current_level = str(current_LO_level)
            command = "POW " + current_level
            SMB_RF.write(command)
            
            
            
            data_now = str(datetime.datetime.now())       
            values.append([f_value, unit.return_unit_str(synthetizer_frequency_min_unit), str(l), current_level, calibration_LO_result] + readPM5(PM5, pm5_misure_number, pm5_misure_delay) + [data_now])
            #turn off RF
            
            
            count +=1
            
            if not createprogressdialog is None:
                import wx
                wx.MicroSleep(500)
                message = "{lo_freq}".format(lo_freq = current_frequency)
                newvalue = int(float(count)/maxcount * 100)
                dialog.Update(newvalue, message)
        


    #turn off RF
    SMB.write("OUTP OFF")

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





#def readNRP2(NRP, NRP_delay, misure_number):
#
#    result_value = []
#    for i in range(0, misure_number): #loop for number of measures
#        time.sleep(NRP_delay)
#        command = "MEAS:SCAL:POW:AVG?"
#        x = NRP.ask(command)[0] #read NRP2 value
#        result_value.append(x)
#    return result_value

        

#create dummy class and objects for debugging
if "SMB_LO" not in globals():

    print("SMB_LO not defined")
    SMB_LO = SMB_class()
    
if "PM5" not in globals():

    print("PM5 not defined")
    PM5 = PM5_class()  
    PM5_delay = 0
else:
    PM5_delay = 1

if __name__ == "__main__":
    sys.exit(measure_100GHz_cal(SMB = SMB_LO, PM5 = PM5))