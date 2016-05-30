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
from utility import save_data, save_settings, unit_class, save_spurius, return_now_postfix, save_harmonic
from scriptutility import calibrate, readcalibrationfile, calibrationfilefunction

VERSION = 7.0

unit = unit_class()
        
calibration_file_LO = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_LO_enable = True
calibration_file_RF = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_RF_enable = True
calibration_file_IF = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\RF_cal.csv"
calibration_file_IF_enable = False
#D:\Users\Andrea\Desktop
result_file_name = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\ArduinoStepAttenuator\\v04\\misuraSpuri_TEST_HARMONIC" #without extension

synthetizer_LO_state = "ON"
synthetizer_LO_frequency_min_unit = unit.MHz
synthetizer_LO_frequency_min = 4600
synthetizer_LO_frequency_max_unit = unit.MHz
synthetizer_LO_frequency_max = 5000
synthetizer_LO_frequency_step_unit = unit.MHz
synthetizer_LO_frequency_step = 500
synthetizer_LO_level_min = 10 #dBm
synthetizer_LO_level_max = 15
synthetizer_LO_level_step =10

synthetizer_RF_state = "ON"
synthetizer_RF_frequency_min_unit = unit.MHz
synthetizer_RF_frequency_min = 3000
synthetizer_RF_frequency_max_unit = unit.MHz
synthetizer_RF_frequency_max = 4500
synthetizer_RF_frequency_step_unit = unit.MHz
synthetizer_RF_frequency_step = 500
synthetizer_RF_level_min = -50 #dBm
synthetizer_RF_level_max = -25
synthetizer_RF_level_step = 20
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
#spectrum_analyzer_attenuation = 0
gainAmplifier = 40 #dB
spectrum_analyzer_IF_atten_enable = True
spectrum_analyzer_IF_atten = 0
spectrum_analyzer_IF_relative_level_enable = False
spectrum_analyzer_IF_relative_level = 30
threshold_power = 30 #dB 

#power meter
power_meter_state = "OFF"
power_meter_misure_number = 1
power_meter_misure_delay = 1 #seconds


#spurius calculation variables
m_min_RF = 0
m_max_RF = 0 #set to 0 for harmonic only
m_step_RF = 1
n_min_LO = 0
n_max_LO = 4
n_step_LO = 1
IF_low = 3000
IF_low_unit = unit.MHz
IF_high = 10000
IF_high_unit = unit.MHz
spurius_IF_unit = unit.MHz

def return_spurius_list(LO, LO_unit, RF, RF_unit, n_min_LO, n_max_LO, n_step_LO, m_min_RF, m_max_RF, m_step_RF, IF_low, IF_low_unit, IF_high, IF_high_unit):
    #build the spurius list table for the LO and RF frequency
    #table format: [Spurius Frequency, unit, LO frequency, RF frequency, n, m]
    #by the equation
    #spurius = n*LO - m*RF
    #remove the spurius for n and m = 0 and > IF_high
    result = []
    IF_low_converted = unit.unit_conversion(IF_low, IF_low_unit, IF_high_unit)
    for n in range(n_min_LO, n_max_LO + n_step_LO, n_step_LO):
        if m_step_RF>0: # RF enabled
            for m in range(m_min_RF, m_max_RF + m_step_RF, m_step_RF):
                if n != 0 and m != 0:
                    current_spurius = n * unit.unit_conversion(LO, LO_unit, IF_high_unit) + m * unit.unit_conversion(RF, RF_unit, IF_high_unit)
                    current_spurius = round(current_spurius, 5)
                    if current_spurius > IF_low_converted and current_spurius < IF_high:
                        result.append([current_spurius, unit.return_unit_str(IF_high_unit), unit.unit_conversion(LO, LO_unit, IF_high_unit), unit.unit_conversion(RF, RF_unit, IF_high_unit), n, m])
        else: #RF disable
            if n != 0:
                current_spurius = n * unit.unit_conversion(LO, LO_unit, IF_high_unit)
                current_spurius = round(current_spurius, 5)
                if current_spurius > IF_low_converted and current_spurius < IF_high:
                    result.append([current_spurius, unit.return_unit_str(IF_high_unit), unit.unit_conversion(LO, LO_unit, IF_high_unit), unit.unit_conversion(LO, LO_unit, IF_high_unit), n, 0])
    return result


        

