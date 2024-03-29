#!/usr/bin/env python
import os
import csv
import matplotlib.pyplot as plt
from lstp_cam_script import lstp_cam_script
from match_cam_script import match_cam_script

(hp_data, lstp_data) = lstp_cam_script()
(ptm_sizes, lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, read_lstp_power) = lstp_data

(hp_data, lstp_data) = match_cam_script()
(_1, lstp_match_delay, _3, _4, match_lstp_power) = lstp_data

operations = ["Write","Read","Match","Hold"]

ptm_sizes.insert(0, ptm_sizes.pop())

write_lstp_power.insert(0, write_lstp_power.pop())
read_lstp_power.insert(0, read_lstp_power.pop())
match_lstp_power.insert(0, match_lstp_power.pop())
hold_lstp_power.insert(0, hold_lstp_power.pop())

lstp_write_delay.insert(0, lstp_write_delay.pop())
lstp_read_delay.insert(0, lstp_read_delay.pop())
lstp_match_delay.insert(0, lstp_match_delay.pop())

with open('power_results.csv', mode='w') as power_results:
    power_writer = csv.writer(power_results, delimiter = ',') 
    power_writer.writerow(operations) 
    for power in range(5):
        power_writer.writerow([write_lstp_power[power], read_lstp_power[power], match_lstp_power[power], hold_lstp_power[power]]) 

with open('delay_results.csv', mode='w') as delay_results:
    delay_writer = csv.writer(delay_results, delimiter = ',') 
    delay_writer.writerow(operations[:-1]) # Does not need Hold operation
    for delay in range(5):
        delay_writer.writerow([lstp_write_delay[delay], lstp_read_delay[delay], lstp_match_delay[delay]]) 

# Graphing delays and power
plt.figure(1)
plt.title("Average Write Power by FET Size")
plt.scatter(ptm_sizes, write_lstp_power, color = "blue", label = "LSTP Write")
plt.scatter(ptm_sizes, read_lstp_power, color = "cyan", label = "LSTP Read")
plt.scatter(ptm_sizes, match_lstp_power, color = "green", label = "LSTP Match")
plt.scatter(ptm_sizes, hold_lstp_power, color = "black", label = "LSTP Hold")
plt.xlabel("Width (nm)")
plt.ylabel("Power (nw)")
plt.grid()
plt.legend()

plt.figure(2)
plt.title("FETs' Average Delays for \nHigh Performance (HP) and Low Standby Power (LSTP)")
plt.scatter(ptm_sizes, lstp_write_delay, color = "blue", label = "LSTP Write")
plt.scatter(ptm_sizes, lstp_read_delay, color = "cyan", marker = "D", label = "LSTP Read")
plt.scatter(ptm_sizes, lstp_match_delay, color = "green", marker = "s", label = "LSTP Match")
plt.xlabel("Width (nm)")
plt.ylabel("Delay (ps)")
plt.legend()
plt.grid()

plt.show()
