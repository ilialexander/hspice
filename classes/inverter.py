#!/usr/bin/env python
import os

class inverter:

    def __init__(self, script_params, grid_params, fet_params, sim_params):
        (script_dir, script_name, uut) = script_params 
        self.script_dir = script_dir # script working directory
        self.uut = uut # unit under test
        self.script_name = script_name # name of running script

        (spice_file, parallel_instances, serial_instances, load_amount, fan_out_chain) = grid_params
        self.spice_file = spice_file # name of unit under test, e.g. inverter
        self.par_instances = parallel_instances # grid columns
        self.ser_instances = serial_instances # grid rows
        self.load_amount = load_amount # load for realistic results
        self.fan_out_chain = fan_out_chain # load for fan out driven

        (subuut, fet_nfin) = fet_params
        self.subuut = subuut # ptm under test
        self.fet_nfin = fet_nfin # fin size?? e.g. 1000m

        (sim_type, sim_tinc, sim_time) = sim_params
        self.sim_type = sim_type # simulation type, e.g., tran, dc
        self.sim_tinc = sim_tinc # simulation time step
        self.sim_time = sim_time # total simulation time

        self.script_path = self.script_dir + "/" + self.script_name # full path to working script



    '''Inputs and Outputs LOADS'''

    def write_source(self):
        '''Write input source of system to .sp file'''
        # input sources are porportional to the amount of instances
        self.spice_file.write("$all input sources\n")
        for instance in range(self.par_instances):
            fall_time = (2) * (2 ** instance) / 2 # time from highest value to lowest, it provides a virtual binary count
            rise_time = str(fall_time / 2)    # time from lowest value to lowest
            fall_time = str(fall_time)
            instance = str(instance)
            # sets input wave
            self.spice_file.write("vin_" + instance + " inb_" + instance + " gnd  PULSE(vdd " + "0V 0ns " + self.sim_tinc + " " + self.sim_tinc + " " + rise_time + "n " + fall_time + "n)\n")

        # sets a more realistic input through inverter load
        self.spice_file.write("$invert input sources\n")
        for instance in range(self.par_instances):
            instance = str(instance)
            # sets wave inverted
            self.spice_file.write("xinput_" + instance + " inb_" + instance + " outin_0" + instance + " vdd " + "inverter\n")
        self.spice_file.write("\n")
        return None


    def write_outputs(self):
        '''Write realistic output load of system to .sp file'''
        for instance in range(self.par_instances):
            inout = str(self.ser_instances) # connects model_uut output to realistic loads
            for output_tag in range(self.load_amount):
                instance = str(instance) # instance of ouput to evaluate
                output_tag = str(output_tag) # amount of load per output
                # call instance of ouput load subckt for model_uut
                self.spice_file.write("xoutput_" + instance + output_tag + " outin_" + inout  + instance + " outb_" + instance + output_tag + " vdd " + "inverter\n")
                # creates FO4 chain of inverters
                self.write_fan_out_4(self.load_amount, int(self.fan_out_chain/4), instance + output_tag)
        self.spice_file.write("\n")
        return None


    def write_fan_out_4(self, output_tag, fan_out, outer_tag):
        '''Writes an FO4 Chain, outer layer must be divisible by 4'''
        if fan_out == 1:
            return None
        else:
            for value in range(output_tag):
                # call instance of fo4 load
                self.spice_file.write("xoutput_" + outer_tag + str(value) + " outb_" + outer_tag + " outb_" + outer_tag + str(value) + " vdd " + "inverter\n")
                # creates each layer of fo4, e.g., 16, 64, 256
                self.write_fan_out_4(output_tag, int(fan_out/4), outer_tag + str(value))



    '''UUTs'''
    def set_cells_subckts(self):
        '''Write inverter subckt'''
        # declare subckt name, input, output, and source
        self.spice_file.write(".subckt inverter in out vdd\n")
        self.spice_file.write("$fets" + "\n")
        # call pfet model name, and decaler its input, output, and source
        self.spice_file.write("xpfet out in vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
        # call nfet model name, and decaler its input, output, and source
        self.spice_file.write("xnfet out in gnd gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write(".ends\n") # end subckt declaration
        self.spice_file.write("\n")
        return None

    def write_uut(self):
        '''Write inverter device'''
        # declare model_uut_grid subckt
        self.spice_file.write(".subckt model_uut_grid vdd\n")
        self.spice_file.write("+")
        for instance in range(self.par_instances):
            instance = str(instance)
            # declare subckt inputs
            self.spice_file.write("outin_0" + instance + " ")
        self.spice_file.write("$inputs to model_uut_grid Subckt\n")

        self.spice_file.write("+")
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                inout = str(outin + 1)
                # declare subckt outputs
                self.spice_file.write("outin_" + inout + instance + " ")
        self.spice_file.write("$outputs to model_uut_grid Subckt\n")
                
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                inout = str(outin + 1)
                outin = str(outin)
                # invoke inverters
                self.spice_file.write("xinverter" + outin + instance + " " + "outin_" + outin  + instance + " " + "outin_" + inout + instance + " vdd " + "inverter\n")
        self.spice_file.write(".ends\n")

        # invoke model_uut_grid
        self.spice_file.write("$invoke UUT grid\n")
        self.spice_file.write("xmodel_uut_grid vdd\n")
        self.spice_file.write("+")
        for instance in range(self.par_instances):
            instance = str(instance)
            # declare inputs
            self.spice_file.write("outin_0" + instance + " ")
        self.spice_file.write("$inputs to model_uut_grid\n")

        self.spice_file.write("+")
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                inout = str(outin + 1)
                # declare outputs
                self.spice_file.write("outin_" + inout + instance + " ")
        self.spice_file.write("$outputs to model_uut_grid\n")
        self.spice_file.write("+model_uut_grid\n\n")
        return None



    '''Analysis and Measurements'''

    def set_library(self):
        '''Sets the library to read the ptm model'''
        # name of unit under test in spice file
        self.spice_file.write("$ Netlist of " + self.uut + "\n")
        # script location disclaimer
        self.spice_file.write("$ This UUT was automatically generated by:\n")
        self.spice_file.write("$ " + self.script_path + "\n")
        # invoke library for ptm model to test
        self.spice_file.write(".lib '../models' " + self.subuut + "\n")
        # gets 50% of vdd of delay calculation
        self.spice_file.write(".param vdd_50='vdd/2'"  "\n")
        return None


    def analysis_type(self):
        '''Sets the type of analysis for the simulation'''
        self.spice_file.write(".option post=2 ingold=2\n")
        # sets the simulation step and duration
        self.spice_file.write("." + self.sim_type + " " + self.sim_tinc + " " + self.sim_time + "n\n\n")
        self.spice_file.write(".end")
        return None


    def run_hspice(self):
        '''Runs hspice for each model simulation'''
        os.chdir(self.uut) # changes to uut directory
        # invokes hspice
        os.system('hspice ' + self.subuut + ".sp > " + self.subuut + ".lis")
        os.chdir(self.script_dir) # changes directory back to script
        return None


    def read_meas(self, start_str, end_str, line, lis_flag):
        '''Reads the measurements from .lis file'''
        lis_line_data = []
        if (start_str in line):
            lis_flag = 1 # start reading
        elif (end_str in line) and (lis_flag == 1):
            lis_flag = 0 # stop resding
        elif (lis_flag == 1):
            # append lines with data
            for datum in line.replace("=", " ").split(): # remove equal signs to capture negative numbers
                try:
                    lis_line_data.append(abs(float(datum))) # converts numeriral strings to floats
                except:
                    lis_line_data.append(datum) # adds names to list
        # returns the flag and data collected
        return (lis_flag, lis_line_data)


    def collect_data(self):
        '''Collects all data to import by python'''
        # will divide between avg and max
        power_series = [] # reads all power data
        delay_series = [] # reads all delay data
        timing_series = [] # reads all timing data
        with open(self.script_dir + "/" + self.uut + "/" + self.subuut + ".lis") as results:
            timing_flag = 0 # initializes flag
            delay_flag = 0 # initializes flag
            power_flag = 0 # initializes flag
            old_timing_flag = 0 # initializes flag 
            timing_len = 0
            for line in results:
                # reads the power measurements from .lis file
                (power_flag, power_line_data) = self.read_meas("transient analysis", "trf", line, power_flag)
                if (power_flag) and len(power_line_data):
                    power_series.append(power_line_data)
                # reads the delay measurements from .lis file
                (delay_flag, delay_line_data) = self.read_meas("source_avg_power", "x\n", line, delay_flag)
                if (delay_flag) and len(delay_line_data):
                    delay_series.append(delay_line_data)
                # reads the timing measurements from .lis file
                (timing_flag, timing_line_data) = self.read_meas("x\n", "y\n", line, timing_flag)
                if (timing_flag == 1) and len(timing_line_data):
                    if timing_len:# == len(timing_line_data):
                        for i in range(timing_len):
                            try:
                                if not(i):
                                    timing_series[i].append(timing_line_data[i] * 1e9) # 1e9 makes diagram visualization better
                                else:
                                    timing_series[i].append(timing_line_data[i])
                            except:
                                continue
                    else:
                        timing_len = len(timing_line_data) # gets width of measurments to create proper matrix
                        timing_series = [[] for i in range(timing_len)] # creates a matrix of proper width
                if (old_timing_flag == 1) and (timing_flag == 0):
                    for i in range(1, timing_len - 1):
                        timing_series[i].pop(0) # delete redundant item
                old_timing_flag = timing_flag

        # returns power, delay and timing data
        return (power_series, delay_series, timing_series)


    def clean_data(self, start_index, step, series):
        '''Cleans the data for delays and power'''
        model_uut_data = {}
        for datum in series[start_index::step]:
            # selects datum and datum name
            model_uut_data[datum[0]] = datum[1]

        return model_uut_data        


    '''NOT IN USE'''
    def get_power_avg(self, subuut_power_data):
        subuut_avg_power = []
        for power_keys in list(subuut_power_data.keys()):
            if "model_uut" in power_keys:
                subuut_avg_power.append(subuut_power_data.pop(power_keys))
        return sum(subuut_avg_power) / len(subuut_avg_power)


    def measure_delays(self):
        '''Measures all delays of model_uut_grid'''
        for instance in range(self.par_instances):
            rise_fall_count = 2 ** ((self.par_instances - instance) - 1) # calculates the amount of rises and falls of a signal
            for outin in range(self.ser_instances):
                inout = str(outin + 1)
                outin = str(outin)
                for rise_fall in range(rise_fall_count):
                    rise_fall = str(rise_fall + 1)
                    instance = str(instance)
                    # measures rise_fall delay
                    self.spice_file.write(".measure tran trf_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=vdd_50 rise=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=vdd_50 fall=" + rise_fall + "\n")
                    # measures rise_fall delay
                    self.spice_file.write(".measure tran tfr_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=vdd_50 fall=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=vdd_50 rise=" + rise_fall + "\n")
        # measures delay for inverter in fo4 chain
        self.spice_file.write(".measure tran fo4_inverter_rf_delay trig v(" + "outb_01) val=vdd_50 rise=" + rise_fall + " targ v(" + "outb_012) val=vdd_50 fall=" + rise_fall + "\n")
        # measures delay for inverter in fo4 chain
        self.spice_file.write(".measure tran fo4_inverter_fr_delay trig v(" + "outb_01) val=vdd_50 fall=" + rise_fall + " targ v(" + "outb_012) val=vdd_50 rise=" + rise_fall + "\n")
        return None


    def measure_power(self):
        '''Measures model_uut_grid and individual unit powers'''
        #self.spice_file.write("v_012 outb_012 gnd 0\n")
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                outin = str(outin)
                # measures individual max power
                self.spice_file.write(".measure tran model_uut_peak_power" + outin + instance  + " max p(xmodel_uut_grid.x" + "inverter" + outin + instance + ")\n")
                # measures individual avg power
                self.spice_file.write(".measure tran model_uut_avg_power" + outin + instance  + " avg p(xmodel_uut_grid.x" + "inverter" + outin + instance + ")\n")

        # measures peak power for an inverter in the middle of the FO4
        self.spice_file.write(".measure tran fo4_inverter_peak_power" + outin + instance  + " max p(xoutput_012)\n")
        # measures avg power for an inverter in the middle of the FO4
        self.spice_file.write(".measure tran fo4_inverter_avg_power avg p(xoutput_012)\n")
        # measures model_uut_grid max power
        self.spice_file.write(".measure tran uut_peak_power max p(xmodel_uut_grid)\n")
        # measures model_uut_grid avg power
        self.spice_file.write(".measure tran uut_avg_power avg p(xmodel_uut_grid)\n")
        # Serve more as flag to collect data
        self.spice_file.write(".measure tran source_peak_power max power\n") # measures source avg power
        self.spice_file.write(".measure tran source_avg_power avg power\n") # measures source max power
        return None


    def print_wave(self):
        '''Prints each datapoint to .lis file'''
        self.uut_subckt = []
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                inout = str(outin + 1)
                outin = str(outin)
                # prints data per input-output pair in each model_uut subckt
                self.spice_file.write(".print TRAN V(" + "outin_" + outin + instance + ") V(" + "outin_" + inout + instance + ")\n")
                self.uut_subckt.append("xinverter" + outin + instance)
                
        self.spice_file.write("\n")
        return None


#   def write_dram(self, instance):

