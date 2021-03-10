#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from hp_cam_script import hp_cam_script
from lstp_cam_script import lstp_cam_script
from match_cam_script import match_cam_script

(hp_data, lstp_data) = hp_cam_script()
(ptm_sizes, hp_write_delay, hp_read_delay, write_hp_power, hold_hp_power, read_hp_power) = hp_data
(lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, read_lstp_power) = lstp_data

(hp_data, lstp_data) = lstp_cam_script()
(lstp_write_delay, lstp_read_delay, write_lstp_power, hold_lstp_power, _) = lstp_data

(hp_data, lstp_data) = match_cam_script()
(_1, _2, hp_match_delay, _3, _4, match_hp_power) = hp_data
(_1, lstp_match_delay, _2, _3, match_lstp_power) = lstp_data


# removes 7 and 10 nm data
ptm_sizes.pop(4)
hp_write_delay.pop(4)
hp_read_delay.pop(4)
write_hp_power.pop(4)
hold_hp_power.pop(4)
read_hp_power.pop(4)

lstp_write_delay.pop(4)
lstp_read_delay.pop(4)
write_lstp_power.pop(4)
hold_lstp_power.pop(4)
read_lstp_power.pop(4)
 
#hp_match_delay.pop(4)
#match_hp_power.pop(4)
#
#lstp_match_delay.pop(4)
#match_lstp_power.pop(4)

ptm_sizes.pop(1)
hp_write_delay.pop(1)
hp_read_delay.pop(1)
write_hp_power.pop(1)
hold_hp_power.pop(1)
read_hp_power.pop(1)

lstp_write_delay.pop(1)
lstp_read_delay.pop(1)
write_lstp_power.pop(1)
hold_lstp_power.pop(1)
read_lstp_power.pop(1)
 
hp_match_delay.pop(1)
match_hp_power.pop(1)

lstp_match_delay.pop(1)
match_lstp_power.pop(1)

# Graphing delays and power
plt.figure(1)
plt.title("Average Write Power by FET Size")
plt.scatter(ptm_sizes, write_hp_power, color = "red", label = "High Performance")
plt.scatter(ptm_sizes, write_lstp_power, color = "blue", label = "Low Standby Power")
plt.xlabel("Width (nm)")
plt.ylabel("Power (nw)")
plt.legend()

plt.figure(2)
plt.title("Average Read Power by FET Size")
plt.scatter(ptm_sizes, read_hp_power, color = "red", label = "High Performance")
plt.scatter(ptm_sizes, read_lstp_power, color = "blue", label = "Low Standby Power")
plt.xlabel("Width (nm")
plt.ylabel("Power (nw)")
plt.legend()

plt.figure(3)
plt.title("Average Match Power by FET Size")
plt.scatter(ptm_sizes, match_hp_power, color = "red", label = "High Performance")
plt.scatter(ptm_sizes, match_lstp_power, color = "blue", label = "Low Standby Power")
plt.xlabel("Width (nm")
plt.ylabel("Power (nw)")
plt.legend()

plt.figure(4)
plt.title("Average Hold Power by FET Size")
plt.scatter(ptm_sizes, hold_hp_power, color = "red", label = "High Performance")
plt.scatter(ptm_sizes, hold_lstp_power, color = "blue", label = "Low Standby Power")
plt.xlabel("Width (nm)")
plt.ylabel("Power (nw)")
plt.legend()

plt.figure(5)
plt.title("Average Delay by FET size for \nHigh Performance ('red') and Low Standby Power ('blue')")
plt.scatter(ptm_sizes, lstp_write_delay, color = "blue", label = "LSTP Write")
plt.scatter(ptm_sizes, lstp_read_delay, color = "green", label = "LSTP Read")
plt.scatter(ptm_sizes, hp_write_delay, color = "red", label = "HP Write")
plt.scatter(ptm_sizes, hp_read_delay, color = "black", label = "HP Read")
plt.scatter(ptm_sizes, lstp_match_delay, color = "magenta", label = "LSTP Match")
plt.scatter(ptm_sizes, hp_match_delay, color = "cyan", label = "HP Match")
plt.xlabel("Width (nm)")
plt.ylabel("Delay (ps)")
plt.legend()

plt.show()
