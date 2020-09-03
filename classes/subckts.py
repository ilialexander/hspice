#!/usr/bin/env python

class Subckts:

    def __init__(self, uut, fet_size, fet_nfin):
        self.uut = uut
        self.fet_size = fet_size
        self.fet_nfin = fet_nfin

    '''Inputs and Outputs LOADS'''

    def write_input(self, instance):
        self.uut.write(".subckt input_" + instance + " inb_" + instance + " in_" + instance + " vdd\n")
        self.uut.write("xpfetin_" + instance + " in_" + instance + " inb_" + instance + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write("xnfetin_" + instance + " in_" + instance + " inb_" + instance + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n\n")
        self.uut.write("xinput_" + instance + " inb_" + instance + " in_" + instance + " vdd " + "input_" + instance + "\n")
        return None

    def write_output(self, instance):
        self.uut.write("$Output Load\n")
        self.uut.write(".subckt output_" + instance + " out_" + instance + " outb_" + instance + " vdd\n")
        self.uut.write("xpfetout_" + instance + " outb_" + instance + " out_" + instance + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write("xnfetout_" + instance + " outb_" + instance + " out_" + instance + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n\n")
        self.uut.write("xoutput_" + instance + " out_" + instance + " outb_" + instance + " vdd " + "output_" + instance + "\n")
        return None

#    def inductor(self):

    '''UUTs'''

    def write_inverter(self, instance):
        self.uut.write(".subckt inverter" + "0" + " in_" + "0" + " out_" + "0" + " vdd\n")
        self.uut.write("$FETs" + "\n")
        self.uut.write("xpfet_" + "0" + " out_" + "0" + " in_" + "0" + " vdd vdd pfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write("xnfet_" + "0" + " out_" + "0" + " in_" + "0" + " gnd gnd nfet l=" + self.fet_size + "n nfin=" + self.fet_nfin + "\n")
        self.uut.write(".ends\n\n")
        self.uut.write("xinverter" + "0" + " in_" + "0" + " out_" + "0" + " vdd " + "inverter" + "0" + "\n")
        return None
