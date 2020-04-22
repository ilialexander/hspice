$EE105 SPICE Tutorial Example 1 - Simple Inverter Circuit
.include ptm20lp
vin in gnd PULSE(0V 0.9V 0ns 50ps 50ps 1ns 2ns)
vs vs gnd 0.9
xpfet1 out in vs  vs  pfet l=20n nfin=1000m
xnfet1 out in gnd gnd nfet l=20n nfin=1000m
c1 out gnd 1fF
.tran 10ps 4ns
.option post=2
.end
