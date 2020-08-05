$This UUT was automatically generated by:
$/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/inverter_script.py

$Netlist of test
.include lstp_20

$FETs
xpfet1 out in vdd vdd pfet l=lstpn nfin=1000m
xnfet1 out in gnd gnd nfet l=lstpn nfin=1000m

$Output Load
c1 out 0 5f

$Power Sources
vdd vdd gnd 0.9V
vin in  gnd  PULSE(0V 0.9V 0ns 50ps 50ps 1ns 20ns)

.option post=2

$Analysis
.tran 10ps 4ns

.end