#!/usr/bin/env python
import os
import pandas as pd
import matplotlib.pyplot as plt

exec(open("python.py").read())
module('load', 'apps/synopsys/hspice/F-2011.09-SP2')

from classes.ptm import ptm
from classes.subckts import subckts

def main():
    # For the given path, get the full path list of transistors models
    cwd = os.getcwd() # gets the current_working_directoru
    dir_name = cwd + '/modelfiles/'

    uut_setup = ptm("inverter", "nfet.pm", "pfet.pm", "1000m")

    uut_params = uut_setup.set_fet_names(dir_name) # gets/sets fet names and creates uut directory

    timing_data = {}     # collects data to produce timing diagrams
    rise_fall_data = {}  # collects data to calculate rise_fall avg delay 
    fall_rise_data = {}  # collects data to calculate fall_rise avg delay 
    avg_delay_data = {}  # collects data to calculate rise_fall avg delay 
    peak_power_data = {} # collects peak power data
    subckt_peak_power_data = {} # collects subckt peak power data
    avg_power_data = {}  # collects average power data
    subckt_avg_power_data = {}  # collects subckt average power data
    hp_delay = []
    lstp_delay = []
    hp_power = []
    lstp_power = []

    hp_timing_in = []
    hp_timing_out = []
    lstp_timing_in = []
    lstp_timing_out = []
    timing_steps = []

    ptm_sizes = []
    
    #exit()
    for fet_params in uut_params:
        (subuut, fet_nfin) = fet_params
        with open(cwd + "/" + uut_setup.uut + "/" + subuut + ".sp", 'w+') as spice_file:

            uut = uut_setup.uut    # uut name
            script_name = __file__ # working script name
            script_params = (cwd, script_name, uut)

            parallel_instances = 1 # modules with unique inout
            serial_instances = 1   # modules connected output to input
            load_amount = 4        # load amount for 'realistic' results
            fan_out_chain = 64     # load amount for fan out
            grid_params = (spice_file, parallel_instances, serial_instances, load_amount, fan_out_chain)

            sim_type = "tran"      # simulation type, e.g., tran, dc
            sim_tinc = "1p"        # time step for simulations
            sim_time = "1n"        # str(2 ** parallel_instances) # simulataion time
            sim_params = (sim_type, sim_tinc, sim_time)

            # invokes subckts class
            subckts_modules = subckts(script_params, grid_params, fet_params, sim_params)

            # set .sp header
            subckts_modules.set_library()

            spice_file.write("$ UUT individual unit\n")
            subckts_modules.set_inverter_subckt()

            spice_file.write("$ Sources\n")
            spice_file.write("vdd vdd gnd vdd\n")
            subckts_modules.write_source()
 
            spice_file.write("$ Unit Under Test\n")
            subckts_modules.write_inverter()

            spice_file.write("$ Output Loads\n")
            subckts_modules.write_outputs()


            spice_file.write("$ Measurements\n")
            subckts_modules.measure_power()
            subckts_modules.measure_delays()
            subckts_modules.print_wave()

            spice_file.write("$ Simulation/Analysis Type\n")
            subckts_modules.analysis_type()

        # run hspice
        subckts_modules.run_hspice()

        #exit()
        # collect all series
        (power_series, delay_series, timing_series) = subckts_modules.collect_data()

        # collect all data
        timing_data[subuut] = timing_series
        rise_fall_data[subuut] = subckts_modules.clean_data(0, 2, delay_series)
        fall_rise_data[subuut] = subckts_modules.clean_data(1, 2, delay_series)
        peak_power_data[subuut] = subckts_modules.clean_data(0, 3, power_series)
        avg_power_data[subuut] = subckts_modules.clean_data(2, 3, power_series)

        #print(subuut)
        list_rf_values = list(rise_fall_data[subuut].values())
        list_fr_values = list(fall_rise_data[subuut].values())
        delay_values = list_rf_values + list_fr_values # list_fr_values # 
        avg_delay_data[subuut] = sum(delay_values) / len(delay_values)

        #print(timing_data[subuut].values())
        if "hp" in subuut:
            ptm_sizes.append(int(subuut.replace("ptm","").replace("hp","")))
            hp_delay.append(avg_delay_data[subuut] * 1e12)
            #print("HP delay value:", avg_delay_data[subuut])
            hp_power.append(avg_power_data[subuut]["model_uut_avg_power012"] * 1e9)# * 1e12)
            #print("HP power value:", avg_power_data[subuut]["model_uut_avg_power012"])

        if "lstp" in subuut:
            lstp_delay.append(avg_delay_data[subuut] * 1e12)
            #print("LSTP delay value:", avg_delay_data[subuut])
            lstp_power.append(avg_power_data[subuut]["model_uut_avg_power012"] * 1e9)# * 1e12)
            #print("LSTP power value:", avg_power_data[subuut]["model_uut_avg_power012"])

        #exit()
        #break
    plt.figure(1)
    plt.title("Average Power by FET size for \nHigh Performance ('red') and Low Standby Power ('blue')")
    plt.scatter(ptm_sizes, hp_power, color = "red")
    plt.scatter(ptm_sizes, lstp_power)

    plt.figure(2)
    plt.title("Average Delay by FET size for \nHigh Performance ('red') and Low Standby Power ('blue')")
    plt.scatter(ptm_sizes, hp_delay, color = "red")
    plt.scatter(ptm_sizes, lstp_delay)

    plt.figure(3)
    plt.title("Signal in to the FO4 chain inverter \nHigh Performance")
    for fet_params in uut_params:
        (subuut, fet_nfin) = fet_params
        if "hp" in subuut:
            plt.plot(timing_data[subuut][0], timing_data[subuut][1])
 
    plt.show()

    #data = pd.DataFrame(timing_data[subuut][subckts_modules.uut_subckt[3]], columns = ['Time', 'Voltage_in', 'Voltage_out'])
    #data_no_indices = data.to_string(index=False)
    #print(data_no_indices)


if __name__ == '__main__':
    main()
