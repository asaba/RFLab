# encoding: utf-8

'''
Created on 01/12/2015

@author: Andrea

Spurius measurements

'''

import sys
import os
import csv
import numpy as np
import time
import datetime
from debug import FSV_class, SAB_class, NRP2_class, SMB_class
from utility import save_data, save_settings, unit_class, save_spurius, return_now_postfix, save_harmonic, \
    Generic_Range, human_readable_frequency_unit
from scriptutility import calibrate, readcalibrationfile, calibrationfilefunction, Frequency_Range
from instrumentmeasures import readFSV_marker, FSV_reset_setup

VERSION = 8.0

unit = unit_class()

calibration_file_LO = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_LO_enable = True
calibration_file_RF = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_RF_enable = True
calibration_file_IF = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_IF_enable = False
# D:\Users\Andrea\Desktop
result_file_name = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\misuraSpuri_TEST_HARMONIC"  # without extension

synthetizer_LO_state = "ON"
synthetizer_LO_frequency = Frequency_Range(4600, 5000, 500, unit.MHz)
synthetizer_LO_frequency.to_base()
synthetizer_LO_level = Generic_Range(10, 15, 5)

synthetizer_RF_state = "ON"
synthetizer_RF_frequency = Frequency_Range(3000, 4500, 500, unit.MHz)
synthetizer_RF_frequency.to_base()
synthetizer_RF_level = Generic_Range(-50, -25, 20)
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

# power meter
power_meter_state = "OFF"
power_meter_misure_number = 1
power_meter_misure_delay = 1  # seconds

# spurius calculation variables
m_RF = Generic_Range(-3, 0, 1)
n_LO = Generic_Range(0, 4, 1)
IF_low = 3000
IF_low_unit = unit.MHz
IF_high = 10000
IF_high_unit = unit.MHz
spurius_IF_unit = unit.MHz


def return_spurius_list(LO, RF, n_LO, m_RF, IF_low, IF_high):
    # build the spurius list table for the LO and RF frequency
    # table format: [Spurius Frequency, unit, LO frequency, RF frequency, n, m]
    # by the equation
    # spurius = n*LO - m*RF
    # remove the spurius for n and m = 0 and > IF_high

    n_LO_range = n_LO.return_range()
    if m_RF.min == 0 and m_RF.max == 0 and m_RF.step == 1:
        m_RF_range = m_RF.return_range(step_correction=False)
    else:
        m_RF_range = m_RF.return_range()

    result = []
    for n in n_LO_range:
        if len(m_RF_range) > 0:  # RF enabled
            for m in m_RF_range:
                if n == 0 and m == 0:
                    pass
                else:
                    current_spurius = n * LO + m * RF
                    if current_spurius > IF_low and current_spurius < IF_high:
                        result.append([current_spurius, unit.return_unit_str(unit.Hz), LO, RF, n, m])
        else:  # RF disable
            if n != 0:
                current_spurius = n * LO
                if current_spurius > IF_low and current_spurius < IF_high:
                    result.append([current_spurius, unit.Hz, LO, 0, n, 0])
    return result


