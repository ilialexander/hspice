#!/usr/bin/env python

class subckts:

    def __init__(self, uut, fet_size, fet_nfin, fet_voltage):
        self.uut = uut # name of unit under test, e.g. inverter
        self.fet_size = fet_size # fet length size, e.g. 14nm, 10nm, 7nm
        self.fet_nfin = fet_nfin # fin size?? e.g. 1000m
        self.fet_voltage = fet_voltage # nominal voltage for ptm model

    '''Inputs and Outputs LOADS'''

    def write_source(self, instance, fall_time):
        '''Write input source of system to .sp file'''
        rise_time = str(fall_time / 2)
        fall_time = str(fall_time)
        instance = str(instance)
        self.uut.write("vin_" + instance + " inb_" + instance + " gnd  PULSE(" + self.fet_voltage + "V " + "0V 0ns 50ps 50ps " + rise_time + "n " + fall_time + "n)\n\n")
        # declare subckt name, input, output, and source
        self.uut.write(".subckt input_" + instance + " inb_" + instance + " in_" + instance + " vdd\n")
        # call pfet model name, and decaler its input, output, and source
        self.uut.write("xpfetin_" + instance + " in_" + instance + " inb_" + instance + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        # call nfet model name, and decaler its input, output, and source
        self.uut.write("xnfetin_" + instance + " in_" + instance + " inb_" + instance + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n") # end subckt declaration
        # call instance of input source subckt in uut file
        self.uut.write("xinput_" + instance + " inb_" + instance + " in_" + instance + " vdd " + "input_" + instance + "\n\n")
        return None

    def write_outputs(self, instance, tag):
        '''Write output load of system to .sp file'''
        for output_tag in range(tag):
            instance = str(instance) # instance of ouput to evaluate
            output_tag = str(output_tag) # amount of load per output
            self.uut.write("$Output Load\n")
            # declare subckt name, input, output, and source
            self.uut.write(".subckt output_" + instance + output_tag + " out_" + instance + " outb_" + instance + output_tag + " vdd\n")
            # call pfet model name, and decaler its input, output, and source
            self.uut.write("xpfetout_" + instance + " outb_" + instance + output_tag + " out_" + instance + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
            # call nfet model name, and decaler its input, output, and source
            self.uut.write("xnfetout_" + instance + " outb_" + instance + output_tag + " out_" + instance + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
            self.uut.write(".ends\n") # end subckt declaration
            # call instance of ouput load subckt in uut file
            self.uut.write("xoutput_" + instance + output_tag + " out_" + instance + " outb_" + instance + output_tag + " vdd " + "output_" + instance + output_tag + "\n\n")
        return None


    '''UUTs'''

    def write_inverter(self, instance):
        '''Write inverter device'''
        instance = str(instance)
        # declare subckt name, input, output, and source
        self.uut.write(".subckt inverter" + instance + " in_" + instance + " out_" + instance + " vdd\n")
        self.uut.write("$FETs" + "\n")
        # call pfet model name, and decaler its input, output, and source
        self.uut.write("xpfet_" + instance + " out_" + instance + " in_" + instance + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        # call nfet model name, and decaler its input, output, and source
        self.uut.write("xnfet_" + instance + " out_" + instance + " in_" + instance + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n") # end subckt declaration
        # call instance of inverter subckt in uut file
        self.uut.write("xinverter" + instance + " in_" + instance + " out_" + instance + " vdd " + "inverter" + instance + "\n\n")
        return None

#   def write_dram(self, instance):

