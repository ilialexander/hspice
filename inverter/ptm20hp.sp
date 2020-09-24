$ Netlist of inverter
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/hspice_script.py
.lib '../models' ptm20hp
$ UUT individual unit
.subckt inverter in out vdd
$fets
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

$ Sources
vdd vdd  gnd vdd
$all input sources
vin_0 inb_0 gnd  PULSE(vdd 0V 0ns 1ps 1ps 1.0n 2n)
$invert input sources
xinput_0 inb_0 outin_00 vdd inverter

$ Unit Under Test
.subckt model_uut_grid vdd
+outin_00 $inputs to model_uut_grid Subckt
+outin_10 $outputs to model_uut_grid Subckt
xinverter00 outin_00 outin_10 vdd inverter
.ends
$invoke UUT grid
xmodel_uut_grid vdd
+outin_00 $inputs to model_uut_grid
+outin_10 $outputs to model_uut_grid
+model_uut_grid

$ Output Loads
xoutput_00 outin_10 outb_00 vdd inverter
xoutput_01 outin_10 outb_01 vdd inverter
xoutput_02 outin_10 outb_02 vdd inverter
xoutput_03 outin_10 outb_03 vdd inverter

$ Measurements
.measure tran model_uut_peak_power00 max p(xmodel_uut_grid.xinverter00)
.measure tran model_uut_avg_power00 avg p(xmodel_uut_grid.xinverter00)
.measure tran uut_peak_power max p(xmodel_uut_grid)
.measure tran uut_avg_power avg p(xmodel_uut_grid)
.measure tran source_peak_power max power
.measure tran source_avg_power avg power
.measure tran trf_delay_001 trig v(outin_00) val=0.45 rise=1 targ v(outin_10) val=0.45 fall=1
.measure tran tfr_delay_001 trig v(outin_00) val=0.45 fall=1 targ v(outin_10) val=0.45 rise=1
.print TRAN V(outin_00) V(outin_10)

$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 2ns

.end