def measure_LNA_spurius(SMB_LO, SMB_RF, FSV,
                        synthetizer_LO_state=synthetizer_LO_state,
                        synthetizer_LO_frequency=synthetizer_LO_frequency,
                        synthetizer_LO_level=synthetizer_LO_level,  # dBm
                        synthetizer_RF_state=synthetizer_RF_state,
                        synthetizer_RF_frequency=synthetizer_RF_frequency,
                        synthetizer_RF_level=synthetizer_RF_level,  # dBm
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
                        m_RF=m_RF,
                        n_LO=n_LO,
                        IF_low=IF_low,
                        IF_low_unit=IF_low_unit,
                        IF_high=IF_high,
                        IF_high_unit=IF_high_unit,
                        spurius_IF_unit=spurius_IF_unit,
                        calibration_file_LO=calibration_file_LO,
                        calibration_file_LO_enable=calibration_file_LO_enable,
                        calibration_file_RF=calibration_file_RF,
                        calibration_file_RF_enable=calibration_file_RF_enable,
                        calibration_file_IF=calibration_file_IF,
                        calibration_file_IF_enable=calibration_file_IF_enable,
                        result_file_name=result_file_name,
                        createprogressdialog=False):
    dialog = createprogressdialog
    # if createprogressdialog:
    #    import wx
    #    
    #    app = wx.App()
    #    dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
    #            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)


    values = []  # variable for results

    # reset the synthetizer SMB100A
    SMB_LO.write("*rst")
    SMB_RF.write("*rst")

    # reset spectrum analyzer
    # imposta la modalit� di funzionamento dei due SMB
    SMB_LO.write("FREQ:MODE FIX")
    SMB_LO.write("POW:MODE FIX")
    SMB_RF.write("FREQ:MODE FIX")
    SMB_RF.write("POW:MODE FIX")

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

    # load data for cables from calibration files
    if calibration_file_LO_enable:
        calibration_LO = readcalibrationfile(calibration_file_LO)
        calibration_function_LO, calibration_function_LO_unit = calibrationfilefunction(calibration_LO)
    else:
        calibration_LO = []
        calibration_function_LO = None
        calibration_function_LO_unit = unit.Hz
    if calibration_file_IF_enable:
        calibration_IF = readcalibrationfile(calibration_file_IF)
        calibration_function_IF, calibration_function_IF_unit = calibrationfilefunction(calibration_IF)
    else:
        calibration_IF = []
        calibration_function_IF = None
        calibration_function_IF_unit = unit.Hz
    if calibration_file_RF_enable:
        calibration_RF = readcalibrationfile(calibration_file_RF)
        calibration_function_RF, calibration_function_RF_unit = calibrationfilefunction(calibration_RF)
    else:
        calibration_RF = []
        calibration_function_RF = None
        calibration_function_RF_unit = unit.Hz
    totale_values = []
    if not synthetizer_LO_state:
        # set default parameter to skeep syntetizer loop
        synthetizer_LO_frequency = Frequency_Range(3000, 3000, 50, unit.MHz)  # same value of min for fixed value
        synthetizer_LO_frequency.to_base()
        synthetizer_LO_level = Generic_Range(-10, -10, 0.5)  # same value of min for fixed value

    if (not synthetizer_RF_state) or (m_RF.min == 0 and m_RF.max == 0 and m_RF.step == 1):
        # set default parameter to skeep syntetizer loop
        # By this mode is possibile calculate harmonic for LO frequency LO power
        synthetizer_RF_frequency = Frequency_Range(3000, 3000, 50, unit.MHz)  # same value of min for fixed value
        synthetizer_RF_frequency.to_base()
        synthetizer_RF_level = Generic_Range(-10, -10, 0.5)  # same value of min for fixed value

        m_step_RF = 0

    p = unicode("_".join(["PartialResults", return_now_postfix()]))
    partial_file_path = os.path.join(result_file_name, p)
    if not os.path.exists(partial_file_path):
        try:
            os.makedirs(partial_file_path)
        except:
            print("Error creating " + partial_file_path)
            return 0
    frequency_LO_range = synthetizer_LO_frequency.return_range()
    level_LO_range = synthetizer_LO_level.return_arange()
    level_RF_range = synthetizer_RF_level.return_arange()
    frequency_RF_range = synthetizer_RF_frequency.return_range()
    IF_high = unit.convertion_to_base(IF_high, IF_high_unit)
    IF_low = unit.convertion_to_base(IF_low, IF_low_unit)

    maxcount = float(len(frequency_LO_range) * len(level_LO_range) * len(level_RF_range) * len(frequency_RF_range))
    count = 0
    continue_progress = (True, True)

    for f_LO in frequency_LO_range:  # frequency loop
        # set SMB100A frequency for LO
        f_LO_value = str(f_LO)
        current_lo_frequency = f_LO_value + unit.return_unit_str(unit.Hz)
        current_lo_frequency_human_readable = unit.return_human_readable_str(f_LO)
        command = "FREQ " + current_lo_frequency  # Ex. FREQ 500kHz
        SMB_LO.write(command)

        for l_LO in level_LO_range:  # power level loop
            # set SMB100A level for LO
            # calculate calibrated value of level for LO
            current_LO_level, calibration_LO_result = calibrate(l_LO, f_LO, unit.Hz, calibration_LO,
                                                                calibration_function=calibration_function_LO,
                                                                calibration_function_unit=calibration_function_LO_unit)
            command = "POW " + str(current_LO_level)
            SMB_LO.write(command)
            # turn on LO
            SMB_LO.write("OUTP ON")

            for l_RF in level_RF_range:  # power level loop

                for f_RF in frequency_RF_range:  # frequency loop
                    values = []
                    # calculate calibrated value of level for RF
                    current_RF_level, calibration_RF_result = calibrate(l_RF, f_RF, unit.Hz, calibration_RF,
                                                                        calibration_function=calibration_function_RF,
                                                                        calibration_function_unit=calibration_function_RF_unit)
                    command = "POW " + str(current_RF_level)
                    SMB_RF.write(command)  # set level for RF
                    # set SMB100A frequency for RF
                    f_RF_value = str(f_RF)
                    current_rf_frequency = f_RF_value + unit.return_unit_str(unit.Hz)
                    current_rf_frequency_human_readable = unit.return_human_readable_str(f_RF)
                    command = "FREQ " + current_rf_frequency  # Ex. FREQ 500kHz
                    SMB_RF.write(command)

                    # calculate spurius frequency
                    spurius_tmp = return_spurius_list(f_LO, f_RF, n_LO, m_RF, IF_low, IF_high)
                    # turn on RF
                    SMB_RF.write("OUTP ON")
                    spurius_markers = readFSV_marker_spurius(FSV,
                                                             FSV_delay,
                                                             spurius_tmp,
                                                             unit.Hz,
                                                             calibration_IF,
                                                             calibration_IF_function=calibration_function_IF,
                                                             calibration_IF_function_unit=calibration_function_IF_unit)
                    count += 1

                    if not createprogressdialog is None:
                        import wx
                        wx.MicroSleep(500)
                        message = "LO {lo_freq} {lo_pow}dB - RF  {rf_freq} {rf_pow}dB".format(
                            lo_freq=current_lo_frequency_human_readable, lo_pow=str(current_LO_level),
                            rf_freq=current_rf_frequency_human_readable, rf_pow=str(current_RF_level))
                        newvalue = min([int(count / maxcount * 100), 100])
                        if newvalue == 100:
                            createprogressdialog = False
                            # dialog.Update(newvalue, message)
                            # wx.MicroSleep(500)
                            dialog.Close()
                        else:
                            continue_progress = dialog.Update(newvalue, message)

                    # load value for each spurius frequency
                    for s in spurius_markers:
                        # value = [LO frequency, unit, LO level, CAL/NOCAL, RF frequency, unit, RF level, CAL/NOCAL, Spurius Frequency, Spurius level]
                        # values.append([f_LO_value, unit.return_unit_str(synthetizer_LO_frequency_unit), str(current_LO_level), calibration_LO_result, f_RF_value, unit.return_unit_str(synthetizer_RF_frequency_unit), str(current_RF_level), calibration_RF_result] + s)
                        values.append(
                            [f_LO_value, unit.return_unit_str(unit.Hz), str(l_LO), calibration_LO_result, f_RF_value,
                             unit.return_unit_str(unit.Hz), str(l_RF), calibration_RF_result] + s)
                        totale_values.append(values[-1])
                        print(totale_values[-1])
                    # build filename - result_file_name_LOfrequency_unit_LOlevel_CAL/NOCAL_RFfrequency_unit_RFlevel_CAL/NOCAL_datetime
                    if len(spurius_markers) > 0:
                        spurius_filename = os.path.join(partial_file_path, "_".join(["R"] + values[0][0:-2]))
                        save_spurius(spurius_filename, values)

                    if not continue_progress[0]:
                        dialog.Destroy()
                        break
                    if f_LO == frequency_LO_range[-1] and l_LO == level_LO_range[-1] and l_RF == level_RF_range[
                        -1] and f_RF == frequency_RF_range[-1]:
                        # safety turn Off
                        # dialog.Update(100, "Measure completed)
                        dialog.Destroy()
                        # SMB_LO.write("OUTP OFF")
                        # SMB_RF.write("OUTP OFF")
                if not continue_progress[0]:
                    break
            if not continue_progress[0]:
                break
        if not continue_progress[0]:
            break

    # turn off LO and RF
    SMB_LO.write("OUTP OFF")
    SMB_RF.write("OUTP OFF")

    if m_RF.step == 0:
        harmonic_filename = result_file_name + "_TOTAL_HARMONIC_" + return_now_postfix()
        save_harmonic(harmonic_filename, totale_values)
        spurius_filename = result_file_name + "_TOTAL_" + return_now_postfix()
        save_spurius(spurius_filename, totale_values)
    else:
        spurius_filename = result_file_name + "_TOTAL_" + return_now_postfix()
        save_spurius(spurius_filename, totale_values)

    print("Misure completed\n")
    return spurius_filename


