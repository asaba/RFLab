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
import pyvisa
#from utility import unit_class_my

from debug import FSV_class, SMB_class, SAB_class, NRP2_class
from instrumentmeasures import readNRP2


if "SAB" not in globals():
    print("SAB not defined")
    SAB = SAB_class()  
    SAB_delay = 0
else:
    SAB_delay = 1

        

#create dummy class and objects for debugging
if "SMB_LO" not in globals() or "SMB_RF" not in globals():

    print("SMB_LO or SMB_RF not defined")
    SMB_LO = SMB_class()
    SMB_RF = SMB_class()
    

if "NRP2" not in globals():

    print("NRP2 not defined")
    NRP2 = NRP2_class()
    NRP2_delay = 0
else:
    NRP2_delay = 2

if "FSV" not in globals():

    print("FSV not defined")
    FSV = FSV_class()  
    FSV_delay = 0
else:
    FSV_delay = 1




VERSION = 7.0

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

power_meter_make_zero = "ON"
power_meter_make_zero_delay = 10
power_meter_misure_number = 1
power_meter_misure_delay = 1 #seconds

SAB_switch_01_delay = 2
SAB_switch_02_delay = 2


result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"
#result_file_name = "D:\\Users\\Andrea\\Documents\\Lavoro\\2015\\INAF\\MisureLNA\\test_cable"
#Freqeunza strat , stop step

def measure_calibration_cable(SMB = SMB_RF,
                    NRP2 = NRP2,
                    SAB = SAB,
                    synthetizer_frequency_min_unit = synthetizer_frequency_min_unit,
                    synthetizer_frequency_min = synthetizer_frequency_min,
                    synthetizer_frequency_max_unit = synthetizer_frequency_max_unit,
                    synthetizer_frequency_max = synthetizer_frequency_max,
                    synthetizer_frequency_step_unit = synthetizer_frequency_step_unit,
                    synthetizer_frequency_step = synthetizer_frequency_step,
                    synthetizer_fix_power = synthetizer_fix_power, #dBm
                    power_meter_make_zero = power_meter_make_zero,
                    power_meter_make_zero_delay = power_meter_make_zero_delay,
                    power_meter_misure_number = power_meter_misure_number,
                    power_meter_misure_delay = power_meter_misure_delay, #seconds
                    SAB_switch_01_delay = SAB_switch_01_delay,
                    SAB_switch_02_delay = SAB_switch_02_delay,
                    result_file_name = result_file_name,
                    createprogressdialog = None
                    ):

    dialog = createprogressdialog

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
    SMB.write("FREQ:MODE FIX")
    SMB.write("POW:MODE FIX")
    command = "POW " + str(synthetizer_fix_power)
    SMB.write(command)
    
    synthetizer_frequency_min = unit.unit_conversion(synthetizer_frequency_min, synthetizer_frequency_min_unit, synthetizer_frequency_min_unit)
    synthetizer_frequency_max = unit.unit_conversion(synthetizer_frequency_max, synthetizer_frequency_max_unit, synthetizer_frequency_min_unit)
    synthetizer_frequency_step = unit.unit_conversion(synthetizer_frequency_step, synthetizer_frequency_step_unit, synthetizer_frequency_min_unit)
    
    frequency_range = np.arange(synthetizer_frequency_min, synthetizer_frequency_max + synthetizer_frequency_step, synthetizer_frequency_step)

    maxcount = len(frequency_range)
    count = 0
    
    
    for f in frequency_range: #frequency loop
        #set SMB100A frequency
        f_value = str(f)
        current_frequency = f_value + unit.return_unit_str(synthetizer_frequency_min_unit) 
        command = "FREQ " + current_frequency #Ex. FREQ 500kHz
        SMB.write(command)
        
        ##make zero, switch on load
        #command="SENS1:FREQ:FIX " +  current_frequency #Ex. FREQ 500kHz
        ##print(command)
        #NRP2.write(command)
        #SAB.write("SWT1 0")
        #time.sleep(SAB_switch_01_delay)
        #NRP2.write("CAL:ZERO:AUTO ONCE")
        ##NRP2.ask("CAL:ZERO:AUTO?")
        #time.sleep(power_meter_make_zero_delay)
        ##NRP2.write("*WAI")
        ##NRP2.ask("CAL:ZERO:AUTO?")
        
        ##switch on cable
        #SAB.write("SWT1 1")
        #time.sleep(SAB_switch_01_delay) 
        ##turn on RF
        SMB.write("OUTP ON")
        time.sleep(2) 
        data_now = str(datetime.datetime.now())       
        values.append([f_value, unit.return_unit_str(synthetizer_frequency_min_unit)] + readNRP2(SAB, NRP2, power_meter_misure_number, power_meter_misure_delay, f, synthetizer_frequency_min_unit, SAB_switch_01_delay, make_zero = True) + [data_now])
        #turn off RF
        SMB.write("OUTP OFF")
        
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
    header = ["Frequency", "Unit"]
    values_headers = []
    for v in range(0, power_meter_misure_number):
        values_headers.append("Loss value(dB)")
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
if "SMB_LO" not in globals() or "SMB_RF" not in globals():

    print("SMB_LO or SMB_RF not defined")
    SMB_LO = SMB_class()
    SMB_RF = SMB_class()
    
if "FSV" not in globals():

    print("FSV not defined")
    FSV = FSV_class()  
    FSV_delay = 0
else:
    FSV_delay = 1

if __name__ == "__main__":
    sys.exit(measure_calibration_cable(SMB = SMB_RF, NRP2 = NRP2, SAB = SAB))