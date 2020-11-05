$ Netlist of sram
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/sram_script.py
.lib '../models' ptm14lstp
.param vdd_50='vdd*.5'
.param vdd_10='vdd*.1'
.param vdd_15='vdd*.15'
.param vdd_90='vdd*.9'
$ UUT individual unit
.subckt inverter in out vdd gnd
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

.subckt prec sae bl bbl vdd
xsae   bl  sae vdd vdd pfet l=lg nfin=1000m
xsae_b bbl sae vdd vdd pfet l=lg nfin=1000m
.ends

.subckt writing we data bl bbl vdd
xwrite_bl  bl  we dbl  gnd nfet l=lg nfin=1000m
xwrite_bbl bbl we dbbl gnd nfet l=lg nfin=1000m
xwrite_dbl  dbl  data gnd gnd nfet l=lg nfin=1000m
xwrite_dbbl dbbl datab gnd gnd nfet l=lg nfin=1000m
xq  data datab vdd gnd inverter
.ends

.subckt sram wl bl bbl vdd
xnfet_bl  bl  wl q  q  nfet l=lg nfin=1000m
xnfet_bbl bbl wl qb qb nfet l=lg nfin=1000m
xq  qb q  vdd gnd inverter
xqb q  qb vdd gnd inverter
.ends

.subckt sa sae bl bbl sa_out sa_outb vdd
xpdiff  sa_outb sa_outb vdd vdd pfet l=lg nfin=1000m
xpdiffb sa_out  sa_outb vdd vdd pfet l=lg nfin=1000m
xndiff  sa_outb bl  gnd_acc gnd nfet l=lg nfin=1000m
xndiffb sa_out  bbl gnd_acc gnd nfet l=lg nfin=1000m
xngnd_acc gnd_acc sae gnd gnd nfet l=lg nfin=1000m
.ends
$ Sources
vdd vdd gnd vdd
$Sources
vin_wl_0 in_wl_0  gnd  pulse(vdd 0v 0.25ns 1p 1p 0.5n 1.0n)
xwl_0 in_wl_0 wl_0 vdd gnd inverter
xdata_0 gnd data_0 vdd gnd inverter
vin_we_0 in_we_0  gnd  pulse(vdd 0v 0n 1p 1p 1.0n 2n)
xwe_0 in_we_0 we_0 vdd gnd inverter
vin_sae0 in_sae_0  gnd  pulse(vdd 0v 1.5ns 1p 1p 1.0n 2n)
xsae_0 in_sae_0 sae_0 vdd gnd inverter

$ Unit Under Test
xprec_0 sae_0 bl_0 bbl_0 vdd prec
xsram_00 wl_0 bl_0 bbl_0 vdd sram
xwriting_0 we_0 data_0 bl_0 bbl_0 vdd writing
xsa_0 sae_0 bl_0 bbl_0 sa_out0 sa_outb0 vdd sa
$ Measurements
.measure tran write_q_delay_00 trig v(bbl_0) val=vdd_90 fall=1 targ v(xsram_00.q) val=vdd_90 rise=1
.measure tran write_qb_delay_00  trig v(bbl_0) val=vdd_90 fall=1 targ v(xsram_00.qb) val=vdd_10 fall=1
.measure tran read_qb_delay_00  trig v(wl_0) val=vdd_10 rise=3 targ v(xsram_00.qb) val=vdd_15 rise=1
$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 2n

.end