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
# from utility_v02 import save_data, save_settings
from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix, human_readable_frequency_unit
import pyvisa
# from utility import unit_class_my

from debug import FSV_class, SMB_class, SAB_class, NRP2_class
from instrumentmeasures import readNRP2
import utility
from scriptutility import Frequency_Range

if "SAB" not in globals():
    # print("SAB not defined")
    SAB = SAB_class()
    SAB_delay = 0
else:
    SAB_delay = 1

# create dummy class and objects for debugging
if "SMB_LO" not in globals() or "SMB_RF" not in globals():
    # print("SMB_LO or SMB_RF not defined")
    SMB_LO = SMB_class()
    SMB_RF = SMB_class()

if "NRP2" not in globals():

    # print("NRP2 not defined")
    NRP2 = NRP2_class()
    NRP2_delay = 0
else:
    NRP2_delay = 2

if "FSV" not in globals():

    # print("FSV not defined")
    FSV = FSV_class()
    FSV_delay = 0
else:
    FSV_delay = 1

VERSION = 7.0

unit = unit_class()

# imposta i valori del sintetizzatore
# 0 dbm per la potenza fissa
synthetizer_fix_power = 0  # dBm
# synthetizer_frequency_min_unit = unit.MHz
# synthetizer_frequency_min = 4600
# synthetizer_frequency_max_unit = unit.MHz
# synthetizer_frequency_max = 4700
# synthetizer_frequency_step_unit = unit.MHz
# synthetizer_frequency_step = 100
# synthetizer_frequency_unit = unit.MHz
synthetizer_frequency = Frequency_Range(4600, 4700, 100, unit.MHz)
synthetizer_frequency.to_base()

power_meter_make_zero = "ON"
power_meter_make_zero_delay = 10
power_meter_misure_number = 1
power_meter_misure_delay = 1000  # milliseconds

SAB_switch_01_delay = 2
SAB_switch_02_delay = 2

result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"


# result_file_name = "D:\\Users\\Andrea\\Documents\\Lavoro\\2015\\INAF\\MisureLNA\\test_cable"
# Freqeunza strat , stop step

def continous_measure_PM(NRP2=NRP2,
                              power_meter_misure_number=power_meter_misure_number,
                              power_meter_misure_delay=power_meter_misure_delay,  # milliseconds
                              result_file_name=result_file_name,
                              createprogressdialog=None
                              ):
    dialog = createprogressdialog
    values = []  # variable for results
    count = 0
    continue_progress = (True, True)

    NRP2.write("SYSTem:SPEed FAST")
    for n in range(0, power_meter_misure_number):  # number of reading
        data_now = str(datetime.datetime.now())
        values.append(readNRP2(None, NRP2, 1, power_meter_misure_delay, 0, unit.Hz, SAB_switch_delay=0, make_zero=False) + [data_now])
        count += 1

        if not createprogressdialog is None:
            import wx
            #wx.MicroSleep(1)
            message = "Read {count}".format(count=count)
            newvalue = int(float(count) / power_meter_misure_number * 100)
            if newvalue >= 100:
                createprogressdialog = False
                # dialog.Update(newvalue, message)
                # wx.MicroSleep(500)
                dialog.Close()
            else:
                continue_progress = dialog.Update(newvalue, message)
            if not continue_progress[0]:
                dialog.Destroy()
                break


    print("Misure completed\n")

    # build header for data table on file
    header = ["value(dB)", "Time"]
    values_headers = []
    # save data on file
    savefile_path = result_file_name + "_" + return_now_postfix() + ".csv"
    try:
        f_csv = open(savefile_path, "wb")
        create_csv(f_csv, header, values_headers, values)
        f_csv.close()
    except:
        # on error print data on standard output
        print(values)

    return savefile_path


# def readNRP2(NRP, NRP_delay, misure_number):
#
#    result_value = []
#    for i in range(0, misure_number): #loop for number of measures
#        time.sleep(NRP_delay)
#        command = "MEAS:SCAL:POW:AVG?"
#        x = NRP.ask(command)[0] #read NRP2 value
#        result_value.append(x)
#    return result_value



# create dummy class and objects for debugging
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
    sys.exit(measure_calibration_cable(SMB=SMB_RF, NRP2=NRP2, SAB=SAB))