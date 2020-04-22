EE105 SPICE Tutorial Example 1 - Simple Inverter Circuit
vin in gnd PULSE(0V 0.9V 0ns 50ps 50ps 1ns 2ns)
vs vs gnd 0.9
Mp1 out in vs  vs  p L=10n
Mn2 out in gnd gnd n L=10n
c1 out gnd 1fF
.tran 10ps 4ns
.option post=2
.MODEL p PMOS LEVEL=72
.MODEL n NMOS LEVEL=72
.end