def measure_LNA_spurius(SMB_LO, SMB_RF, FSV,
                        synthetizer_LO_state = synthetizer_LO_state,
                        synthetizer_LO_frequency_min_unit = synthetizer_LO_frequency_min_unit,
                        synthetizer_LO_frequency_min = synthetizer_LO_frequency_min,
                        synthetizer_LO_frequency_max_unit = synthetizer_LO_frequency_max_unit,
                        synthetizer_LO_frequency_max = synthetizer_LO_frequency_max,
                        synthetizer_LO_frequency_step_unit = synthetizer_LO_frequency_step_unit,
                        synthetizer_LO_frequency_step = synthetizer_LO_frequency_step,
                        synthetizer_LO_level_min = synthetizer_LO_level_min, #dBm
                        synthetizer_LO_level_max = synthetizer_LO_level_max,
                        synthetizer_LO_level_step = synthetizer_LO_level_step,
                        synthetizer_RF_state = synthetizer_RF_state,
                        synthetizer_RF_frequency_min_unit = synthetizer_RF_frequency_min_unit,
                        synthetizer_RF_frequency_min = synthetizer_RF_frequency_min,
                        synthetizer_RF_frequency_max_unit = synthetizer_RF_frequency_max_unit,
                        synthetizer_RF_frequency_max = synthetizer_RF_frequency_max,
                        synthetizer_RF_frequency_step_unit = synthetizer_RF_frequency_step_unit,
                        synthetizer_RF_frequency_step = synthetizer_RF_frequency_step,
                        synthetizer_RF_level_min = synthetizer_RF_level_min, #dBm
                        synthetizer_RF_level_max = synthetizer_RF_level_max,
                        synthetizer_RF_level_step = synthetizer_RF_level_step,
                        #power_meter_state = power_meter_state,
                        #power_meter_misure_number = power_meter_misure_number,
                        #power_meter_misure_delay = power_meter_misure_delay, #seconds
                        spectrum_analyzer_state = spectrum_analyzer_state,
                        spectrum_analyzer_sweep_points = spectrum_analyzer_sweep_points,
                        spectrum_analyzer_resolution_bandwidth = spectrum_analyzer_resolution_bandwidth,
                        spectrum_analyzer_resolution_bandwidth_unit = spectrum_analyzer_resolution_bandwidth_unit,
                        spectrum_analyzer_video_bandwidth = spectrum_analyzer_video_bandwidth,
                        spectrum_analyzer_video_bandwidth_unit = spectrum_analyzer_video_bandwidth_unit,
                        spectrum_analyzer_frequency_span = spectrum_analyzer_frequency_span,
                        spectrum_analyzer_frequency_span_unit = spectrum_analyzer_frequency_span_unit,
                        #spectrum_analyzer_attenuation = spectrum_analyzer_attenuation,
                        gainAmplifier = gainAmplifier, #dB
                        spectrum_analyzer_IF_atten_enable = spectrum_analyzer_IF_atten_enable,
                        spectrum_analyzer_IF_atten = spectrum_analyzer_IF_atten,
                        spectrum_analyzer_IF_relative_level = spectrum_analyzer_IF_relative_level_enable,
                        spectrum_analyzer_IF_relative_level_enable = spectrum_analyzer_IF_relative_level_enable,
                        threshold_power = threshold_power, #dB 
                        spectrum_analyzer_frequency_marker_unit = spectrum_analyzer_frequency_marker_unit,
                        FSV_delay = FSV_delay,
                        m_min_RF = m_min_RF,
                        m_max_RF = m_max_RF,
                        m_step_RF = m_step_RF,
                        n_min_LO = n_min_LO,
                        n_max_LO = n_max_LO,
                        n_step_LO = n_step_LO,
                        IF_low = IF_low,
                        IF_low_unit = IF_low_unit,
                        IF_high = IF_high,
                        IF_high_unit = IF_high_unit,
                        spurius_IF_unit = spurius_IF_unit,
                        calibration_file_LO = calibration_file_LO,
                        calibration_file_LO_enable = calibration_file_LO_enable,
                        calibration_file_RF = calibration_file_RF,
                        calibration_file_RF_enable = calibration_file_RF_enable,
                        calibration_file_IF = calibration_file_IF,
                        calibration_file_IF_enable = calibration_file_IF_enable,
                        result_file_name = result_file_name,
                        createprogressdialog = False):


    dialog = createprogressdialog
    #if createprogressdialog:
    #    import wx
    #    
    #    app = wx.App()
    #    dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
    #            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
    
    
    values = [] #variable for results

    #reset the synthetizer SMB100A
    SMB_LO.write("*rst")
    SMB_RF.write("*rst")

    #reset spectrum analyzer
    FSV.write("*rst")

    #imposta la modalit� di funzionamento dei due SMB
    SMB_LO.write("FREQ:MODE FIX")
    SMB_LO.write("POW:MODE FIX")
    SMB_RF.write("FREQ:MODE FIX")
    SMB_RF.write("POW:MODE FIX")
    
    #imposta la modalit� di funzionamento dello spectrum analyzer
    FSV.write("SYST:DISP:UPD OFF") #diplay off
    FSV.write("INIT:CONT ON") #contiuous sweep mode
    FSV.write("DISP:WIND:TRAC:MODE WRIT") #lavora con Clr/Write mode
    FSV.write("FREQ:MODE SWE") #Selects the frequency domain
    FSV.write("SWE:POIN " + str(spectrum_analyzer_sweep_points)) #number of sweep points 101 to 32001 default 691
    FSV.write("BAND " + str(spectrum_analyzer_resolution_bandwidth) + unit.return_unit_str(spectrum_analyzer_resolution_bandwidth_unit)) #set the resolution bandwidth
    FSV.write("BAND:VID " + str(spectrum_analyzer_video_bandwidth) + unit.return_unit_str(spectrum_analyzer_video_bandwidth_unit)) #set video bandwidth
    FSV.write("FREQ:SPAN " + str(spectrum_analyzer_frequency_span) + unit.return_unit_str(spectrum_analyzer_frequency_span_unit)) #
    
    if spectrum_analyzer_IF_atten_enable == True:
        FSV.write("INP:ATT " + str(spectrum_analyzer_IF_atten)) #set attenuation
    if spectrum_analyzer_IF_relative_level_enable == True:
        FSV.write("DISP:WIND:TRAC:Y:RLEV " + spectrum_analyzer_IF_relative_level + "dBm")
    FSV.write("CALC:MARKER ON") #enable marker mode

    #load data for cables from calibration files
    if calibration_file_LO_enable:
        calibration_LO = readcalibrationfile(calibration_file_LO)
        calibration_function_LO, calibration_function_LO_unit = calibrationfilefunction(calibration_LO)
    else:
        calibration_LO = []
        calibration_function_LO = None
        calibration_function_LO_unit = unit.MHz
    if calibration_file_IF_enable:
        calibration_IF = readcalibrationfile(calibration_file_IF)
        calibration_function_IF, calibration_function_IF_unit = calibrationfilefunction(calibration_IF)
    else:
        calibration_IF = []
        calibration_function_IF = None
        calibration_function_IF_unit = unit.MHz
    if calibration_file_RF_enable:
        calibration_RF = readcalibrationfile(calibration_file_RF)
        calibration_function_RF, calibration_function_RF_unit = calibrationfilefunction(calibration_RF)
    else:
        calibration_RF = []
        calibration_function_RF = None
        calibration_function_RF_unit = unit.MHz
    totale_values = []
    if not synthetizer_LO_state:
        #set default parameter to skeep syntetizer loop
        synthetizer_LO_frequency_min_unit = unit.MHz
        synthetizer_LO_frequency_min = 3000
        synthetizer_LO_frequency_max_unit = unit.MHz
        synthetizer_LO_frequency_max = 3000 #same value of min for fixed value
        synthetizer_LO_frequency_step_unit = unit.MHz
        synthetizer_LO_frequency_step = 50 #>0

        synthetizer_LO_level_min = -10 #dBm
        synthetizer_LO_level_max = -10 #same value of min for fixed value
        synthetizer_LO_level_step = 0.5

    if (not synthetizer_RF_state) or (m_min_RF == 0 and m_max_RF == 0 and m_step_RF == 1):
        #set default parameter to skeep syntetizer loop
        #By this mode is possibile calculate harmonic for LO frequency LO power
        synthetizer_RF_frequency_min_unit = unit.MHz
        synthetizer_RF_frequency_min = 3000
        synthetizer_RF_frequency_max_unit = unit.MHz
        synthetizer_RF_frequency_max = 3000  #same value of min for fixed value
        synthetizer_RF_frequency_step_unit = unit.MHz
        synthetizer_RF_frequency_step = 50

        synthetizer_RF_level_min = -10 #dBm
        synthetizer_RF_level_max = -10 #same value of min for fixed value
        synthetizer_RF_level_step = 0.5
        m_step_RF = 0

    p = unicode("_".join(["PartialResults", return_now_postfix()]))
    partial_file_path = os.path.join(result_file_name, p)
    if not os.path.exists(partial_file_path):
        try:
            os.makedirs(partial_file_path)
        except:
            print("Error creating " + partial_file_path)
            return 0
    frequency_LO_range = np.arange(synthetizer_LO_frequency_min, unit.unit_conversion( synthetizer_LO_frequency_max, synthetizer_LO_frequency_max_unit, synthetizer_LO_frequency_min_unit)  + unit.unit_conversion(synthetizer_LO_frequency_step, synthetizer_LO_frequency_step_unit, synthetizer_LO_frequency_min_unit) , unit.unit_conversion(synthetizer_LO_frequency_step, synthetizer_LO_frequency_step_unit, synthetizer_LO_frequency_min_unit))
    level_LO_range = np.arange(synthetizer_LO_level_min, synthetizer_LO_level_max + synthetizer_LO_level_step, synthetizer_LO_level_step)
    level_RF_range = np.arange(synthetizer_RF_level_min, synthetizer_RF_level_max + synthetizer_RF_level_step, synthetizer_RF_level_step)
    frequency_RF_range = np.arange(synthetizer_RF_frequency_min, unit.unit_conversion(synthetizer_RF_frequency_max, synthetizer_RF_frequency_max_unit, synthetizer_RF_frequency_min_unit) + unit.unit_conversion(synthetizer_RF_frequency_step, synthetizer_RF_frequency_step_unit, synthetizer_RF_frequency_min_unit) , unit.unit_conversion(synthetizer_RF_frequency_step, synthetizer_RF_frequency_step_unit, synthetizer_RF_frequency_min_unit))
    
    maxcount = float(len(frequency_LO_range) * len(level_LO_range) * len(level_RF_range) * len(frequency_RF_range))
    count = 0
    

    for f_LO in frequency_LO_range: #frequency loop
        #set SMB100A frequency for LO
        f_LO_value = str(f_LO)
        current_lo_frequency = f_LO_value + unit.return_unit_str(synthetizer_LO_frequency_min_unit)  
        command = "FREQ " + current_lo_frequency #Ex. FREQ 500kHz
        SMB_LO.write(command)
        
        for l_LO in level_LO_range: #power level loop
            #set SMB100A level for LO
            #calculate calibrated value of level for LO
            current_LO_level, calibration_LO_result =  calibrate(l_LO, f_LO,  synthetizer_LO_frequency_min_unit, calibration_LO, calibration_function = calibration_function_LO, calibration_function_unit = calibration_function_LO_unit)
            command = "POW " + str(current_LO_level)
            SMB_LO.write(command)
            #turn on LO
            SMB_LO.write("OUTP ON")
            
            for l_RF in level_RF_range: #power level loop
                
                for f_RF in frequency_RF_range: #frequency loop
                    values = []
                    #calculate calibrated value of level for RF
                    current_RF_level, calibration_RF_result =  calibrate(l_RF, f_RF, synthetizer_RF_frequency_min_unit, calibration_RF, calibration_function = calibration_function_RF, calibration_function_unit = calibration_function_RF_unit)
                    command = "POW " + str(current_RF_level)
                    SMB_RF.write(command) #set level for RF
                    #set SMB100A frequency for RF
                    f_RF_value = str(f_RF)
                    current_rf_frequency = f_RF_value + unit.return_unit_str(synthetizer_RF_frequency_min_unit)  
                    command = "FREQ " + current_rf_frequency #Ex. FREQ 500kHz
                    SMB_RF.write(command)
                    
                    #calculate spurius frequency
                    spurius_tmp = return_spurius_list(f_LO, synthetizer_LO_frequency_min_unit, f_RF, synthetizer_RF_frequency_min_unit, n_min_LO, n_max_LO, n_step_LO, m_min_RF, m_max_RF, m_step_RF, IF_low, IF_low_unit, IF_high, IF_high_unit)
                    #turn on RF
                    SMB_RF.write("OUTP ON")
                    spurius_markers = readFSV_marker_spurius(FSV, FSV_delay, spurius_tmp, spectrum_analyzer_IF_atten, spurius_IF_unit, calibration_IF, calibration_IF_function = calibration_function_IF, calibration_IF_function_unit = calibration_function_IF_unit)
                    count +=1
                    
                    
                    if not createprogressdialog is None:
                        import wx
                        wx.MicroSleep(500)
                        message = "LO {lo_freq} {lo_pow}dB - RF  {rf_freq} {rf_pow}dB".format(lo_freq = current_lo_frequency, lo_pow = str(current_LO_level), rf_freq = current_rf_frequency, rf_pow = str(current_RF_level))
                        newvalue = min([int(count/maxcount * 100), 100])
                        if newvalue == 100:
                            createprogressdialog = False
                            #dialog.Update(newvalue, message)
                            #wx.MicroSleep(500)
                            dialog.Close()
                        else:
                            dialog.Update(newvalue, message)
                    
                    
                    #load value for each spurius frequency
                    for s in spurius_markers:  
                        #value = [LO frequency, unit, LO level, CAL/NOCAL, RF frequency, unit, RF level, CAL/NOCAL, Spurius Frequency, Spurius level]
                        #values.append([f_LO_value, unit.return_unit_str(synthetizer_LO_frequency_unit), str(current_LO_level), calibration_LO_result, f_RF_value, unit.return_unit_str(synthetizer_RF_frequency_unit), str(current_RF_level), calibration_RF_result] + s)
                        values.append([f_LO_value, unit.return_unit_str(synthetizer_LO_frequency_min_unit), str(l_LO), calibration_LO_result, f_RF_value, unit.return_unit_str(synthetizer_RF_frequency_min_unit), str(l_RF), calibration_RF_result] + s)
                        totale_values.append(values[-1])
                        print(totale_values[-1])
                    #build filename - result_file_name_LOfrequency_unit_LOlevel_CAL/NOCAL_RFfrequency_unit_RFlevel_CAL/NOCAL_datetime
                    if len(spurius_markers) >0:
                        spurius_filename =  os.path.join(partial_file_path, "_".join(["R"] + values[0][0:-2]))
                        save_spurius(spurius_filename, values)
                    if f_LO == frequency_LO_range[-1] and l_LO == level_LO_range[-1] and l_RF == level_RF_range[-1] and f_RF == frequency_RF_range[-1]:
                        #safety turn Off
                        #dialog.Update(100, "Measure completed)
                        dialog.Destroy()
                        #SMB_LO.write("OUTP OFF")
                        #SMB_RF.write("OUTP OFF")
                    
                    
    #turn off LO and RF
    SMB_LO.write("OUTP OFF")
    SMB_RF.write("OUTP OFF")
    
    if m_step_RF == 0:
        harmonic_filename =result_file_name + "_TOTAL_HARMONIC_" + return_now_postfix()
        save_harmonic(harmonic_filename, totale_values)
        spurius_filename =result_file_name + "_TOTAL_" + return_now_postfix()
        save_spurius(spurius_filename, totale_values) 
    else:
        spurius_filename  =result_file_name + "_TOTAL_" + return_now_postfix()
        save_spurius(spurius_filename, totale_values)     

    return spurius_filename
    print("Misure completed\n")
    
    
