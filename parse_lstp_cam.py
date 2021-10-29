#!/usr/bin/env python
import os
import csv
import matplotlib.pyplot as plt
from hp_cam_script import hp_cam_script
from lstp_cam_script import lstp_cam_script
from match_cam_script import match_cam_script

#(hp_data, lstp_data) = hp_cam_script()
#(ptm_sizes, hp_write_delay, hp_read_delay, write_hp_power, hold_hp_power, read_hp_power) = hp_data
#(lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, read_lstp_power) = lstp_data

(hp_data, lstp_data) = lstp_cam_script()
(ptm_sizes, lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, read_lstp_power) = lstp_data

#(hp_data, lstp_data) = match_cam_script()
#(_1, _2, hp_match_delay, _3, _4, match_hp_power) = hp_data
#(_1, lstp_match_delay, _3, _4, match_lstp_power) = lstp_data

# removes 7 and 10 nm data
#ptm_sizes.pop(4)
#hp_write_delay.pop(4)
#hp_read_delay.pop(4)
#write_hp_power.pop(4)
#hold_hp_power.pop(4)
#read_hp_power.pop(4)
#
#lstp_write_delay.pop(4)
#lstp_read_delay.pop(4)
#write_lstp_power.pop(4)
#hold_lstp_power.pop(4)
#read_lstp_power.pop(4)
# 
##hp_match_delay.pop(4)
##match_hp_power.pop(4)
##
##lstp_match_delay.pop(4)
##match_lstp_power.pop(4)
#
#ptm_sizes.pop(1)
#hp_write_delay.pop(1)
#hp_read_delay.pop(1)
#write_hp_power.pop(1)
#hold_hp_power.pop(1)
#read_hp_power.pop(1)
#
#lstp_write_delay.pop(0)
#lstp_read_delay.pop(0)
#write_lstp_power.pop(0)
#hold_lstp_power.pop(0)
#read_lstp_power.pop(0)
# 
#hp_match_delay.pop(1)
#match_hp_power.pop(1)
#
#lstp_match_delay.pop(1)
#match_lstp_power.pop(1)

with open('power_results.csv', mode='w') as power_results:
    power_writer = csv.writer(power_results, delimiter = ',') 
    power_writer.writerow(write_lstp_power) 
    power_writer.writerow(read_lstp_power) 
#    power_writer.writerow(match_lstp_power) 
    power_writer.writerow(hold_lstp_power) 
#    power_writer.writerow(write_hp_power) 
#    power_writer.writerow(read_hp_power) 
#    power_writer.writerow(match_hp_power) 
#    power_writer.writerow(hold_hp_power)

with open('delay_results.csv', mode='w') as delay_results:
    delay_writer = csv.writer(delay_results, delimiter = ',') 
    delay_writer.writerow(lstp_write_delay) 
    delay_writer.writerow(lstp_read_delay)
#    delay_writer.writerow(lstp_match_delay)
#    delay_writer.writerow(hp_write_delay)
#    delay_writer.writerow(hp_read_delay)
#    delay_writer.writerow(hp_match_delay)

# Graphing delays and power

plt.figure(1)
plt.title("Average Write Power by FET Size")
plt.scatter(ptm_sizes, write_lstp_power, color = "blue", label = "LSTP Write")
plt.scatter(ptm_sizes, read_lstp_power, color = "cyan", label = "LSTP Read")
#plt.scatter(ptm_sizes, match_lstp_power, color = "green", label = "LSTP Match")
plt.scatter(ptm_sizes, hold_lstp_power, color = "black", label = "LSTP Hold")
#plt.scatter(ptm_sizes, write_hp_power, color = "red", label = "HP Write")
#plt.scatter(ptm_sizes, read_hp_power, color = "magenta", label = "HP Read")
#plt.scatter(ptm_sizes, match_hp_power, color = "lime", label = "HP Match")
#plt.scatter(ptm_sizes, hold_hp_power, color = "dimgray", label = "HP Hold")
plt.xlabel("Width (nm)")
plt.ylabel("Power (nw)")
plt.grid()
plt.legend()

plt.figure(2)
plt.title("FETs' Average Delays for \nHigh Performance (HP) and Low Standby Power (LSTP)")
plt.scatter(ptm_sizes, lstp_write_delay, color = "blue", label = "LSTP Write")
plt.scatter(ptm_sizes, lstp_read_delay, color = "cyan", marker = "D", label = "LSTP Read")
#plt.scatter(ptm_sizes, lstp_match_delay, color = "green", marker = "s", label = "LSTP Match")
#plt.scatter(ptm_sizes, hp_write_delay, color = "red", marker = "v", label = "HP Write")
#plt.scatter(ptm_sizes, hp_read_delay, color = "magenta", marker = "*", label = "HP Read")
#plt.scatter(ptm_sizes, hp_match_delay, color = "lime", marker = "x", label = "HP Match")
plt.xlabel("Width (nm)")
plt.ylabel("Delay (ps)")
plt.legend()
plt.grid()

plt.show()
