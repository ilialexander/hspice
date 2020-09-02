$This UUT was automatically generated by:
$/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/inverter_script.py

$Netlist of test
.lib '../models' ptm16lstp

.subckt input_0 inb_0 in_0 vdd
xpfetin_0 in_0 inb_0 vdd vdd pfet l=16n nfin=1000m
xnfetin_0 in_0 inb_0 gnd gnd nfet l=16n nfin=1000m
.ends

xinput_0 inb_0 in_0 vdd input_0
.subckt test0 in_0 out_0 vdd
$FETs
xpfet_0 out_0 in_0 vdd vdd pfet l=16n nfin=1000m
xnfet_0 out_0 in_0 gnd gnd nfet l=16n nfin=1000m
.ends

xtest0 in_0 out_0 vdd test0
$Output Load
.subckt output_0 out_0 outb_0 vdd
xpfetout_0 outb_0 out_0 vdd vdd pfet l=16n nfin=1000m
xnfetout_0 outb_0 out_0 gnd gnd nfet l=16n nfin=1000m
.ends

xoutput_0 out_0 outb_0 vdd output_0
$Dummy Load
c1 outb_0 gnd 5f

$Power Sources
vdd vdd  gnd 0.85V
vin inb_0 gnd  PULSE(0V 0.85V 0ns 50ps 50ps 1ns 2ns)

.option post=2

$Analysis
.tran 10ps 4ns

.print TRAN V(in_0) V(out_0)
.measure tran power_avg avg power
.measure tran avg_power avg p(vin) from=0ns to=4ns
.measure tran inv_avg_power avg p(xtest0) from=0ns to=4ns
.measure tran peakpower max p(xtest0)
.measure tran trf_delay_1 trig v(in_0) val=0.425 rise=1 targ v(out_0) val=0.425 fall=1

.measure tran tfr_delay_1 trig v(in_0) val=0.425 fall=1 targ v(out_0) val=0.425 rise=1

.measure tran trf_delay_2 trig v(in_0) val=0.425 rise=2 targ v(out_0) val=0.425 fall=2

.measure tran tfr_delay_2 trig v(in_0) val=0.425 fall=2 targ v(out_0) val=0.425 rise=2

.end