# encoding: utf-8
'''
Created on 02/ott/2015

@author: Andrea

Modificato il 05/05/2016:   Passaggio dall'utlizzo della SAB da modalità seriale a motalità di rete. 
                            Aggiunta della calibrazione dell'NRP2 prima di ogni misura tramite SWITCH della SAB 
'''

import time
import sys
import numpy as np
# import stepattenuatorserial
import csv
from utility import save_data, save_settings, create_csv, unit_class, human_readable_frequency_unit, \
    Generic_Range
from scriptutility import readcalibrationfile, calibrate, calibrationfilefunction, Frequency_Range
from instrumentmeasures import readNRP2

unit = unit_class()

if "SMB_RF" not in globals():
    # print("SMB_RF not defined")
    class SMB_class():
        def write(self, command):
            pass

        def ask(self, command):
            return [1.1]


    SMB_RF = SMB_class()
if "NRP2" not in globals():
    # print("NRP2 not defined")
    class NRP2_class():
        def write(self, command):
            pass

        def ask(self, command):
            return [1.1]


    NRP2 = NRP2_class()

if "SAB" not in globals():

    # print("SAB not defined")

    class SAB_class():

        def write(self, command):
            pass

        def ask(self, command):
            return ["1.1"]


    SAB = SAB_class()
    SAB_delay = 0
else:
    SAB_delay = 1

synthetizer_state = "ON"
# synthetizer_frequency_min = 5000
# synthetizer_frequency_max = 6000
# synthetizer_frequency_step = 100
# synthetizer_frequency_unit = unit.MHz
synthetizer_frequency = Frequency_Range(5000, 6000, 100, unit.MHz)
synthetizer_frequency.to_base()
synthetizer_fix_power = 0  # dBm
synthetizer_level = Generic_Range(0, 10, 1)
# synthetizer_level_max = 10 #dBm
# synthetizer_level_step = 1 #dBm
power_meter_make_zero = True
power_meter_make_zero_delay = 1  # seconds
power_meter_misure_number = 1
power_meter_misure_delay = 1  # seconds
SAB_state = "ON"
SAB_attenuation_level = Generic_Range(0, 5, 1)
# SAB_attenuation_level_max = 5
# SAB_attenuation_level_step = 1
SAB_attenuation_delay = 1
SAB_switch_01_delay = 1  # seconds
SAB_switch_02_delay = 1  # seconds
calibration_cable_file_name = "C:\\Users\\Labele\\Desktop\\IP1\\misure calibrate\\CableLO_20160505122636.csv"
result_file_name = "C:\\Users\\Labele\\Desktop\\IP1\\misure calibrate\\result"


