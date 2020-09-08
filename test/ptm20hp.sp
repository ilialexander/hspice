$This UUT was automatically generated by:
$/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/inverter_script.py

$Netlist of test
.lib '../models' ptm20hp

vin_0 inb_0 gnd  PULSE(0V 0.9V 0ns 50ps 50ps 1.0n 2n)

.subckt input_0 inb_0 in_0 vdd
xpfetin_0 in_0 inb_0 vdd vdd pfet l=20n nfin=1000m
xnfetin_0 in_0 inb_0 gnd gnd nfet l=20n nfin=1000m
.ends
xinput_0 inb_0 in_0 vdd input_0

.subckt inverter0 in_0 out_0 vdd
$FETs
xpfet_0 out_0 in_0 vdd vdd pfet l=20n nfin=1000m
xnfet_0 out_0 in_0 gnd gnd nfet l=20n nfin=1000m
.ends
xinverter0 in_0 out_0 vdd inverter0

$Output Load
.subckt output_00 out_0 outb_00 vdd
xpfetout_0 outb_00 out_0 vdd vdd pfet l=20n nfin=1000m
xnfetout_0 outb_00 out_0 gnd gnd nfet l=20n nfin=1000m
.ends
xoutput_00 out_0 outb_00 vdd output_00

$Output Load
.subckt output_01 out_0 outb_01 vdd
xpfetout_0 outb_01 out_0 vdd vdd pfet l=20n nfin=1000m
xnfetout_0 outb_01 out_0 gnd gnd nfet l=20n nfin=1000m
.ends
xoutput_01 out_0 outb_01 vdd output_01

$Output Load
.subckt output_02 out_0 outb_02 vdd
xpfetout_0 outb_02 out_0 vdd vdd pfet l=20n nfin=1000m
xnfetout_0 outb_02 out_0 gnd gnd nfet l=20n nfin=1000m
.ends
xoutput_02 out_0 outb_02 vdd output_02

$Output Load
.subckt output_03 out_0 outb_03 vdd
xpfetout_0 outb_03 out_0 vdd vdd pfet l=20n nfin=1000m
xnfetout_0 outb_03 out_0 gnd gnd nfet l=20n nfin=1000m
.ends
xoutput_03 out_0 outb_03 vdd output_03

$Power Sources
vdd vdd  gnd 0.9V
.option post=2

$Analysis
.tran 10ps 8ns

.print TRAN V(in_0) V(out_0)
.measure tran power_avg avg power
.measure tran avg_power avg p(vdd) from=0ns to=4ns
.measure tran inv_avg_power avg p(xinverter0) from=0ns to=4ns
.measure tran peakpower max p(xinverter0)
.measure tran trf_delay_1 trig v(in_0) val=0.45 rise=1 targ v(out_0) val=0.45 fall=1

.measure tran tfr_delay_1 trig v(in_0) val=0.45 fall=1 targ v(out_0) val=0.45 rise=1

.measure tran trf_delay_2 trig v(in_0) val=0.45 rise=2 targ v(out_0) val=0.45 fall=2

.measure tran tfr_delay_2 trig v(in_0) val=0.45 fall=2 targ v(out_0) val=0.45 rise=2

.end