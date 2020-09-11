$This UUT was automatically generated by:
$/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/inverter_script.py

$Netlist of test
.lib '../models' ptm7hp

$Power Sources
vdd vdd  gnd 0.7V
vin_0 inb_0 gnd  PULSE(0.7V 0V 0ns 50ps 50ps 1.0n 2n)

.subckt input_0 inb_0 in_0 vdd
xpfetin_0 in_0 inb_0 vdd vdd pfet l=7n nfin=1000m
xnfetin_0 in_0 inb_0 gnd gnd nfet l=7n nfin=1000m
.ends
xinput_0 inb_0 in_0 vdd input_0

.subckt inverter0 in_0 out_0 vdd
$FETs
xpfet_0 out_0 in_0 vdd vdd pfet l=7n nfin=1000m
xnfet_0 out_0 in_0 gnd gnd nfet l=7n nfin=1000m
.ends
xinverter0 in_0 out_0 vdd inverter0

$Output Load
.subckt output_00 out_0 outb_00 vdd
xpfetout_0 outb_00 out_0 vdd vdd pfet l=7n nfin=1000m
xnfetout_0 outb_00 out_0 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_00 out_0 outb_00 vdd output_00

$Output Load
.subckt output_01 out_0 outb_01 vdd
xpfetout_0 outb_01 out_0 vdd vdd pfet l=7n nfin=1000m
xnfetout_0 outb_01 out_0 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_01 out_0 outb_01 vdd output_01

.print TRAN V(in_0) V(out_0)
.measure tran inv_avg_power0 avg p(xinverter0) from=0ns to=8ns
.measure tran peakpower0 max p(xinverter0)
.measure tran trf_delay_01 trig v(in_0) val=0.35 rise=1 targ v(out_0) val=0.35 fall=1
.measure tran tfr_delay_01 trig v(in_0) val=0.35 fall=1 targ v(out_0) val=0.35 rise=1
.measure tran trf_delay_02 trig v(in_0) val=0.35 rise=2 targ v(out_0) val=0.35 fall=2
.measure tran tfr_delay_02 trig v(in_0) val=0.35 fall=2 targ v(out_0) val=0.35 rise=2
.measure tran trf_delay_03 trig v(in_0) val=0.35 rise=3 targ v(out_0) val=0.35 fall=3
.measure tran tfr_delay_03 trig v(in_0) val=0.35 fall=3 targ v(out_0) val=0.35 rise=3
.measure tran trf_delay_04 trig v(in_0) val=0.35 rise=4 targ v(out_0) val=0.35 fall=4
.measure tran tfr_delay_04 trig v(in_0) val=0.35 fall=4 targ v(out_0) val=0.35 rise=4
vin_1 inb_1 gnd  PULSE(0.7V 0V 0ns 50ps 50ps 2.0n 4n)

.subckt input_1 inb_1 in_1 vdd
xpfetin_1 in_1 inb_1 vdd vdd pfet l=7n nfin=1000m
xnfetin_1 in_1 inb_1 gnd gnd nfet l=7n nfin=1000m
.ends
xinput_1 inb_1 in_1 vdd input_1

.subckt inverter1 in_1 out_1 vdd
$FETs
xpfet_1 out_1 in_1 vdd vdd pfet l=7n nfin=1000m
xnfet_1 out_1 in_1 gnd gnd nfet l=7n nfin=1000m
.ends
xinverter1 in_1 out_1 vdd inverter1

$Output Load
.subckt output_10 out_1 outb_10 vdd
xpfetout_1 outb_10 out_1 vdd vdd pfet l=7n nfin=1000m
xnfetout_1 outb_10 out_1 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_10 out_1 outb_10 vdd output_10

$Output Load
.subckt output_11 out_1 outb_11 vdd
xpfetout_1 outb_11 out_1 vdd vdd pfet l=7n nfin=1000m
xnfetout_1 outb_11 out_1 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_11 out_1 outb_11 vdd output_11

.print TRAN V(in_1) V(out_1)
.measure tran inv_avg_power1 avg p(xinverter1) from=0ns to=8ns
.measure tran peakpower1 max p(xinverter1)
.measure tran trf_delay_11 trig v(in_1) val=0.35 rise=1 targ v(out_1) val=0.35 fall=1
.measure tran tfr_delay_11 trig v(in_1) val=0.35 fall=1 targ v(out_1) val=0.35 rise=1
.measure tran trf_delay_12 trig v(in_1) val=0.35 rise=2 targ v(out_1) val=0.35 fall=2
.measure tran tfr_delay_12 trig v(in_1) val=0.35 fall=2 targ v(out_1) val=0.35 rise=2
vin_2 inb_2 gnd  PULSE(0.7V 0V 0ns 50ps 50ps 4.0n 8n)

.subckt input_2 inb_2 in_2 vdd
xpfetin_2 in_2 inb_2 vdd vdd pfet l=7n nfin=1000m
xnfetin_2 in_2 inb_2 gnd gnd nfet l=7n nfin=1000m
.ends
xinput_2 inb_2 in_2 vdd input_2

.subckt inverter2 in_2 out_2 vdd
$FETs
xpfet_2 out_2 in_2 vdd vdd pfet l=7n nfin=1000m
xnfet_2 out_2 in_2 gnd gnd nfet l=7n nfin=1000m
.ends
xinverter2 in_2 out_2 vdd inverter2

$Output Load
.subckt output_20 out_2 outb_20 vdd
xpfetout_2 outb_20 out_2 vdd vdd pfet l=7n nfin=1000m
xnfetout_2 outb_20 out_2 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_20 out_2 outb_20 vdd output_20

$Output Load
.subckt output_21 out_2 outb_21 vdd
xpfetout_2 outb_21 out_2 vdd vdd pfet l=7n nfin=1000m
xnfetout_2 outb_21 out_2 gnd gnd nfet l=7n nfin=1000m
.ends
xoutput_21 out_2 outb_21 vdd output_21

.print TRAN V(in_2) V(out_2)
.measure tran inv_avg_power2 avg p(xinverter2) from=0ns to=8ns
.measure tran peakpower2 max p(xinverter2)
.measure tran trf_delay_21 trig v(in_2) val=0.35 rise=1 targ v(out_2) val=0.35 fall=1
.measure tran tfr_delay_21 trig v(in_2) val=0.35 fall=1 targ v(out_2) val=0.35 rise=1
.option post=2

$Analysis
.tran 10ps 8ns

.measure tran power_avg avg power
.measure tran avg_power avg p(vdd) from=0ns to=8ns
.end