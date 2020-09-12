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

    temp = ptm("test", "nfet.pm", "pfet.pm")

    models_subdirs = temp.set_fet_names(dir_name)
    models_list = temp.get_models_libs()
    subdir_paths = temp.set_uut_dir(dir_name) # create uut directories and sbudirs

    nfin = "1000m"

    timing_data = [] # collects data to produce timing diagrams
    delay_data = []  # collects data to calculate avg delay 
    power_data = []  # collects data to present power

    for model_subdir in models_subdirs:
        parts = model_subdir.split("/")
        parts.reverse()
        parts = "".join(parts)
        subuut = [subuut_name for subuut_name in models_list if parts in subuut_name]
        subuut = subuut[0]
        with open(cwd + "/" + temp.uut + "/" + subuut + ".sp", 'w+') as uut:
            (fet_size, fet_voltage) = temp.get_fet_params(model_subdir)
            vdd_50 = str(float(fet_voltage) / 2)

            parallel_instances = 2 # modules with unique inout
            serial_instances = 2   # modules connected output to input
            load_amount = 1        # load amount for 'realistic' results

            sim_type = "tran"      # simulation type, e.g., tran, dc
            sim_tinc = "10p"       # time step for simulations
            sim_time = str(2 ** parallel_instances) # total simulation time

            # invokes subckts class
            subckts_modules = subckts(uut, fet_size, nfin, fet_voltage)

            # set .sp header
            script_path = cwd + "/" + __file__
            subckts_modules.set_library(script_path, subuut, temp.uut)

            uut.write("$Sources\n")
            # set source function
            uut.write("vdd vdd  gnd " + fet_voltage + "V\n")
            subckts_modules.write_source(parallel_instances)
 
            uut.write("$Unit Under Test\n")
            subckts_modules.set_inverter_subckt()
            subckts_modules.write_inverter(parallel_instances, serial_instances)

            uut.write("$Output Loads\n")
            subckts_modules.write_outputs(parallel_instances, load_amount, serial_instances)

            uut.write("$Measurements\n")
            subckts_modules.measure_power(parallel_instances, sim_time, serial_instances)
            subckts_modules.measure_delays(parallel_instances, serial_instances)
            subckts_modules.print_wave(parallel_instances, serial_instances)

            uut.write("$Simulation/Analysis Type\n")
            subckts_modules.analysis_type(sim_type, sim_tinc, sim_time)

        # run hspice
        subckts_modules.run_hspice(cwd, subuut, temp.uut)

        # collect all series
        (power_series, delay_series, timing_series) = subckts_modules.collect_data(cwd, subuut, temp.uut)

        timing_data.append(timing_series)
        delay_data.append(delay_series)
        power_data.append(power_series)

#    print(timing_data[0][1])
#    print(timing_data[0][2][1])

    data = pd.DataFrame(timing_data[0], columns = ['Time', 'Voltage_in', 'Voltage_out'])
    data_no_indices = data.to_string(index=False)

#    print(data_no_indices)
#    print(timing_data)
#    print(delay_data)
#    print(power_data)

if __name__ == '__main__':
    main()

