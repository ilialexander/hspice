$ Netlist of inverter
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/hspice_script.py
.lib '../models' ptm16hp
.param vdd_50='vdd/2'
$ UUT individual unit
.subckt inverter in out vdd
$fets
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

$ Sources
vdd vdd gnd vdd
$all input sources
vin_0 inb_0 gnd  PULSE(vdd 0V 0ns 1p 1p 1.0n 2n)
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
xoutput_000 outb_00 outb_000 vdd inverter
xoutput_0000 outb_000 outb_0000 vdd inverter
xoutput_0001 outb_000 outb_0001 vdd inverter
xoutput_0002 outb_000 outb_0002 vdd inverter
xoutput_0003 outb_000 outb_0003 vdd inverter
xoutput_001 outb_00 outb_001 vdd inverter
xoutput_0010 outb_001 outb_0010 vdd inverter
xoutput_0011 outb_001 outb_0011 vdd inverter
xoutput_0012 outb_001 outb_0012 vdd inverter
xoutput_0013 outb_001 outb_0013 vdd inverter
xoutput_002 outb_00 outb_002 vdd inverter
xoutput_0020 outb_002 outb_0020 vdd inverter
xoutput_0021 outb_002 outb_0021 vdd inverter
xoutput_0022 outb_002 outb_0022 vdd inverter
xoutput_0023 outb_002 outb_0023 vdd inverter
xoutput_003 outb_00 outb_003 vdd inverter
xoutput_0030 outb_003 outb_0030 vdd inverter
xoutput_0031 outb_003 outb_0031 vdd inverter
xoutput_0032 outb_003 outb_0032 vdd inverter
xoutput_0033 outb_003 outb_0033 vdd inverter
xoutput_01 outin_10 outb_01 vdd inverter
xoutput_010 outb_01 outb_010 vdd inverter
xoutput_0100 outb_010 outb_0100 vdd inverter
xoutput_0101 outb_010 outb_0101 vdd inverter
xoutput_0102 outb_010 outb_0102 vdd inverter
xoutput_0103 outb_010 outb_0103 vdd inverter
xoutput_011 outb_01 outb_011 vdd inverter
xoutput_0110 outb_011 outb_0110 vdd inverter
xoutput_0111 outb_011 outb_0111 vdd inverter
xoutput_0112 outb_011 outb_0112 vdd inverter
xoutput_0113 outb_011 outb_0113 vdd inverter
xoutput_012 outb_01 outb_012 vdd inverter
xoutput_0120 outb_012 outb_0120 vdd inverter
xoutput_0121 outb_012 outb_0121 vdd inverter
xoutput_0122 outb_012 outb_0122 vdd inverter
xoutput_0123 outb_012 outb_0123 vdd inverter
xoutput_013 outb_01 outb_013 vdd inverter
xoutput_0130 outb_013 outb_0130 vdd inverter
xoutput_0131 outb_013 outb_0131 vdd inverter
xoutput_0132 outb_013 outb_0132 vdd inverter
xoutput_0133 outb_013 outb_0133 vdd inverter
xoutput_02 outin_10 outb_02 vdd inverter
xoutput_020 outb_02 outb_020 vdd inverter
xoutput_0200 outb_020 outb_0200 vdd inverter
xoutput_0201 outb_020 outb_0201 vdd inverter
xoutput_0202 outb_020 outb_0202 vdd inverter
xoutput_0203 outb_020 outb_0203 vdd inverter
xoutput_021 outb_02 outb_021 vdd inverter
xoutput_0210 outb_021 outb_0210 vdd inverter
xoutput_0211 outb_021 outb_0211 vdd inverter
xoutput_0212 outb_021 outb_0212 vdd inverter
xoutput_0213 outb_021 outb_0213 vdd inverter
xoutput_022 outb_02 outb_022 vdd inverter
xoutput_0220 outb_022 outb_0220 vdd inverter
xoutput_0221 outb_022 outb_0221 vdd inverter
xoutput_0222 outb_022 outb_0222 vdd inverter
xoutput_0223 outb_022 outb_0223 vdd inverter
xoutput_023 outb_02 outb_023 vdd inverter
xoutput_0230 outb_023 outb_0230 vdd inverter
xoutput_0231 outb_023 outb_0231 vdd inverter
xoutput_0232 outb_023 outb_0232 vdd inverter
xoutput_0233 outb_023 outb_0233 vdd inverter
xoutput_03 outin_10 outb_03 vdd inverter
xoutput_030 outb_03 outb_030 vdd inverter
xoutput_0300 outb_030 outb_0300 vdd inverter
xoutput_0301 outb_030 outb_0301 vdd inverter
xoutput_0302 outb_030 outb_0302 vdd inverter
xoutput_0303 outb_030 outb_0303 vdd inverter
xoutput_031 outb_03 outb_031 vdd inverter
xoutput_0310 outb_031 outb_0310 vdd inverter
xoutput_0311 outb_031 outb_0311 vdd inverter
xoutput_0312 outb_031 outb_0312 vdd inverter
xoutput_0313 outb_031 outb_0313 vdd inverter
xoutput_032 outb_03 outb_032 vdd inverter
xoutput_0320 outb_032 outb_0320 vdd inverter
xoutput_0321 outb_032 outb_0321 vdd inverter
xoutput_0322 outb_032 outb_0322 vdd inverter
xoutput_0323 outb_032 outb_0323 vdd inverter
xoutput_033 outb_03 outb_033 vdd inverter
xoutput_0330 outb_033 outb_0330 vdd inverter
xoutput_0331 outb_033 outb_0331 vdd inverter
xoutput_0332 outb_033 outb_0332 vdd inverter
xoutput_0333 outb_033 outb_0333 vdd inverter

$ Measurements
.measure tran model_uut_peak_power00 max p(xoutput_012)
.measure tran model_uut_avg_power00 avg p(xoutput_012)
.measure tran uut_peak_power max p(xmodel_uut_grid)
.measure tran uut_avg_power avg p(xmodel_uut_grid)
.measure tran source_peak_power max power
.measure tran source_avg_power avg power
.measure tran trf_delay trig v(outb_01) val=vdd_50 rise=1 targ v(outb_012) val=vdd_50 fall=1
.measure tran tfr_delay trig v(outb_01) val=vdd_50 fall=1 targ v(outb_012) val=vdd_50 rise=1
.print TRAN V(outin_00) V(outin_10)

$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 2ns

.end