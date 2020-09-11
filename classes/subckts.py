#!/usr/bin/env python

class subckts:

    def __init__(self, uut, fet_size, fet_nfin, fet_voltage):
        self.uut = uut # name of unit under test, e.g. inverter
        self.fet_size = fet_size # fet length size, e.g. 14nm, 10nm, 7nm
        self.fet_nfin = fet_nfin # fin size?? e.g. 1000m
        self.fet_voltage = fet_voltage # nominal voltage for ptm model


    '''Inputs and Outputs LOADS'''

    def write_source(self, uut_size):
        '''Write input source of system to .sp file'''
            # inputs uut_size, load ammount, sim_time
        for instance in range(uut_size):
            fall_time = (2) * (2 ** instance)
            rise_time = str(fall_time / 2)
            fall_time = str(fall_time)
            instance = str(instance)
            self.uut.write("vin_" + instance + " inb_" + instance + " gnd  PULSE(" + self.fet_voltage + "V " + "0V 0ns 50ps 50ps " + rise_time + "n " + fall_time + "n)\n")
            # call instance of input source subckt in uut file
            self.uut.write("xinput_" + instance + " inb_" + instance + " outin_0" + instance + " vdd " + "inverter\n")
        self.uut.write("\n")
        return None

    def write_outputs(self, uut_size, tag, outin):
        '''Write output load of system to .sp file'''
        for instance in range(uut_size):
            inout = str(outin + 1)
            for output_tag in range(tag):
                instance = str(instance) # instance of ouput to evaluate
                output_tag = str(output_tag) # amount of load per output
                # call instance of ouput load subckt in uut file
                self.uut.write("xoutput_" + instance + output_tag + " outin_" + inout  + instance + " outb_" + instance + output_tag + " vdd " + "inverter\n")
        self.uut.write("\n")
        return None


    '''UUTs'''
    def set_inverter(self):
        '''Write inverter subckt'''
        # declare subckt name, input, output, and source
        self.uut.write(".subckt inverter in out vdd\n")
        self.uut.write("$FETs" + "\n")
        # call pfet model name, and decaler its input, output, and source
        self.uut.write("xpfet out in vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        # call nfet model name, and decaler its input, output, and source
        self.uut.write("xnfet out in gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n") # end subckt declaration
        self.uut.write("\n")
        return None

    def write_inverter(self, uut_size, serial_instance):
        '''Write inverter device'''
        for instance in range(uut_size):
            for outin in range(serial_instance):
                instance = str(instance)
                inout = str(outin + 1)
                outin = str(outin)
                # declare subckt name, input, output, and source
                self.uut.write("xinverter" + outin + instance + " " + "outin_" + outin  + instance + " " + "outin_" + inout + instance + " vdd " + "inverter\n")
        self.uut.write("\n")
        return None


    '''Measurements'''

    def measure_delays(self, uut_size, serial_instance):
        vdd_50 = str(float(self.fet_voltage) / 2)
        for instance in range(uut_size):
            rise_fall_count = 2 ** ((uut_size - instance) - 1)
            for outin in range(serial_instance):
                inout = str(outin + 1)
                outin = str(outin)
                for rise_fall in range(rise_fall_count ):
                    rise_fall = str(rise_fall + 1)
                    instance = str(instance)
                    # use instance to derive a method that will calculate all delays and an average
                    self.uut.write(".measure tran trf_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=" + vdd_50 + " rise=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=" + vdd_50 + " fall=" + rise_fall + "\n")
                    # automate to print per uut subckt
                    self.uut.write(".measure tran tfr_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=" + vdd_50 + " fall=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=" + vdd_50 + " rise=" + rise_fall + "\n")
        return None

    def measure_power(self, uut_size, sim_time, serial_instance):
        for instance in range(uut_size):
            for outin in range(serial_instance):
                instance = str(instance)
                outin = str(outin)
                # automate to print per uut subckt, create subckt uut to calculate power of entire uut
                self.uut.write(".measure tran inv_avg_power" + outin + instance  + " avg p(x" + "inverter" + outin + instance + ") from=0ns to=" + sim_time + "ns\n")
                # automate to print per uut subckt
                self.uut.write(".measure tran peakpower" + outin + instance  + " max p(x" + "inverter" + outin + instance + ")\n")
                return None

    def print_wave(self, uut_size, serial_instance):
        for instance in range(uut_size):
            for outin in range(serial_instance):
                instance = str(instance)
                inout = str(outin + 1)
                outin = str(outin)
                # automate to print per uut subckt, need to use instance and tags
                self.uut.write(".print TRAN V(" + "outin_" + outin + instance + ") V(" + "outin_" + inout + instance + ")\n")
        return None

#   def write_dram(self, instance):

