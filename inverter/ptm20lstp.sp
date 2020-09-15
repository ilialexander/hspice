$ Netlist of inverter
$ This UUT was automatically generated by:
$ /work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/hspice_script.py
.lib '../models' ptm20lstp
$ UUT individual unit
.subckt inverter in out vdd
$fets
xpfet out in vdd vdd pfet l=20n nfin=1000m
xnfet out in gnd gnd nfet l=20n nfin=1000m
.ends

$ Sources
vdd vdd  gnd 0.9V
$all input sources
vin_0 inb_0 gnd  PULSE(0.9V 0V 0ns 50ps 50ps 1.0n 2n)
vin_1 inb_1 gnd  PULSE(0.9V 0V 0ns 50ps 50ps 2.0n 4n)
$invert input sources
xinput_0 inb_0 outin_00 vdd inverter
xinput_1 inb_1 outin_01 vdd inverter

$ Unit Under Test
.subckt model_uut_grid vdd
+outin_00 outin_01 $inputs to model_uut_grid Subckt
+outin_10 outin_20 outin_11 outin_21 $outputs to model_uut_grid Subckt
xinverter00 outin_00 outin_10 vdd inverter
xinverter10 outin_10 outin_20 vdd inverter
xinverter01 outin_01 outin_11 vdd inverter
xinverter11 outin_11 outin_21 vdd inverter
.ends
$invoke UUT grid
xmodel_uut_grid vdd
+outin_00 outin_01 $inputs to model_uut_grid
+outin_10 outin_20 outin_11 outin_21 $outputs to model_uut_grid
+model_uut_grid

$ Output Loads
xoutput_00 outin_20 outb_00 vdd inverter
xoutput_10 outin_21 outb_10 vdd inverter

$ Measurements
.measure tran model_uut_peak_power00 max p(xmodel_uut_grid.xinverter00)
.measure tran model_uut_avg_power00 avg p(xmodel_uut_grid.xinverter00)
.measure tran model_uut_peak_power10 max p(xmodel_uut_grid.xinverter10)
.measure tran model_uut_avg_power10 avg p(xmodel_uut_grid.xinverter10)
.measure tran model_uut_peak_power01 max p(xmodel_uut_grid.xinverter01)
.measure tran model_uut_avg_power01 avg p(xmodel_uut_grid.xinverter01)
.measure tran model_uut_peak_power11 max p(xmodel_uut_grid.xinverter11)
.measure tran model_uut_avg_power11 avg p(xmodel_uut_grid.xinverter11)
.measure tran uut_peak_power max p(xmodel_uut_grid)
.measure tran uut_avg_power avg p(xmodel_uut_grid)
.measure tran source_peak_power max power
.measure tran source_avg_power avg power
.measure tran trf_delay_001 trig v(outin_00) val=0.45 rise=1 targ v(outin_10) val=0.45 fall=1
.measure tran tfr_delay_001 trig v(outin_00) val=0.45 fall=1 targ v(outin_10) val=0.45 rise=1
.measure tran trf_delay_002 trig v(outin_00) val=0.45 rise=2 targ v(outin_10) val=0.45 fall=2
.measure tran tfr_delay_002 trig v(outin_00) val=0.45 fall=2 targ v(outin_10) val=0.45 rise=2
.measure tran trf_delay_101 trig v(outin_10) val=0.45 rise=1 targ v(outin_20) val=0.45 fall=1
.measure tran tfr_delay_101 trig v(outin_10) val=0.45 fall=1 targ v(outin_20) val=0.45 rise=1
.measure tran trf_delay_102 trig v(outin_10) val=0.45 rise=2 targ v(outin_20) val=0.45 fall=2
.measure tran tfr_delay_102 trig v(outin_10) val=0.45 fall=2 targ v(outin_20) val=0.45 rise=2
.measure tran trf_delay_011 trig v(outin_01) val=0.45 rise=1 targ v(outin_11) val=0.45 fall=1
.measure tran tfr_delay_011 trig v(outin_01) val=0.45 fall=1 targ v(outin_11) val=0.45 rise=1
.measure tran trf_delay_111 trig v(outin_11) val=0.45 rise=1 targ v(outin_21) val=0.45 fall=1
.measure tran tfr_delay_111 trig v(outin_11) val=0.45 fall=1 targ v(outin_21) val=0.45 rise=1
.print TRAN V(outin_00) V(outin_10)
.print TRAN V(outin_10) V(outin_20)
.print TRAN V(outin_01) V(outin_11)
.print TRAN V(outin_11) V(outin_21)

$ Simulation/Analysis Type
.option post=2
.tran 10p 4ns

.end