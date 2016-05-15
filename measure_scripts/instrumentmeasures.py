'''
Created on 08/mag/2016

@author: sabah
'''

import time
from utility import unit_class

unit = unit_class()


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
            NRP2.ask("CAL:ZERO:AUTO?")
            #switch on cable
            SAB.write("SWT1 1")
            time.sleep(SAB_switch_delay) 
        command = "MEAS:SCAL:POW:AVG?"
        x = NRP2.ask(command)[0] #read NRP2 value
        result_values.append(x)
    return result_values