def readFSV_marker_harmonic(FSV, FSV_delay, central_frequency_value, central_frequency_unit, harmonic, attenuation_in,
                            gainAmplifier):
    result = []
    fsv_att_value = attenuation_in + gainAmplifier
    if fsv_att_value < 10:
        fsv_att_value = 10

    result.append(str(fsv_att_value))
    FSV.write("INP:ATT " + str(fsv_att_value))  # set attenuation

    for i in range(0, harmonic):
        freq = central_frequency_value * (i + 1)
        result += readFSV_marker(FSV, FSV_delay, str(freq) + central_frequency_unit)

    return result


def readFSV_marker_spurius(FSV,
                           FSV_delay,
                           spurius_list,
                           spurius_IF_unit,
                           calibration_IF,
                           calibration_IF_function,
                           calibration_IF_function_unit):
    # measure all spurius level from FSV
    # return list [[Frequency, Unit, Level, n, m], [Frequency, Unit, Level, n, m], ..., [Frequency, Unit, Level, n, m]]
    result = []

    for s in spurius_list:
        freq = s[0]
        freq_unit = unit.return_unit(s[1])
        result += [readFSV_marker(FSV,
                                  FSV_delay,
                                  freq,
                                  freq_unit,
                                  spurius_IF_unit,
                                  calibration_IF,
                                  calibration_IF_function,
                                  calibration_IF_function_unit) + [str(s[4]), str(s[5])]]
    return result


