EE105 SPICE Tutorial Example 1 - Simple RC Circuit
vs vs gnd PWL(0s 0V 5ms 0V 5.001ms 5V 10ms 5V)
r1 vs vo 1k
c1 vo gnd 1uF
.tran 0.01ms 10ms
.option post=2
.end
