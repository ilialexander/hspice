#!/usr/bin/env python
import os
import matplotlib.pyplot as plt

exec(open("python.py").read())
module('load', 'apps/synopsys/hspice/F-2011.09-SP2')

from classes.ptm import ptm
from classes.inverter import inverter
from classes.lstp_cam import lstp_cam
from classes.hp_cam import hp_cam

def lstp_cam_script():
    # For the given path, get the full path list of transistors models
    cwd = os.getcwd() # gets the current_working_directoru
    fet_models_dir_name = cwd + '/modelfiles/' # full path to fet models files
    uut_setup = ptm("lstp_cam", "nfet.pm", "pfet.pm", "1000m") # calls ptm class
    uut_params = uut_setup.set_fet_names(fet_models_dir_name) # gets/sets fet names and creates uut directory
    cap_dict = {"ptm7lstp": "0.2ff", "ptm10lstp": "0.6ff", "ptm14lstp": "1.0ff", "ptm16lstp": "1.2ff", "ptm20lstp": "1.6ff",
    "ptm7hp": "0.2ff", "ptm10hp": "0.6ff", "ptm14hp": "1.0ff", "ptm16hp": "1.2ff", "ptm20hp": "1.6ff"}
    ptm_sizes = []       # stores all fet sizes
    hp_write_delay = []        # collects hp delay data to graph
    hp_read_delay = []        # collects hp delay data to graph
    lstp_write_delay = []      # collects lstp delay data to graph
    lstp_read_delay = []      # collects lstp delay data to graph
    write_hp_power = []        # collects hp write power data to graph
    write_lstp_power = []      # collects lstp write power data to graph
    hold_hp_power = []        # collects hp hold power data to graph
    hold_lstp_power = []      # collects lstp hold power data to graph
    read_hp_power = []        # collects hp read power data to graph
    read_lstp_power = []      # collects lstp read power data to graph

    for fet_params in uut_params:
        (subuut, fet_nfin) = fet_params
        if "hp" in subuut:
            continue
        with open(cwd + "/" + uut_setup.uut + "/" + subuut + ".sp", 'w+') as spice_file:
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
            sim_time = "1"        # str(2 ** parallel_instances) # simulataion time in ns
            bl_capacitance = cap_dict[subuut]        # str(2 ** parallel_instances) # simulataion time in ns
            data = 1
            sim_params = (sim_type, sim_tinc, sim_time, bl_capacitance, data)

            # invokes subckts class
            subckts_modules = lstp_cam(script_params, grid_params, fet_params, sim_params)

            # set .sp header and calls library
            subckts_modules.set_library()

            spice_file.write("$ UUT individual unit\n")
            subckts_modules.set_cells_subckts()

            spice_file.write("$ Sources\n")
            spice_file.write("vdd vdd gnd vdd\n")
            subckts_modules.write_source()
 
            spice_file.write("$ Unit Under Test\n")
            subckts_modules.write_uut()

            spice_file.write("$ Measurements\n")
            subckts_modules.measure_power()
            subckts_modules.measure_delays()

            spice_file.write("$ Simulation/Analysis Type\n")
            subckts_modules.analysis_type()

        # run hspice
        subckts_modules.run_hspice()

        # collect all series
        (power_series, delay_series) = subckts_modules.collect_data()

        # collects delay values and calculates delay average
        write_delay = list(subckts_modules.clean_data(0, 2, delay_series).values())[-1]
        read_delay = list(subckts_modules.clean_data(1, 2, delay_series).values())[-1]

        if "hp" in subuut:
            ptm_sizes.append(int(subuut.replace("ptm","").replace("hp","")))
            hp_write_delay.append(write_delay * 1e12)
            hp_read_delay.append(read_delay * 1e12)
            write_hp_power.append(power_series[6][1] * 1e9)
            hold_hp_power.append(power_series[7][1] * 1e9)
            read_hp_power.append(power_series[8][1] * 1e9)

        if "lstp" in subuut:
            ptm_sizes.append(int(subuut.replace("ptm","").replace("lstp","")))
            lstp_write_delay.append(write_delay * 1e12)
            lstp_read_delay.append(read_delay * 1e12)
            write_lstp_power.append(power_series[6][1] * 1e9)
            hold_lstp_power.append(power_series[7][1] * 1e9)
            read_lstp_power.append(power_series[8][1] * 1e9)

    hp_data = (ptm_sizes, hp_write_delay, hp_read_delay, write_hp_power, hold_hp_power, read_hp_power)
    lstp_data = (ptm_sizes, lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, read_lstp_power)

    return (hp_data, lstp_data)
