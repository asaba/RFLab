'''
Created on 23/mag/2016

@author: sabah
'''


frequency_LO_index = 0
unit_LO_index = 1
power_LO_index = 2
is_LO_calibrated_index = 3
frequency_RF_index = 4
unit_RF_index = 5
power_RF_index = 6
is_RF_calibrated_index = 7
frequency_IF_index = 8
unit_IF_index = 9
power_IF_index = 10
is_IF_calibrated_index = 11
n_LO_index = 12
m_RF_index = 13
conversion_loss = 14

csv_file_header = ["Freq_LO", 
                   "unit_LO", 
                   "power_LO (dBm)", 
                   "calib_LO", 
                   "Freq_RF", 
                   "unit_RF", 
                   "power_RF (dBm)", 
                   "calib_RF", 
                   "Freq_IF", 
                   "unit_IF", 
                   "power_IF (dBm)", 
                   "calib_IF", 
                   "n_LO", 
                   "m_RF", 
                   "conversion_loss (dBm)"]