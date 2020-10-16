#!/usr/bin/env python
import os
import matplotlib.pyplot as plt

exec(open("python.py").read())
module('load', 'apps/synopsys/hspice/F-2011.09-SP2')

from classes.ptm import ptm
from classes.inverter import inverter
from classes.sram import sram

def main():
    # For the given path, get the full path list of transistors models
    cwd = os.getcwd() # gets the current_working_directoru
    fet_models_dir_name = cwd + '/modelfiles/' # full path to fet models files
    uut_setup = ptm("sram", "nfet.pm", "pfet.pm", "1000m") # calls ptm class
    uut_params = uut_setup.set_fet_names(fet_models_dir_name) # gets/sets fet names and creates uut directory

    lstp_subuuts = []    # stores all lstp subuuts names to ease color in diagrams
    hp_subuuts = []      # stores all hp subuuts names to ease color in diagrams
    ptm_sizes = []       # stores all fet sizes

    hp_delay = []        # collects hp delay data to graph
    lstp_delay = []      # collects lstp delay data to graph
    hp_power = []        # collects hp power data to graph
    lstp_power = []      # collects lstp power data to graph

    timing_data = {}     # collects data to produce timing diagrams
    hp_timing_in = []    # stores the signal in data
    hp_timing_out = []   # stores the signal our data
    lstp_timing_in = []  # stores the signal in data
    lstp_timing_out = [] # stores the signal our data
    timing_steps = []    # stores the time increments of the simulation

    for fet_params in uut_params:
        (subuut, fet_nfin) = fet_params
        with open(cwd + "/" + uut_setup.uut + "/" + subuut + ".sp", 'w+') as spice_file:
            data = 0
            uut = uut_setup.uut    # uut name
            script_name = __file__ # working script name
            script_params = (cwd, script_name, uut)

            parallel_instances = 1 # modules with unique inout
            serial_instances = 1   # modules connected output to input
            load_amount = 4        # load amount for 'realistic' results
            fan_out_chain = 4     # fan out grid extension
            grid_params = (spice_file, parallel_instances, serial_instances, load_amount, fan_out_chain)

            sim_type = "tran"      # simulation type, e.g., tran, dc
            sim_tinc = "1p"        # time step for simulations
            sim_time = "2n"        # str(2 ** parallel_instances) # simulataion time
            sim_params = (sim_type, sim_tinc, sim_time)

            # invokes subckts class
            subckts_modules = sram(script_params, grid_params, fet_params, sim_params)

            # set .sp header and calls library
            subckts_modules.set_library()

            spice_file.write("$ UUT individual unit\n")
            subckts_modules.set_cells_subckts()

            spice_file.write("$ Sources\n")
            spice_file.write("vdd vdd gnd vdd\n")
            subckts_modules.write_source(data)
 
            spice_file.write("$ Unit Under Test\n")
            subckts_modules.write_uut()

#            spice_file.write("$ Output Loads\n")
#            subckts_modules.write_outputs()
#
#
#            spice_file.write("$ Measurements\n")
#            subckts_modules.measure_power()
#            subckts_modules.measure_delays()
#            subckts_modules.print_wave()
#
            spice_file.write("$ Simulation/Analysis Type\n")
            subckts_modules.analysis_type()
#
        # run hspice
        subckts_modules.run_hspice()
#
#        # collect all series
#        (power_series, delay_series, timing_series) = subckts_modules.collect_data()
#
#        # collects all timing data
#        timing_data[subuut] = timing_series
#
#        # collects delay values and calculates delay average
#        list_rf_values = list(subckts_modules.clean_data(0, 2, delay_series).values())[-1]
#        list_fr_values = list(subckts_modules.clean_data(1, 2, delay_series).values())[-1]
#        delay_values = [list_rf_values, list_fr_values]
#
#        if "hp" in subuut:
#            hp_subuuts.append(subuut) # collects all hp subuut names
#            # collects all ptm sizes
#            ptm_sizes.append(int(subuut.replace("ptm","").replace("hp","")))
#            # collects all hp delays
#            hp_delay.append(sum(delay_values) / len(delay_values) * 1e12)
#            # collects all hp powers
#            hp_power.append(subckts_modules.clean_data(2, 3, power_series)["fo4_inverter_avg_power"] * 1e9)# * 1e12)
#
#        if "lstp" in subuut:
#            lstp_subuuts.append(subuut) # collects all lstp subuut names
#            # collects all lstp delays
#            lstp_delay.append(sum(delay_values) / len(delay_values) * 1e12)
#            # collects all lstp powers
#            lstp_power.append(subckts_modules.clean_data(2, 3, power_series)["fo4_inverter_avg_power"] * 1e9)# * 1e12)
#
#    plt.figure(1)
#    plt.title("Average Power by FET size for \nHigh Performance ('red') and Low Standby Power ('blue')")
#    plt.scatter(ptm_sizes, hp_power, color = "red")
#    plt.scatter(ptm_sizes, lstp_power)
#
#    plt.figure(2)
#    plt.title("Average Delay by FET size for \nHigh Performance ('red') and Low Standby Power ('blue')")
#    plt.scatter(ptm_sizes, hp_delay, color = "red")
#    plt.scatter(ptm_sizes, lstp_delay)
#
#    color_list = ["magenta", "red", "blue", "green", "black"]
#    plt.figure(3)
#    plt.title("Signal In to the FO4 chain inverter \nHigh Performance")
#    plt.xlim(0, 1)
#    plt.ylim(0, .91)
#    for subuut, color in zip(hp_subuuts, color_list):
#        plt.plot(timing_data[subuut][0], timing_data[subuut][1], color = color)
#
#    plt.figure(4)
#    plt.title("Signal Out of the FO4 chain inverter \nHigh Performance")
#    plt.xlim(0, 1)
#    plt.ylim(0, .91)
#    for subuut, color in zip(hp_subuuts, color_list):
#        plt.plot(timing_data[subuut][0], timing_data[subuut][2], color = color)
# 
#    plt.figure(5)
#    plt.title("Signal In to the FO4 chain inverter \nLow Standby Power")
#    plt.xlim(0, 1)
#    plt.ylim(0, .91)
#    for subuut, color in zip(lstp_subuuts, color_list):
#        plt.plot(timing_data[subuut][0], timing_data[subuut][1], color = color)
#
#    plt.figure(6)
#    plt.title("Signal Out of the FO4 chain inverter \nLow Standby Power")
#    plt.xlim(0, 1)
#    plt.ylim(0, .91)
#    for subuut, color in zip(lstp_subuuts, color_list):
#        plt.plot(timing_data[subuut][0], timing_data[subuut][2], color = color)
#
#    plt.show()


if __name__ == '__main__':
    main()
