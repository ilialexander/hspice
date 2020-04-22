$EE105 SPICE Tutorial Example 1 - Simple RC Circuit
$`include "constants.vams"
.hdl resistor.va
v1 vs gnd 0 
x1 vs gnd resistor r=1G
.print i(x1)
.DC v1 0 1 1 
.option post=2
.end
