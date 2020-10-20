$ Netlist of sram
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/sram_script.py
.lib '../models' ptm14lstp
.param vdd_50='vdd/2'
$ UUT individual unit
.subckt inverter in out vdd
$fets
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

.subckt sram wl bl blb vdd
xnfet_bl  bl  wl q  q  nfet l=lg nfin=1000m
xnfet_blb blb wl qb qb nfet l=lg nfin=1000m
xq  qb q  vdd inverter
xqb q  qb vdd inverter
.ends
$ Sources
vdd vdd gnd vdd
$Sources
vin_wl_0 in_wl_0  gnd  pulse(vdd 0v 0.25ns 1p 1p 0.5n 1.0n)
xwl_0 in_wl_0 wl_0 vdd inverter
vin_blb_0 in_blb_0  gnd  pulse(vdd 0v 0ns 1p 1p 0.5n 1.0n)
xblb_0 in_blb_0 blb_0 vdd inverter
xbl_0 gnd bl_0 vdd inverter

$ Unit Under Test
xsram00 wl_0 bl_0 blb_0 vdd sram
$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 2n

.end