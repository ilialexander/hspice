#!/usr/bin/env python
import os

from classes.inverter import inverter

class sram(inverter):
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

        (sim_type, sim_tinc, sim_time, data) = sim_params
        self.sim_type = sim_type # simulation type, e.g., tran, dc
        self.sim_tinc = sim_tinc # simulation time step
        self.sim_time = sim_time # total simulation time
        self.data = data         # data to write in sram cell

        self.script_path = self.script_dir + "/" + self.script_name # full path to working script



    '''Inputs and Outputs LOADS'''

    def write_source(self):
        '''write sourse system to .sp file'''
        # input sources are porportional to the amount of instances
        self.spice_file.write("$Sources\n")
        for instance in range(self.par_instances):
            fall_time = (2) * (2 ** instance) / 4 # time from highest value to lowest, it provides a virtual binary count
            rise_time_str = str(fall_time / 2)    # time from lowest value to lowest
            fall_time_str = str(fall_time)
            ins_str = str(instance)
            # sets world line wave
            self.spice_file.write("vin_wl_" + ins_str + " in_wl_" + ins_str + "  gnd  pulse(vdd " + "0v 0.25ns " + self.sim_tinc + " " + self.sim_tinc + " " + rise_time_str + "n " + fall_time_str + "n)\n")
            self.spice_file.write("xwl_" + ins_str + " in_wl_" + ins_str + " wl_" + ins_str + " vdd " + "inverter\n")

        for outin in range(self.ser_instances):
            fall_time = (2) * (2 ** instance) / 2 # time from highest value to lowest, it provides a virtual binary count
            rise_time_str = str(fall_time / 2)    # time from lowest value to lowest
            fall_time_str = str(fall_time)
            inout = str(outin)
            # sets data wave
            if self.data == 1:
                self.spice_file.write("xdata_" + inout + " vdd data_" + inout + " vdd " + "inverter\n")
            else:
                self.spice_file.write("xdata_" + inout + " gnd data_" + inout + " vdd " + "inverter\n")


            fall_time = (2) * (2 ** instance) # time from highest value to lowest, it provides a virtual binary count
            rise_time_str = str(fall_time / 8)    # time from lowest value to lowest
            fall_time_str = str(fall_time)
            self.spice_file.write("vin_phi" + inout + " in_phi_" + inout + "  gnd  pulse(0v " + "vdd 0.2ns " + self.sim_tinc + " " + self.sim_tinc + " 0.2n " + fall_time_str + "n)\n")
            self.spice_file.write("xphi_" + inout + " in_phi_" + inout + " phi_" + inout + " vdd " + "inverter\n")
            # sets write enable wave
            self.spice_file.write("vin_we_" + ins_str + " in_we_" + ins_str + "  gnd  pulse(vdd " + "0v 0.26n " + self.sim_tinc + " " + self.sim_tinc + " " + rise_time_str + "n " + fall_time_str + "n)\n")
            self.spice_file.write("xwe_" + ins_str + " in_we_" + ins_str + " we_" + ins_str + " vdd " + "inverter\n")
            # sets sense amplifier enable / reading enable wave
            self.spice_file.write("vin_sae" + inout + " in_sae_" + inout + "  gnd  pulse(vdd " + "0v .8ns " + self.sim_tinc + " " + self.sim_tinc + " " + rise_time_str + "n " + fall_time_str + "n)\n")
            self.spice_file.write("xsae_" + inout + " in_sae_" + inout + " sae_" + inout + " vdd " + "inverter\n")
            self.spice_file.write("xsaeb_" + inout + " sae_" + inout + " saeb_" + inout + " vdd " + "inverter\n")

        self.spice_file.write("\n")
        return None


    def write_outputs(self):
        '''Write realistic output load of system to .sp file'''
        for instance in range(self.par_instances):
            inout = str(self.ser_instances) # connects model_uut output to realistic loads
            for output_tag in range(self.load_amount):
                ins_str = str(instance) # instance of ouput to evaluate
                output_tag = str(output_tag) # amount of load per output
                # call instance of ouput load subckt for model_uut
                self.spice_file.write("xoutput_" + ins_str + output_tag + " outin_" + inout  + ins_str + " outb_" + ins_str + output_tag + " vdd " + "inverter\n")
                # creates FO4 chain of inverters
        self.spice_file.write("\n")
        return None



    '''UUTs'''
    def set_cells_subckts(self, subuut):
        # declare inverter subckt
        self.spice_file.write(".subckt inverter in out vdd\n")
        self.spice_file.write("xpfet out in vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write("xnfet out in gnd gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write(".ends\n\n")

        # declare blline conditioning/pre-charge subckt
        self.spice_file.write(".subckt prec phi bl bbl \n")
        if "hp" in subuut:
            self.spice_file.write("xprec_bl bl phi vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xprec_bbl bbl phi vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
        else:
            self.spice_file.write("xprec_eq bl phi bbl vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write(".ends\n\n")

        # declare write subckt
        self.spice_file.write(".subckt writing we data bl bbl vdd\n")
        self.spice_file.write("xwrite_bl  datab we bl  gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write("xwrite_bbl data  we bbl gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write("xq  data datab vdd inverter\n")
        self.spice_file.write(".ends\n\n")

        # declare sram subckt
        self.spice_file.write(".subckt sram wl bl bbl vdd\n")
        self.spice_file.write("xnfet_bl  bl  wl q  gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write("xnfet_bbl bbl wl qb gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write("xq  qb q  vdd inverter\n")
        self.spice_file.write("xqb q  qb vdd inverter\n")
        self.spice_file.write(".ends\n\n")

        # declare sense amplifier subckt
        self.spice_file.write(".subckt sa sae saeb bl bbl vdd\n")
        if "hp" in subuut:
            self.spice_file.write("xvdd_acc vdd_acc saeb vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xgnd_acc gnd_acc sae  gnd gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xneq  bl saeb bbl gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xpdiff  bl  bbl vdd_acc vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xpdiffb bbl bl  vdd_acc vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xndiff  bl  bbl gnd_acc gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xndiffb bbl bl  gnd_acc gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        else:
            self.spice_file.write("xvdd_acc vdd_acc saeb vdd vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xgnd_acc gnd_acc sae  gnd gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xneq  bl saeb bbl gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xpdiff  bl  bbl vdd_acc vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xpdiffb bbl bl  vdd_acc vdd pfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xndiff  bl  bbl gnd_acc gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
            self.spice_file.write("xndiffb bbl bl  gnd_acc gnd nfet l=lg nfin=" + self.fet_nfin + "\n")
        self.spice_file.write(".ends\n")
        return None

    def write_uut(self):
        '''Write sram device'''
        self.spice_file.write(".subckt uut_grid vdd\n")
        self.spice_file.write("+")
        for outin in range(self.ser_instances):
            inout = str(outin)
            # declare subckt inputs
            self.spice_file.write("sae_" + inout + " " + "saeb_" + inout + " " + "phi_" + inout + " " + "bl_" + inout + " " + "bbl_" + inout + " " + "we_" + inout + " " + "data_" + inout + " ")
            for instance in range(self.par_instances):
                ins_str = str(instance)
                self.spice_file.write("wl_" + ins_str + " ")
        self.spice_file.write("$inputs to uut_grid Subckt\n")

        self.spice_file.write("+")
        for outin in range(self.ser_instances):
            instance = str(instance)
            inout = str(outin + 1)
            # declare subckt outputs
            self.spice_file.write("d_out_" + inout + " ")
        self.spice_file.write("$outputs to uut_grid Subckt\n")

        for outin in range(self.ser_instances):
            inout = str(outin)
            # invoke pre-charge subckt 
            self.spice_file.write("xprec_" + inout + " " + "phi_" + inout + " " + "bl_" + inout + " " + "bbl_" + inout + " " + "prec\n")
            for instance in range(self.par_instances):
                ins_str = str(instance)
                # invoke srams subckt 
                self.spice_file.write("xsram_" + inout + ins_str + " " + "wl_" + ins_str + " " + "bl_" + inout + " " + "bbl_" + inout + " vdd " + "sram\n")

            # invoke writing subckt 
            self.spice_file.write("xwriting_" + inout + " " + "we_" + inout + " " + "data_" + inout + " " + "bl_" + inout + " " + "bbl_" + inout + " vdd " + "writing\n")
            # invoke sense-amplifier subckt 
            self.spice_file.write("xsa_" + inout + " " + "sae_" + inout + " " + "saeb_" + inout + " " + "bl_" + inout + " " + "bbl_" + inout + " " + "vdd" + " sa\n")
        self.spice_file.write(".ends\n")

        # invoke uut_grid
        self.spice_file.write("$invoke UUT grid\n")
        self.spice_file.write("xuut_grid vdd\n")
        self.spice_file.write("+")
        for outin in range(self.ser_instances):
            inout = str(outin)
            # declare subckt inputs
            self.spice_file.write("sae_" + inout + " " + "saeb_" + inout + " " + "phi_" + inout + " " + "bl_" + inout + " " + "bbl_" + inout + " " + "we_" + inout + " " + "data_" + inout + " ")
            for instance in range(self.par_instances):
                ins_str = str(instance)
                self.spice_file.write("wl_" + ins_str + " ")
        self.spice_file.write("$inputs to uut_grid\n")

        self.spice_file.write("+")
        for outin in range(self.ser_instances):
            inout = str(outin)
            # declare subckt outputs
            self.spice_file.write("d_out_" + inout + " ")
        self.spice_file.write("$outputs to uut_grid\n")
        self.spice_file.write("+uut_grid\n\n")
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
        # gets XX% of vdd for delay calculation
        self.spice_file.write(".param vdd_50='vdd*.5'"  "\n")
        self.spice_file.write(".param vdd_10='vdd*.1'"  "\n")
        self.spice_file.write(".param vdd_15='vdd*.15'"  "\n")
        self.spice_file.write(".param vdd_90='vdd*.9'"  "\n")
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
                (power_flag, power_line_data) = self.read_meas("transient analysis", "write_q", line, power_flag)
                if (power_flag) and len(power_line_data):
                    power_series.append(power_line_data)
                # reads the delay measurements from .lis file
                (delay_flag, delay_line_data) = self.read_meas("sa_avg_read_power", "uut_avg_power", line, delay_flag)
                if (delay_flag) and len(delay_line_data):
                    delay_series.append(delay_line_data)
        return (power_series, delay_series)


    def clean_data(self, start_index, step, series):
        '''Cleans the data for delays and power'''
        model_uut_data = {}
        for datum in series[start_index::step]:
            # selects datum and datum name
            model_uut_data[datum[0]] = datum[1]

        return model_uut_data        


    def measure_delays(self):
        '''Measures all delays of uut_grid'''
        for instance in range(self.par_instances):
            rise_fall_count = 2 ** ((self.par_instances - instance) - 1) # calculates the amount of rises and falls of a signal
            for outin in range(self.ser_instances):
                inout = str(outin)
                for rise_fall in range(rise_fall_count):
                    ins_str = str(instance)
                    if self.data == 1:
                        # measures write q delay
                        self.spice_file.write(".measure tran write_q_delay_" + inout + ins_str + " trig v(wl_" + inout + ") val=vdd_10 rise=1 targ v(xuut_grid.xsram_" + inout + ins_str + ".q) val=vdd_90 rise=1\n")
                        # measures read delay
                        self.spice_file.write(".measure tran read_q_delay_" + inout + ins_str + "  trig v(sae_" + inout + ") val=vdd_10 rise=1 targ v(xuut_grid.bl_" + inout + ") val=vdd_90 rise=1\n")
                    else:
                        # measures write q delay
                        self.spice_file.write(".measure tran write_q_delay_" + inout + ins_str + " trig v(wl_" + inout + ") val=vdd_10 rise=1 targ v(xuut_grid.xsram_" + inout + ins_str + ".qb) val=vdd_90 rise=1\n")
                        # measures read delay
                        self.spice_file.write(".measure tran read_q_delay_" + inout + ins_str + "  trig v(sae_" + inout + ") val=vdd_10 rise=1 targ v(xuut_grid.d_out_" + inout + ") val=vdd_90 rise=1\n")
        self.spice_file.write(".measure tran uut_avg_power avg p(xuut_grid)\n")
        return None


    def measure_power(self):
        '''Measures uut_grid and individual unit powers'''
        # measures uut avg power
        self.spice_file.write(".measure tran uut_avg_hold_power avg p(xuut_grid) from=0ns to=0.15ns\n")
        self.spice_file.write(".measure tran uut_avg_write_power avg p(xuut_grid) from=0.15ns to=0.35ns\n")
        self.spice_file.write(".measure tran uut_avg_read_power avg p(xuut_grid) from=0.7ns to=0.9ns\n")
        for outin in range(self.ser_instances):
            inout = str(outin)
            # measures precharge avg power
            self.spice_file.write(".measure tran prec_avg_hold_power_" + inout + " avg p(xuut_grid.xprec_" + inout + ") from=0ns to=0.15ns\n")
            self.spice_file.write(".measure tran prec_avg_write_power_" + inout + " avg p(xuut_grid.xprec_" + inout + ") from=0.15ns to=0.35ns\n")
            self.spice_file.write(".measure tran prec_avg_read_power_" + inout + " avg p(xuut_grid.xprec_" + inout + ") from=0.7ns to=0.9ns\n")
            for instance in range(self.par_instances):
                ins_str = str(instance)
                # measures sram avg power
                self.spice_file.write(".measure tran sram_avg_hold_power_" + inout + ins_str + " avg p(xuut_grid.xsram_" + inout + ins_str + ") from=0ns to=0.15ns\n")
                self.spice_file.write(".measure tran sram_avg_write_power_" + inout + ins_str + " avg p(xuut_grid.xsram_" + inout + ins_str + ") from=0.15ns to=0.35ns\n")
                self.spice_file.write(".measure tran sram_avg_read_power_" + inout + ins_str + " avg p(xuut_grid.xsram_" + inout + ins_str + ") from=0.7ns to=0.9ns\n")
            # measures writing avg power
            self.spice_file.write(".measure tran writing_avg_hold_power_" + inout + " avg p(xuut_grid.xwriting_" + inout + ") from=0ns to=0.15ns\n")
            self.spice_file.write(".measure tran writing_avg_write_power_" + inout + " avg p(xuut_grid.xwriting_" + inout + ") from=0.15ns to=0.35ns\n")
            self.spice_file.write(".measure tran writing_avg_read_power_" + inout + " avg p(xuut_grid.xwriting_" + inout + ") from=0.7ns to=0.9ns\n")
            # measures sa avg power
            self.spice_file.write(".measure tran sa_avg_hold_power_" + inout + " avg p(xuut_grid.xsa_" + inout + ") from=0ns to=0.15ns\n")
            self.spice_file.write(".measure tran sa_avg_writing_power_" + inout + " avg p(xuut_grid.xsa_" + inout + ") from=0.15ns to=0.35ns\n")
            self.spice_file.write(".measure tran sa_avg_read_power_" + inout + " avg p(xuut_grid.xsa_" + inout + ") from=0.7ns to=0.9ns\n")

        return None


