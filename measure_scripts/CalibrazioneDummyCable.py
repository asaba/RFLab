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
from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix,\
    human_readable_frequency_unit
from scriptutility import Frequency_Range

#from utility import unit_class_my

#from debug import FSV_class, SMB_class, SAB_class, NRP2_class

VERSION = 7.0

unit = unit_class()


#imposta i valori del sintetizzatore
#synthetizer_frequency_min_unit = unit.MHz
#synthetizer_frequency_min = 4600
#synthetizer_frequency_max_unit = unit.MHz
#synthetizer_frequency_max = 4700
#synthetizer_frequency_step_unit = unit.MHz
#synthetizer_frequency_step = 100
synthetizer_frequency = Frequency_Range(4600, 4700, 100, unit.MHz)
synthetizer_frequency.to_base()

frequency_output_unit = unit.MHz

fixed_output_level = -40


#result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"
result_file_name = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\LO_dummy_cal"

def create_calibration_cable(
                    synthetizer_frequency = synthetizer_frequency,
                    fixed_output_level = fixed_output_level, #dBm
                    frequency_output_unit = frequency_output_unit,
                    result_file_name = result_file_name,
                    createprogressdialog = None
                    ):

    dialog = createprogressdialog
    #if createprogressdialog:
    #    import wx
    #    
    #    app = wx.App()
    #    dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
    #            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME )

    values = [] #variable for results
    #synthetizer_frequency_min = unit.unit_conversion(synthetizer_frequency_min, synthetizer_frequency_min_unit, frequency_output_unit)
    #synthetizer_frequency_max = unit.unit_conversion(synthetizer_frequency_max, synthetizer_frequency_max_unit, frequency_output_unit)
    #synthetizer_frequency_step = unit.unit_conversion(synthetizer_frequency_step, synthetizer_frequency_step_unit, frequency_output_unit)
    
    frequency_range = synthetizer_frequency.return_range()

    maxcount = len(frequency_range)
    count = 0
    
    
    for f in frequency_range: #frequency loop
        current_frequency_human_readable = str(unit.convertion_from_base(f, human_readable_frequency_unit)) + unit.return_unit_str(human_readable_frequency_unit)  
        data_now = str(datetime.datetime.now())       
        values.append([str(unit.convertion_from_base(f, frequency_output_unit)), unit.return_unit_str(frequency_output_unit), str(fixed_output_level), data_now])

        count +=1
        if not createprogressdialog is None:
            import wx
            wx.MicroSleep(500)
            message = "{lo_freq} {lo_pow}dB".format(lo_freq = current_frequency_human_readable, lo_pow = str(fixed_output_level))
            newvalue = min([int(count/maxcount * 100), 100])
            dialog.Update(newvalue, message)
            if newvalue == 100:
                createprogressdialog = False
                #dialog.Update(newvalue, message)
                #wx.MicroSleep(500)
                dialog.Close()
            else:
                dialog.Update(newvalue, message)
                
                
            if f == frequency_range[-1]:
                #safety turn Off
                #dialog.Update(100, "Measure completed)
                dialog.Destroy()    
            
    #Output [Frequenza, unit, output power meter(Loss), time]
    #if createprogressdialog:
    #    wx.MicroSleep(500)
    #    wx.CallAfter(dialog.Destroy())
    
    print("Misure completed\n")
    
    #build header for data table on file
    header = ["Frequency", "Unit", "Loss value(dB)", "Time"]
    values_headers = []
    #save data on file
    try:
        f_csv = open(result_file_name + "_" + return_now_postfix() + ".csv", "wb")
        create_csv(f_csv, header, values_headers, values)
        f_csv.close()
        return 1
    except:
        #on error print data on standard output
        print(values)
        return 0


if __name__ == "__main__":
    sys.exit(create_calibration_cable())