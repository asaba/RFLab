'''
Created on 08/mag/2016

@author: sabah
'''

import time
from utility import unit_class, human_readable_frequency_unit
from scriptutility import calibrate

unit = unit_class()



def readPM5(PM5, misure_number, misure_delay):
    result_values = []
    for i in range(0, misure_number):
        time.sleep(misure_delay)
        command = "E1?"
        x = PM5.ask(command) #read NRP2 value
        result_values.append(x)
    return result_values

def readNRP2(SAB, NRP2, misure_number, misure_delay, calibration_frequency, calibration_frequency_unit, SAB_switch_delay, make_zero = False):
    result_values = []
    for i in range(0, misure_number):
        time.sleep(misure_delay)
        if make_zero:
            #make zero
            SAB.write("SWT1 0")
            time.sleep(SAB_switch_delay)
            command="SENS1:FREQ:FIX " +  str(calibration_frequency) + unit.return_unit_str(calibration_frequency_unit) #Ex. FREQ 500kHz
            NRP2.write(command)
            NRP2.write("CAL:ZERO:AUTO ONCE")
            NRP2.write("*WAI")
            NRP2.write("CAL:ZERO:AUTO?")
            #switch on cable
            SAB.write("SWT1 1")
            time.sleep(SAB_switch_delay) 
        command = "MEAS:SCAL:POW:AVG?"
        x = NRP2.ask(command)[0] #read NRP2 value
        result_values.append(x)
    return result_values

def readFSV_marker(FSV, 
                   FSV_delay, 
                   central_frequency, 
                   central_frequency_unit, 
                   spurius_IF_unit, 
                   calibration_IF, 
                   calibration_IF_function, 
                   calibration_IF_function_unit):

    #set central frequency
    command = "FREQ:CENT " + str(central_frequency) + central_frequency_unit
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

def FSV_reset_setup(FSV, spectrum_analyzer_sweep_points, 
                    spectrum_analyzer_resolution_bandwidth, 
                    spectrum_analyzer_resolution_bandwidth_unit, 
                    spectrum_analyzer_video_bandwidth, 
                    spectrum_analyzer_video_bandwidth_unit, 
                    spectrum_analyzer_frequency_span, 
                    spectrum_analyzer_frequency_span_unit, 
                    spectrum_analyzer_IF_atten_enable, 
                    spectrum_analyzer_IF_atten, 
                    spectrum_analyzer_IF_relative_level_enable, 
                    spectrum_analyzer_IF_relative_level):
    
    
    
    #reset instrument
    FSV.write("*rst")

    #Setup spectrum analyzer
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
    

def readFSV_sweep(FSV, 
                  FSV_delay, 
                  central_frequency, 
                  central_frequency_unit):
    
    test_sweep = True
    #return the list [Frequency, Unit, Level]
    
    #set central frequency
    command = "FREQ:CENT " + str(central_frequency) + unit.return_unit_str(central_frequency_unit)
    FSV.write(command)
    #wait for center frequency
    time.sleep(FSV_delay)
    
    FSV.write("INIT:IMM; *WAI")
    if test_sweep:
        tmp = FSV.ask("SWE:POIN?")
        points_number = eval(tmp)
        points = range(0, points_number)
    else:
        points = FSV.ask("TRACe:DATA:X? TRACE1")
        points = [unit.convertion_from_base(eval(x), human_readable_frequency_unit) for x in points.split(",")]
    b = FSV.ask("TRACe:DATA? TRACE1") #FSV2.ask("TRACe:IQ:DATA?")
    y = [eval(x) for x in b.split(",")]
    
    return points, y