# ===============================================================================
# class unit_class():
#     def __init__(self):
#         self.Hz = 1
#         self.KHz = 1000
#         self.MHz = 1e+6
#         self.GHz = 1e+9
#         
#     def return_unit(self, unit_str):
#         if unit_str.upper() == "Hz".upper():
#             return self.Hz
#         elif unit_str.upper() == "KHz".upper():
#             return self.KHz
#         elif unit_str.upper() == "MHz".upper():
#             return self.MHz
#         elif unit_str.upper() == "GHz".upper():
#             return self.GHz
#         
#     def return_unit_str(self, unit_v):
#         if unit_v == self.Hz:
#             return "Hz"
#         elif unit_v == self.KHz:
#             return "KHz"
#         elif unit_v == self.MHz:
#             return "MHz"
#         elif unit_v == self.GHz:
#             return "GHz"
#         
#     def unit_conversion(self, value, initial_unit, destination_unit):
#         return value / (destination_unit/initial_unit)
# ===============================================================================


if "SAB" not in globals():
    # print("SAB not defined")
    SAB = SAB_class()
    SAB_delay = 0
else:
    SAB_delay = 1

# create dummy class and objects for debugging
if "SMB_LO" not in globals():
    # print("SMB_LO  not defined")
    SMB_LO = SMB_class()

if "SMB_RF" not in globals():
    # print("SMB_RF not defined")
    SMB_RF = SMB_class()

if "SMF_RF" not in globals():
    # print("SMF_RF not defined")
    SMF_RF = SMB_class()

if "SMF_LO" not in globals():
    # print("SMF_LO not defined")
    SMF_LO = SMB_class()

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

if __name__ == "__main__":
    sys.exit(measure_LNA_spurius(SMB_LO=SMF_LO, SMB_RF=SMB_RF, NRP2=NRP2, FSV=FSV))