#===============================================================================
#     #save settings on file
#     arguments = {
#         "synthetizer_LO_state" : synthetizer_LO_state,
#         "synthetizer_LO_frequency_min_unit" : synthetizer_LO_frequency_min_unit,
#         "synthetizer_LO_frequency_min" : synthetizer_LO_frequency_min,
#         "synthetizer_LO_frequency_min_unit" : synthetizer_LO_frequency_max_unit,
#         "synthetizer_LO_frequency_max" : synthetizer_LO_frequency_max,
#         "synthetizer_LO_frequency_min_unit" : synthetizer_LO_frequency_step_unit,
#         "synthetizer_LO_frequency_step" : synthetizer_LO_frequency_step,
#         "synthetizer_LO_level_min" : synthetizer_LO_level_min, #dBm
#         "synthetizer_LO_level_max" : synthetizer_LO_level_max,
#         "synthetizer_LO_level_step" : synthetizer_LO_level_step,
#         "synthetizer_RF_state" : synthetizer_RF_state,
#         "synthetizer_RF_frequency_unit" : synthetizer_RF_frequency_min_unit,
#         "synthetizer_RF_frequency_min" : synthetizer_RF_frequency_min,
#         "synthetizer_LO_frequency_min_unit" : synthetizer_RF_frequency_max_unit,
#         "synthetizer_RF_frequency_max" : synthetizer_RF_frequency_max,
#         "synthetizer_LO_frequency_min_unit" : synthetizer_RF_frequency_step_unit,
#         "synthetizer_RF_frequency_step" : synthetizer_RF_frequency_step,
#         "synthetizer_RF_level_min" : synthetizer_RF_level_min, #dBm
#         "synthetizer_RF_level_max" : synthetizer_RF_level_max,
#         "synthetizer_RF_level_step" : synthetizer_RF_level_step,
#         "power_meter_state" : power_meter_state,
#         "power_meter_misure_number" : power_meter_misure_number,
#         "power_meter_misure_delay" : power_meter_misure_delay, #seconds
#         "spectrum_analyzer_state" : spectrum_analyzer_state,
#         "spectrum_analyzer_sweep_points" : spectrum_analyzer_sweep_points,
#         "spectrum_analyzer_resolution_bandwidth" : spectrum_analyzer_sweep_points,
#         "spectrum_analyzer_resolution_bandwidth_unit" : spectrum_analyzer_resolution_bandwidth_unit,
#         "spectrum_analyzer_video_bandwidth" : spectrum_analyzer_video_bandwidth,
#         "spectrum_analyzer_video_bandwidth_unit" : spectrum_analyzer_video_bandwidth_unit,
#         "spectrum_analyzer_frequency_span" : spectrum_analyzer_frequency_span,
#         "spectrum_analyzer_frequency_span_unit" : spectrum_analyzer_frequency_span_unit,
#         "spectrum_analyzer_attenuation" : spectrum_analyzer_attenuation,
#         "gainAmplifier" : gainAmplifier, #dB
#         "spectrum_analyzer_IF_atten_enable" : spectrum_analyzer_IF_atten_enable,
#         "spectrum_analyzer_IF_atten" : spectrum_analyzer_IF_atten,
#         "spectrum_analyzer_IF_relative_level" : spectrum_analyzer_IF_relative_level_enable,
#         "spectrum_analyzer_IF_relative_level_enable" : spectrum_analyzer_IF_relative_level_enable,
#         "threshold_power" : threshold_power, #dB 
#         "spectrum_analyzer_frequency_marker_unit" : spectrum_analyzer_frequency_marker_unit,
#         "m_max_RF" : m_max_RF,
#         "n_max_LO" : n_max_LO,
#         "IF_high" : IF_high,
#         "IF_high_unit" : IF_high_unit,
#         "spurius_IF_unit" : spurius_IF_unit,
#         "calibration_file_LO" : calibration_file_LO,
#         "calibration_file_RF" : calibration_file_RF,
#         "calibration_file_IF" : calibration_file_IF}
# 
#     save_settings(result_file_name = result_file_name, arguments_values = arguments)        
#===============================================================================
    
