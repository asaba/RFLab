'''
Created on 03/dic/2015

@author: Andrea
'''

from numpy import array
from random import uniform
from utility import create_csv
import datetime
import tscpy

#create dummy class and objects for debugging
   
class SAB_class():

    def write(self, command):
        pass

    def ask(self, command):
        return ["1.1"]


#create dummy class and objects for debugging
class PM5_class():

    def write(self, command):
        pass

    def ask(self, command):
        return str(uniform(1.2, 5.5))

#create dummy class and objects for debugging
class SMB_class():

    def write(self, command):
        pass

    def ask(self, command):
        return [str(uniform(1.2, 5.5))]
    
class NRP2_class():

    def write(self, command):
        pass

    def ask(self, command):
        return [str(uniform(23, 44))]


class FSV_class():

    def write(self, command):
        pass

    def ask(self, command):
        if command == "CALC:MARK:X?":
            return str(int(round(uniform(1000000, 5000000)))) #unit HZ
        elif command == "CALC:MARK:Y?":
            return str(uniform(-12, 10))

class TSC_class(tscpy.instruments.TSC5120A):

    def close(self):
        pass
    def __init__(self):
        pass
    
    #def _parse_spectrum(self, spectrum_str): 
    #    frequency = []
    #    density = []
    #    spectrum_str_rows = spectrum_str.split("\n")
    #    for row in spectrum_str_rows[3:]: #skip first three rows
    #        if len(row)>0:
    #            freq, dens = row.split("\t")
    #            frequency.append(freq.trim())
    #            density.append(dens.trim())
    #    frequency_header, density_header = spectrum_str_rows[1].split("\t")
    #    frequency_unit_str = frequency_header.split("(")[1].split(")")[0]
    #    density_unit_str = density_header.split("(")[1].split(")")[0]
        
    
    # user-interface, get different things
    def get_adev(self):
        return [{'NEQBW': 500.0, 'TAU0': 0.001, 'adev': {'tau': array([  1.00000000e-03,   2.00000000e-03,   4.00000000e-03,
         1.00000000e-02,   2.00000000e-02,   4.00000000e-02,
         1.00000000e-01,   2.00000000e-01,   4.00000000e-01,
         1.00000000e+00,   2.00000000e+00,   4.00000000e+00,
         1.00000000e+01,   2.00000000e+01,   4.00000000e+01,
         1.00000000e+02,   2.00000000e+02]), 'adev': array([  6.15200000e-09,   4.15200000e-09,   3.10700000e-09,
         1.91700000e-09,   1.23800000e-09,   8.05000000e-10,
         5.61000000e-10,   5.77000000e-10,   7.31000000e-10,
         9.20000000e-10,   7.13000000e-10,   2.78000000e-10,
         1.11000000e-10,   7.20000000e-11,   2.90000000e-11,
         1.22000000e-11,   1.10000000e-11]), 'err': array([ -7.68000000e-12,  -7.33000000e-12,  -7.75000000e-12,
        -7.56000000e-12,  -6.91000000e-12,  -6.36000000e-12,
        -7.00000000e-12,  -1.02000000e-11,  -1.82000000e-11,
        -3.63000000e-11,  -3.97000000e-11,  -2.19000000e-11,
        -1.38000000e-11,  -1.26000000e-11,  -7.20000000e-12,
        -4.58000000e-12,  -5.48000000e-12])}}, {'NEQBW': 50.0, 'TAU0': 0.01, 'adev': {'tau': array([  1.00000000e-02,   2.00000000e-02,   4.00000000e-02,
         1.00000000e-01,   2.00000000e-01,   4.00000000e-01,
         1.00000000e+00,   2.00000000e+00,   4.00000000e+00,
         1.00000000e+01,   2.00000000e+01,   4.00000000e+01,
         1.00000000e+02,   2.00000000e+02]), 'adev': array([  1.51000000e-09,   1.12100000e-09,   7.58000000e-10,
         5.52000000e-10,   5.75000000e-10,   7.31000000e-10,
         9.20000000e-10,   7.13000000e-10,   2.92000000e-10,
         1.11000000e-10,   7.40000000e-11,   2.90000000e-11,
         1.40000000e-11,   1.10000000e-11]), 'err': array([ -5.96000000e-12,  -6.26000000e-12,  -5.99000000e-12,
        -6.89000000e-12,  -1.02000000e-11,  -1.83000000e-11,
        -3.63000000e-11,  -3.97000000e-11,  -2.30000000e-11,
        -1.38000000e-11,  -1.29000000e-11,  -7.20000000e-12,
        -5.27000000e-12,  -5.60000000e-12])}}, {'NEQBW': 5.0, 'TAU0': 0.1, 'adev': {'tau': array([  1.00000000e-01,   2.00000000e-01,   4.00000000e-01,
         1.00000000e+00,   2.00000000e+00,   4.00000000e+00,
         1.00000000e+01,   2.00000000e+01,   4.00000000e+01,
         1.00000000e+02,   2.00000000e+02]), 'adev': array([  4.73000000e-10,   5.61000000e-10,   7.28000000e-10,
         9.19000000e-10,   7.12000000e-10,   2.66000000e-10,
         1.16000000e-10,   5.60000000e-11,   3.20000000e-11,
         2.10000000e-11,   1.10000000e-11]), 'err': array([ -5.93000000e-12,  -9.94000000e-12,  -1.82000000e-11,
        -3.64000000e-11,  -3.99000000e-11,  -2.11000000e-11,
        -1.45000000e-11,  -9.78000000e-12,  -7.82000000e-12,
        -7.92000000e-12,  -5.41000000e-12])}}, {'NEQBW': 0.5, 'TAU0': 1.0, 'adev': {'tau': array([   1.,    2.,    4.,   10.,   20.,   40.,  100.,  200.]), 'adev': array([  8.75000000e-10,   7.52000000e-10,   2.61000000e-10,
         1.08000000e-10,   6.10000000e-11,   2.90000000e-11,
         2.00000000e-11,   5.60000000e-12]), 'err': array([ -3.54000000e-11,  -4.30000000e-11,  -2.11000000e-11,
        -1.39000000e-11,  -1.11000000e-11,  -7.30000000e-12,
        -8.04000000e-12,  -3.18000000e-12])}}]
    
    def get_fcounter(self):
        return ""
    
    def get_spectrum(self):
        return {"Frequency" : {"value" : array(["1.", "2.", "3.", "4.", "5.", "6."]), "unit_str": "Hz"},
            "Density" : {"value" : array(["-4.", "-6.", "-3.", "-7.", "-3.", "-1."]), "unit_str": "dBc/Hz"},}
    
    #def save_on_csv(self, filepath):
    #    adev = self.get_adev()
    #    fcounter = self.get_fcounter()
    #    spectrum = self.get_spectrum()
    #    
    #    now_postfix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #    
    #    rows = []
    #    for a in adev:
    #        header_01 = ["NEQBW " + str(a['NEQBW']), " TAU " + str(a['TAU0'])]
    #        header_02 = ["tau", "adev", "err"]
    #        rows.append(header_01)
    #        rows.append(header_02)
    #        for i in range(0, len(a["adev"]["tau"])-1):
    #            rows.append([str(a["adev"]["tau"][i]), str(a["adev"]["adev"][i]), str(a["adev"]["err"][i])])
    #    adev_file = open("adev_" + now_postfix + ".csv", "wb")
    #    create_csv(adev_file, ["ADEV"], [], rows)
    #    
    #    rows = []
    #    rows.append(["Frequency", "Density"])
    #    rows.append([spectrum["Frequency"]["unit_str"], spectrum["Density"]["unit_str"]])
    #    for i in range(0, len(spectrum["Frequency"]["value"])-1):
    #        rows.append([spectrum["Frequency"]["value"][i], spectrum["Density"]["value"][i]])
    #    
    #    spectrum_file = open("spectrum_" + now_postfix + ".csv", "wb")
    #    create_csv(spectrum_file, [], [], rows)