def measure_IP1(SMB_RF=SMB_RF,
                NRP2=NRP2,
                SAB=SAB,
                synthetizer_state=synthetizer_state,
                synthetizer_frequency=synthetizer_frequency,
                synthetizer_fix_power=synthetizer_fix_power,  # dBm
                synthetizer_level=synthetizer_level,  # dBm
                power_meter_make_zero=power_meter_make_zero,
                power_meter_make_zero_delay=power_meter_make_zero_delay,
                power_meter_misure_number=power_meter_misure_number,
                power_meter_misure_delay=power_meter_misure_delay,  # seconds
                SAB_state=SAB_state,
                SAB_attenuation_level=SAB_attenuation_level,
                SAB_attenuation_delay=SAB_attenuation_delay,
                SAB_switch_01_delay=SAB_switch_01_delay,
                SAB_switch_02_delay=SAB_switch_02_delay,
                calibration_cable_file_name=calibration_cable_file_name,
                result_file_name=result_file_name,
                createprogressdialog=None
                ):
    dialog = createprogressdialog

    values = []

    # open calibration file
    calibration_LO = readcalibrationfile(calibration_cable_file_name)
    calibration_function_LO, calibration_function_LO_unit = calibrationfilefunction(calibration_LO)

    # reset the synthetizer SMB100A
    SMB_RF.write("*rst")

    # imposta la modalita'� di funzionamento del SMB100A

    SMB_RF.write("FREQ:MODE FIX")
    SMB_RF.write("POW:MODE FIX")

    if str(SAB_state) == "OFF":
        SAB_attenuation_level_min = 0
        SAB_attenuation_level_max = 0
        SAB_attenuation_level_step = 1

    # synthetizer_frequency_min = unit.convertion_to_base(synthetizer_frequency_min, synthetizer_frequency_unit)

    frequency_LO_range = synthetizer_frequency.return_range()
    level_LO_range = synthetizer_level.return_arange()
    attenuation_range = SAB_attenuation_level.return_arange()
    maxcount = len(frequency_LO_range) * len(level_LO_range)

    for s in attenuation_range:
        count = 0
        if SAB_state == True:
            # set stepattenuator value
            SAB.write("ATT " + str(s))
            # print("Attenuation {att} dB".format(att = str(s)))
            time.sleep(SAB_attenuation_delay)
            s_value = str(s)
        else:
            s_value = "OFF"

        for f in frequency_LO_range:
            # set SMB100A frequency
            if synthetizer_state == True:
                f_value = str(f)
                current_frequency = f_value + unit.return_unit_str(unit.Hz)
                current_frequency_human_readable = unit.return_human_readable_str(f)
                command = "FREQ " + current_frequency  # Ex. FREQ 500kHz
                SMB_RF.write(command)
                for l in level_LO_range:

                    current_LO_level, calibration_LO_result = calibrate(l, f, unit.Hz, calibration_LO,
                                                                        calibration_function=calibration_function_LO,
                                                                        calibration_function_unit=calibration_function_LO_unit)
                    # set SMB100A level
                    # current_level =  str(l)
                    current_level = str(current_LO_level)
                    command = "POW " + current_level
                    SMB_RF.write(command)
                    # turn on RF
                    if f == frequency_LO_range[0]:
                        SMB_RF.write("OUTP ON")
                    values.append([f_value, str(l), current_level, calibration_LO_result, s_value] + readNRP2(SAB, NRP2,
                                                                                                              power_meter_misure_number,
                                                                                                              power_meter_misure_delay,
                                                                                                              f,
                                                                                                              unit.Hz,
                                                                                                              SAB_switch_01_delay,
                                                                                                              make_zero=True))
                    count += 1

                    if not createprogressdialog is None:
                        import wx
                        wx.MicroSleep(500)
                        message = "RF {lo_freq} {lo_pow}dB".format(lo_freq=current_frequency_human_readable,
                                                                   lo_pow=current_level)
                        newvalue = min([int(count / maxcount * 100), 100])
                        if newvalue == 100:
                            createprogressdialog = False
                            # dialog.Update(newvalue, message)
                            # wx.MicroSleep(500)
                            dialog.Close()
                        else:
                            dialog.Update(newvalue, message)

                        if f == frequency_LO_range[-1] and l == level_LO_range[-1] and s == attenuation_range[-1]:
                            # safety turn Off
                            # dialog.Update(100, "Measure completed)
                            dialog.Destroy()
            else:
                l = 0
                f_value = "OFF"
                current_level = "OFF"
                calibration_LO_result = "OFF"
                values.append([f_value, str(l), current_level, calibration_LO_result, s_value] + readNRP2(SAB, NRP2,
                                                                                                          power_meter_misure_number,
                                                                                                          power_meter_misure_delay,
                                                                                                          f, unit.Hz,
                                                                                                          SAB_switch_01_delay,
                                                                                                          make_zero=True))

    # if stepattenuator_state == "ON":
    #    #create step attenuator object
    #    STA.closeport()
    # turn off RF
    SMB_RF.write("OUTP OFF")

    print("Misure completed\n")

    save_data("txt", result_file_name, values, power_meter_misure_number, unit.return_unit_str(unit.Hz))
    save_data("csv", result_file_name, values, power_meter_misure_number, unit.return_unit_str(unit.Hz))

    return result_file_name


if __name__ == "__main__":
    sys.exit(measure_IP1(SMB_RF=SMB_RF, NRP2=NRP2, SAB=SAB))