#    if createprogressdialog:
#        dialog.Destroy()


#def readNRP2(NRP, NRP_delay, misure_number):
#    #Read powe meter value
#    #return list of misure_number values
#    result_value = []
#    for i in range(0, misure_number): #loop for number of measures
#        time.sleep(NRP_delay)
#        command = "MEAS:SCAL:POW:AVG?"
#        x = NRP.ask(command)[0] #read NRP2 value
#        result_value.append(x)
#    return result_value



def readFSV_marker_harmonic(FSV, FSV_delay, central_frequency_value, central_frequency_unit, harmonic, attenuation_in, gainAmplifier):

    result = []
    fsv_att_value = attenuation_in + gainAmplifier
    if fsv_att_value < 10:
        fsv_att_value = 10
    
    result.append(str(fsv_att_value))
    FSV.write("INP:ATT " + str(fsv_att_value)) #set attenuation
    
    for i in range(0, harmonic):

        freq = central_frequency_value * (i+1)
        result += readFSV_marker(FSV, FSV_delay, str(freq) + central_frequency_unit)

    return result

def readFSV_marker_spurius(FSV, FSV_delay, spurius_list, fsv_att_value, spurius_IF_unit, calibration_IF, calibration_IF_function, calibration_IF_function_unit):
    #measure all spurius level from FSV
    #return list [[Frequency, Unit, Level, n, m], [Frequency, Unit, Level, n, m], ..., [Frequency, Unit, Level, n, m]]
    result = []
    
    for s in spurius_list:
        freq = s[0]
        result += [readFSV_marker(FSV, FSV_delay, str(freq) + s[1], fsv_att_value, spurius_IF_unit, calibration_IF, calibration_IF_function, calibration_IF_function_unit) + [str(s[4]) , str(s[5])]]
    return result

