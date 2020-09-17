#!/usr/bin/env python
import os

class subckts:

    def __init__(self, script_params, grid_params, fet_params, sim_params):
        (script_dir, script_name, uut) = script_params 
        self.script_dir = script_dir # script working directory
        self.uut = uut # unit under test
        self.script_name = script_name # name of running script

        (spice_file, parallel_instances, serial_instances, load_amount) = grid_params
        self.spice_file = spice_file # name of unit under test, e.g. inverter
        self.par_instances = parallel_instances # grid columns
        self.ser_instances = serial_instances # grid rows
        self.load_amount = load_amount # load for realistic results

        (subuut, fet_length, fet_voltage, fet_nfin) = fet_params
        self.subuut = subuut # ptm under test
        self.fet_length = fet_length # fet length size, e.g. 14nm, 10nm, 7nm
        self.fet_voltage = fet_voltage # nominal voltage for ptm model
        self.fet_nfin = fet_nfin # fin size?? e.g. 1000m

        (sim_type, sim_tinc) = sim_params
        self.sim_type = sim_type # simulation type, e.g., tran, dc
        self.sim_tinc = sim_tinc # simulation time step

        self.vdd_50 = str(float(self.fet_voltage) / 2) # 50% of vdd/nominal voltage
        self.sim_time = str(2 ** self.par_instances) # total simulation time
        self.script_path = self.script_dir + "/" + self.script_name # full path to working script


    '''Inputs and Outputs LOADS'''

    def write_source(self):
        '''Write input source of system to .sp file'''
        # input sources are porportional to the amount of instances
        self.spice_file.write("$all input sources\n")
        for instance in range(self.par_instances):
            fall_time = (2) * (2 ** instance) # time from highest value to lowest, it provides a virtual binary count
            rise_time = str(fall_time / 2)    # time from lowest value to lowest
            fall_time = str(fall_time)
            instance = str(instance)
            # sets input wave
            self.spice_file.write("vin_" + instance + " inb_" + instance + " gnd  PULSE(" + self.fet_voltage + "V " + "0V 0ns 1ps 1ps " + rise_time + "n " + fall_time + "n)\n")
            #self.spice_file.write("vin_" + instance + " outin_0" + instance + " gnd  PULSE(" + self.fet_voltage + "V " + "0V 0ns 1ps 1ps " + rise_time + "n " + fall_time + "n)\n")

        # sets a more realistic input through inverter
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
        self.spice_file.write("\n")
        return None



    '''UUTs'''
    def set_inverter_subckt(self):
        '''Write inverter subckt'''
        # declare subckt name, input, output, and source
        self.spice_file.write(".subckt inverter in out vdd\n")
        self.spice_file.write("$fets" + "\n")
        # call pfet model name, and decaler its input, output, and source
        self.spice_file.write("xpfet out in vdd vdd pfet l=" + self.fet_length + "n nfin=" + self.fet_nfin + "\n")
        # call nfet model name, and decaler its input, output, and source
        self.spice_file.write("xnfet out in gnd gnd nfet l=" + self.fet_length + "n nfin=" + self.fet_nfin + "\n")
        self.spice_file.write(".ends\n") # end subckt declaration
        self.spice_file.write("\n")
        return None

    def write_inverter(self):
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
        return None


    def analysis_type(self):
        '''Sets the type of analysis for the simulation'''
        self.spice_file.write(".option post=2 ingold=2\n")
        # sets the simulation step and duration
        self.spice_file.write("." + self.sim_type + " " + self.sim_tinc + " " + self.sim_time + "ns\n\n")
        self.spice_file.write(".end")
        return None


    def run_hspice(self):
        '''Runs hspice for each model simulation'''
        os.chdir(self.uut) # changes to uut directory
        # invokes hspice
        os.system('hspice ' + self.subuut + ".sp > " + self.subuut + ".lis")
        os.chdir(self.script_dir) # changes directory back to script
        return None


    def read_meas(self, start_str, end_str, line, lis_flag, lis_series):
        '''Reads the measurements from .lis file'''
        if (start_str in line):
            lis_flag = 1 # start reading
        elif (end_str in line) and (lis_flag == 1):
            lis_flag = 0 # stop resding
        elif (lis_flag == 1):
            # append lines with data
            lis_line_data = []
            for datum in line.replace("=", " ").split(): # remove equal signs to capture negative numbers
                try:
                    lis_line_data.append(abs(float(datum))) # converts numeriral strings to floats
                except:
                    lis_line_data.append(datum) # adds names to list
            lis_series.append(lis_line_data)
        # returns the flag and data collected
        return (lis_flag, lis_series)


    def collect_data(self):
        '''Collects all data to import by python'''
        # will divide between avg and max
        power_series = [] # reads all power data
        delay_series = [] # reads all delay data
        timing_series = [] # reads all timing data
        uut_timing_series = {}
        model_uut_count = 0
        with open(self.script_dir + "/" + self.uut + "/" + self.subuut + ".lis") as results:
            timing_flag = 0 # initializes flag
            delay_flag = 0 # initializes flag
            power_flag = 0 # initializes flag
            old_timing_flag = 0 # initializes flag 
            for line in results:
                # reads the power measurements from .lis file
                (power_flag, power_series) = self.read_meas("transient analysis", "trf", line, power_flag, power_series)
                # reads the delay measurements from .lis file
                (delay_flag, delay_series) = self.read_meas("source_avg_power", "x\n", line, delay_flag, delay_series)
                # reads the timing measurements from .lis file
                (timing_flag, timing_series) = self.read_meas("x\n", "y\n", line, timing_flag, timing_series)
                if (old_timing_flag == 1) and (timing_flag == 0):
                    timing_series.pop(0) # delete empty item
                    timing_series.pop(1) # delete redundant item
                    uut_timing_series[self.uut_subckt[model_uut_count]] = timing_series
                    model_uut_count += 1 # move to next model_uut time_series
                    timing_series = []
                old_timing_flag = timing_flag

        # returns power, delay and timing data
        return (power_series, delay_series, uut_timing_series)


    def clean_data(self, start_index, step, series):
        '''Cleans the data for delays and power'''
        model_uut_data = {}
        for datum in series[start_index::step]:
            # selects datum and datum name
            model_uut_data[datum[0]] = datum[1]

        return model_uut_data        


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
                    self.spice_file.write(".measure tran trf_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=" + self.vdd_50 + " rise=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=" + self.vdd_50 + " fall=" + rise_fall + "\n")
                    # measures rise_fall delay
                    self.spice_file.write(".measure tran tfr_delay_" + outin + instance + rise_fall + " trig v(" + "outin_" + outin + instance + ") val=" + self.vdd_50 + " fall=" + rise_fall + " targ v(" + "outin_" + inout + instance + ") val=" + self.vdd_50 + " rise=" + rise_fall + "\n")
        return None


    def measure_power(self):
        '''Measures model_uut_grid and individual unit powers'''
        for instance in range(self.par_instances):
            for outin in range(self.ser_instances):
                instance = str(instance)
                outin = str(outin)
                # measures individual max power
                self.spice_file.write(".measure tran model_uut_peak_power" + outin + instance  + " max p(xmodel_uut_grid.x" + "inverter" + outin + instance + ")\n")
                # measures individual avg power
                self.spice_file.write(".measure tran model_uut_avg_power" + outin + instance  + " avg p(xmodel_uut_grid.x" + "inverter" + outin + instance + ")\n") # from=0ns to=" + self.sim_time + "ns\n")

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

