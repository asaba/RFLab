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

from debug import FSV_class, SMB_class
from instrumentmeasures import readFSV_marker, FSV_reset_setup
import utility
from scriptutility import Frequency_Range

# create dummy class and objects for debugging
if "SMB_LO" not in globals() or "SMB_RF" not in globals():
    # print("SMB_LO or SMB_RF not defined")
    SMB_LO = SMB_class()
    SMB_RF = SMB_class()

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

FSV_delay = 1

spectrum_analyzer_state = "ON"
spectrum_analyzer_sweep_points = 1001
spectrum_analyzer_resolution_bandwidth = 1
spectrum_analyzer_resolution_bandwidth_unit = unit.KHz
spectrum_analyzer_video_bandwidth = 1
spectrum_analyzer_video_bandwidth_unit = unit.KHz
spectrum_analyzer_frequency_span = 100
spectrum_analyzer_frequency_span_unit = unit.KHz
spectrum_analyzer_frequency_marker_unit = unit.KHz
# spectrum_analyzer_attenuation = 0
gainAmplifier = 40  # dB
spectrum_analyzer_IF_atten_enable = True
spectrum_analyzer_IF_atten = 0
spectrum_analyzer_IF_relative_level_enable = False
spectrum_analyzer_IF_relative_level = 30
threshold_power = 30  # dB

result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"


# result_file_name = "D:\\Users\\Andrea\\Documents\\Lavoro\\2015\\INAF\\MisureLNA\\test_cable"
# Freqeunza strat , stop step

def measure_calibration_cable(SMB=SMB_RF,
                              FSV=FSV,
                              synthetizer_frequency=synthetizer_frequency,
                              synthetizer_fix_power=synthetizer_fix_power,  # dBm
                              spectrum_analyzer_state=spectrum_analyzer_state,
                              spectrum_analyzer_sweep_points=spectrum_analyzer_sweep_points,
                              spectrum_analyzer_resolution_bandwidth=spectrum_analyzer_resolution_bandwidth,
                              spectrum_analyzer_resolution_bandwidth_unit=spectrum_analyzer_resolution_bandwidth_unit,
                              spectrum_analyzer_video_bandwidth=spectrum_analyzer_video_bandwidth,
                              spectrum_analyzer_video_bandwidth_unit=spectrum_analyzer_video_bandwidth_unit,
                              spectrum_analyzer_frequency_span=spectrum_analyzer_frequency_span,
                              spectrum_analyzer_frequency_span_unit=spectrum_analyzer_frequency_span_unit,
                              # spectrum_analyzer_attenuation = spectrum_analyzer_attenuation,
                              gainAmplifier=gainAmplifier,  # dB
                              spectrum_analyzer_IF_atten_enable=spectrum_analyzer_IF_atten_enable,
                              spectrum_analyzer_IF_atten=spectrum_analyzer_IF_atten,
                              spectrum_analyzer_IF_relative_level=spectrum_analyzer_IF_relative_level_enable,
                              spectrum_analyzer_IF_relative_level_enable=spectrum_analyzer_IF_relative_level_enable,
                              threshold_power=threshold_power,  # dB
                              spectrum_analyzer_frequency_marker_unit=spectrum_analyzer_frequency_marker_unit,
                              FSV_delay=FSV_delay,
                              result_file_name=result_file_name,
                              dummy_cable_power_level=0,
                              create_dummy_cable=False,
                              createprogressdialog=None
                              ):
    dialog = createprogressdialog
    values = []  # variable for results

    # reset the synthetizer SMB100A
    SMB.write("*rst")

    # imposta la modalit� di funzionamento del SMB100A
    SMB.write("FREQ:MODE FIX")
    SMB.write("POW:MODE FIX")
    command = "POW " + str(synthetizer_fix_power)
    SMB.write(command)

    FSV_reset_setup(FSV, spectrum_analyzer_sweep_points,
                    spectrum_analyzer_resolution_bandwidth,
                    spectrum_analyzer_resolution_bandwidth_unit,
                    spectrum_analyzer_video_bandwidth,
                    spectrum_analyzer_video_bandwidth_unit,
                    spectrum_analyzer_frequency_span,
                    spectrum_analyzer_frequency_span_unit,
                    spectrum_analyzer_IF_atten_enable,
                    spectrum_analyzer_IF_atten,
                    spectrum_analyzer_IF_relative_level_enable,
                    spectrum_analyzer_IF_relative_level)

    FSV.write("CALC:MARKER ON")  # enable marker mode

    calibration_IF = []
    calibration_function_IF = None
    calibration_function_IF_unit = unit.Hz

    frequency_range = synthetizer_frequency.return_range()

    maxcount = len(frequency_range)
    count = 0

    continue_progress = (True, True)
    for f in frequency_range:  # frequency loop
        # set SMB100A frequency
        f_value = str(f)
        current_frequency = f_value + unit.return_unit_str(unit.Hz)
        current_frequency_human_readable = unit.return_human_readable_str(f)
        command = "FREQ " + current_frequency  # Ex. FREQ 500kHz
        SMB.write(command)
        SMB.write("OUTP ON")
        time.sleep(2)
        data_now = str(datetime.datetime.now())
        if create_dummy_cable:
            values.append([f_value, unit.return_unit_str(unit.Hz)] + [str(dummy_cable_power_level)] + [data_now])
        else:
            values.append([f_value, unit.return_unit_str(unit.Hz)] +
                          readFSV_marker(FSV,
                                         FSV_delay,
                                         f,
                                         unit.return_unit_str(unit.Hz),
                                         unit.Hz,
                                         calibration_IF=[],
                                         calibration_IF_function=None,
                                         calibration_IF_function_unit=None) + [data_now])
        # turn off RF
        SMB.write("OUTP OFF")

        count += 1

        if not createprogressdialog is None:
            import wx
            wx.MicroSleep(500)
            message = "{lo_freq}".format(lo_freq=current_frequency_human_readable)
            newvalue = int(float(count) / maxcount * 100)
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
        if f == frequency_range[-1]:
            # safety turn Off
            # dialog.Update(100, "Measure completed)
            dialog.Destroy()

    # turn off RF
    SMB.write("OUTP OFF")

    # Output [Frequenza, output power meter(Loss), time]

    print("Misure completed\n")

    # build header for data table on file
    header = ["Frequency", "Unit"]
    values_headers = []
    values_headers.append("Loss value(dB)")
    values_headers.append("Time")
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
    sys.exit(measure_calibration_cable(SMB=SMB_RF, FSV=FSV))
