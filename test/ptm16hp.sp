$This UUT was automatically generated by:
$/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/inverter_script.py
$Netlist of test
.lib '../models' ptm16hp

$Sources
vdd vdd  gnd 0.85V
vin_0 inb_0 gnd  PULSE(0.85V 0V 0ns 50ps 50ps 1.0n 2n)
xinput_0 inb_0 outin_00 vdd inverter
vin_1 inb_1 gnd  PULSE(0.85V 0V 0ns 50ps 50ps 2.0n 4n)
xinput_1 inb_1 outin_01 vdd inverter

$Unit Under Test
.subckt inverter in out vdd
$FETs
xpfet out in vdd vdd pfet l=16n nfin=1000m
xnfet out in gnd gnd nfet l=16n nfin=1000m
.ends

xinverter00 outin_00 outin_10 vdd inverter
xinverter10 outin_10 outin_20 vdd inverter
xinverter01 outin_01 outin_11 vdd inverter
xinverter11 outin_11 outin_21 vdd inverter

$Output Loads
xoutput_00 outin_30 outb_00 vdd inverter
xoutput_10 outin_31 outb_10 vdd inverter

$Measurements
.measure tran inv_avg_power00 avg p(xinverter00) from=0ns to=4ns
.measure tran peakpower00 max p(xinverter00)
.measure tran inv_avg_power10 avg p(xinverter10) from=0ns to=4ns
.measure tran peakpower10 max p(xinverter10)
.measure tran inv_avg_power01 avg p(xinverter01) from=0ns to=4ns
.measure tran peakpower01 max p(xinverter01)
.measure tran inv_avg_power11 avg p(xinverter11) from=0ns to=4ns
.measure tran peakpower11 max p(xinverter11)
.measure tran source_power avg power
.measure tran trf_delay_001 trig v(outin_00) val=0.425 rise=1 targ v(outin_10) val=0.425 fall=1
.measure tran tfr_delay_001 trig v(outin_00) val=0.425 fall=1 targ v(outin_10) val=0.425 rise=1
.measure tran trf_delay_002 trig v(outin_00) val=0.425 rise=2 targ v(outin_10) val=0.425 fall=2
.measure tran tfr_delay_002 trig v(outin_00) val=0.425 fall=2 targ v(outin_10) val=0.425 rise=2
.measure tran trf_delay_101 trig v(outin_10) val=0.425 rise=1 targ v(outin_20) val=0.425 fall=1
.measure tran tfr_delay_101 trig v(outin_10) val=0.425 fall=1 targ v(outin_20) val=0.425 rise=1
.measure tran trf_delay_102 trig v(outin_10) val=0.425 rise=2 targ v(outin_20) val=0.425 fall=2
.measure tran tfr_delay_102 trig v(outin_10) val=0.425 fall=2 targ v(outin_20) val=0.425 rise=2
.measure tran trf_delay_011 trig v(outin_01) val=0.425 rise=1 targ v(outin_11) val=0.425 fall=1
.measure tran tfr_delay_011 trig v(outin_01) val=0.425 fall=1 targ v(outin_11) val=0.425 rise=1
.measure tran trf_delay_111 trig v(outin_11) val=0.425 rise=1 targ v(outin_21) val=0.425 fall=1
.measure tran tfr_delay_111 trig v(outin_11) val=0.425 fall=1 targ v(outin_21) val=0.425 rise=1
.print TRAN V(outin_00) V(outin_10)
.print TRAN V(outin_10) V(outin_20)
.print TRAN V(outin_01) V(outin_11)
.print TRAN V(outin_11) V(outin_21)
$Simulation/Analysis Type
$Simulation/Analysis Type
.option post=2
.tran 10p 4ns

.end