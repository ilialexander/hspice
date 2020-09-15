#!/usr/bin/env python
import os
import pandas as pd

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
    

    for fet_params in uut_params:
        (subuut, fet_length, fet_voltage, fet_nfin) = fet_params
        with open(cwd + "/" + uut_setup.uut + "/" + subuut + ".sp", 'w+') as spice_file:

            uut = uut_setup.uut         # uut name
            script_name = __file__ # working script name
            script_params = (cwd, script_name, uut)

            parallel_instances = 2 # modules with unique inout
            serial_instances = 2   # modules connected output to input
            load_amount = 1        # load amount for 'realistic' results
            grid_params = (spice_file, parallel_instances, serial_instances, load_amount)

            sim_type = "tran"      # simulation type, e.g., tran, dc
            sim_tinc = "10p"       # time step for simulations
            sim_params = (sim_type, sim_tinc)

            # invokes subckts class
            subckts_modules = subckts(script_params, grid_params, fet_params, sim_params)

            # set .sp header
            subckts_modules.set_library()

            spice_file.write("$ UUT individual unit\n")
            subckts_modules.set_inverter_subckt()

            spice_file.write("$ Sources\n")
            spice_file.write("vdd vdd  gnd " + fet_voltage + "V\n")
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

        # collect all series
        (power_series, delay_series, timing_series) = subckts_modules.collect_data()

        # collect all data
        timing_data[subuut] = timing_series
        rise_fall_data[subuut] = subckts_modules.clean_data(0, 2, delay_series)
        fall_rise_data[subuut] = subckts_modules.clean_data(1, 2, delay_series)
        peak_power_data[subuut] = subckts_modules.clean_data(0, 3, power_series)
        avg_power_data[subuut] = subckts_modules.clean_data(2, 3, power_series)

        list_rf_values = list(rise_fall_data[subuut].values())
        list_fr_values = list(fall_rise_data[subuut].values())
        delay_values = list_rf_values + list_fr_values 
        avg_delay_data[subuut] = sum(delay_values) / len(delay_values)

        model_uut_avg_power = []
        for power_keys in list(avg_power_data[subuut].keys()):
            if "model_uut" in power_keys:
                model_uut_avg_power.append(avg_power_data[subuut][power_keys])
        subckt_avg_power_data[subuut] = sum(model_uut_avg_power) / len(model_uut_avg_power)

        model_uut_peak_power = []
        for power_keys in list(peak_power_data[subuut].keys()):
            if "model_uut" in power_keys:
                model_uut_peak_power.append(peak_power_data[subuut][power_keys])
        subckt_peak_power_data[subuut] = sum(model_uut_peak_power) / len(model_uut_peak_power)
        #subckt_avg_power_data = {}  # collects subckt average power data
    
        #print(timing_data[subuut][subckts_modules.uut_subckt[0]])
        #print(subckts_modules.uut_subckt)
        #print(peak_power_data[subuut])
        #print(avg_power_data[subuut])
        #break
    #print(avg_delay_data)

    #print(timing_series)
#    print(timing_data[0][2][1])

    #trf_delays = delay_series[0::2]
    #print(trf_delays[:])
    #print(delay_series[1::2][:][:1])

    #data = pd.DataFrame(timing_data[fet_params][subckts_modules.uut_subckt[3]], columns = ['Time', 'Voltage_in', 'Voltage_out'])
    #data_no_indices = data.to_string(index=False)
    #print(data_no_indices)

#    print(data_no_indices)
#    print(timing_data)

if __name__ == '__main__':
    main()

