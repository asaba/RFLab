'''
Created on 03/dic/2015

@author: Andrea
'''

from random import uniform

#create dummy class and objects for debugging
   
class SAB_class():

    def write(self, command):
        pass

    def ask(self, command):
        return ["1.1"]

        

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
            return [str(uniform(1000000, 5000000))] #unit HZ
        elif command == "CALC:MARK:Y?":
            return [str(uniform(-12, 10))]