def readFSV_marker(FSV, FSV_delay, central_frequency, fsv_att_value, spurius_IF_unit, calibration_IF, calibration_IF_function, calibration_IF_function_unit):
    #return the list [Frequency, Unit, Level]
    
    FSV.write("INP:ATT " + str(fsv_att_value)) #set attenuation
    
    #set central frequency
    command = "FREQ:CENT " + central_frequency
    FSV.write(command)
    #wait for center frequency
    time.sleep(FSV_delay)
    FSV.write("CALC:MARK:MAX")
    FSV.write("INIT:IMM; *WAI")
    #FSV.write("*OPT")
    #FSV.write("*WAI")
    
    #lettura = FSV.ask("CALC:MARK:X?")
    #time.sleep(FSV_delay)
    frequency = unit.unit_conversion(eval(FSV.ask("CALC:MARK:X?")), unit.Hz, spurius_IF_unit)
    result = [str(frequency)]    
    result += [unit.return_unit_str(spurius_IF_unit)]
    #response = FSV.ask("CALC:MARK:Y?")
    #time.sleep(FSV_delay)
    FSV.write("INIT:IMM; *WAI")
    tmp = eval(FSV.ask("CALC:MARK:Y?"))
    result += [str(x) for x in calibrate(tmp, frequency, spurius_IF_unit, calibration_IF, round_freq = True, calibration_function = calibration_IF_function, calibration_function_unit = calibration_IF_function_unit)]
    return result


#===============================================================================
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
#===============================================================================


if "SAB" not in globals():
    print("SAB not defined")
    SAB = SAB_class()  
    SAB_delay = 0
else:
    SAB_delay = 1

        

#create dummy class and objects for debugging
if "SMB_LO" not in globals():

    print("SMB_LO  not defined")
    SMB_LO = SMB_class()

if "SMB_RF" not in globals():

    print("SMB_RF not defined")
    SMB_RF = SMB_class()

if "SMF_RF" not in globals():

    print("SMF_RF not defined")
    SMF_RF = SMB_class()

if "SMF_LO" not in globals():

    print("SMF_LO not defined")
    SMF_LO = SMB_class()

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





if __name__ == "__main__":
    sys.exit(measure_LNA_spurius(SMB_LO = SMF_LO, SMB_RF = SMB_RF, NRP2 = NRP2, FSV = FSV))