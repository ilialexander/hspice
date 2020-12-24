$ Netlist of cam
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/cam_script.py
.lib '../models' ptm16hp
.param vdd_50='vdd*.5'
.param vdd_10='vdd*.1'
.param vdd_15='vdd*.15'
.param vdd_90='vdd*.9'
$ UUT individual unit
.subckt inverter in out vdd
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

.subckt prec sae bl bbl 
xprec_bl bl sae vdd vdd pfet l=lg nfin=1000m
xprec_bbl bbl sae vdd vdd pfet l=lg nfin=1000m
.ends

.subckt writing we data bl bbl vdd
xwrite_bl  datab we bl  gnd nfet l=lg nfin=1000m
xwrite_bbl data  we bbl gnd nfet l=lg nfin=1000m
xq  data datab vdd inverter
.ends

.subckt cam wl ml bl bbl vdd
xnfet_bl  bl  wl q  gnd nfet l=lg nfin=1000m
xnfet_bbl bbl wl qb gnd nfet l=lg nfin=1000m
xq  qb q  vdd inverter
xqb q  qb vdd inverter
xmatch_q   ml qb gnd_acc gnd nfet l=lg nfin=1000m
xmatch_qb  ml q  gnd_acc gnd nfet l=lg nfin=1000m
xmatch_bl  gnd_acc bl  gnd gnd nfet l=lg nfin=1000m
xmatch_bbl gnd_acc bbl gnd gnd nfet l=lg nfin=1000m
.ends

.subckt sa sae saeb bl bbl d_out vdd
xngnd_acc gnd_acc sae  gnd gnd nfet l=lg nfin=1000m
xneq  sa_outb saeb sa_out sa_out nfet l=lg nfin=1000m
xpdiff  sa_outb sa_out  vdd vdd pfet l=lg nfin=1000m
xpdiffb sa_out  sa_outb vdd vdd pfet l=lg nfin=1000m
xndiff  sa_outb bl  gnd_acc gnd nfet l=lg nfin=1000m
xndiffb sa_out  bbl gnd_acc gnd nfet l=lg nfin=1000m
xd_out sa_outb  d_out vdd inverter
.ends
$ Sources
vdd vdd gnd vdd
$Sources
vin_wl_0 in_wl_0  gnd  pulse(vdd 0v 0s 1p 1p 0.25n 0.5n)
xwl_0 in_wl_0 wl_0 vdd inverter
xdata_0 vdd data_0 vdd inverter
vin_we_0 in_we_0  gnd  pulse(vdd 0v 0n 1p 1p 0.25n 2n)
xwe_0 in_we_0 we_0 vdd inverter
vin_sae0 in_sae_0  gnd  pulse(vdd 0v .5ns 1p 1p 0.25n 2n)
xsae_0 in_sae_0 sae_0 vdd inverter
xsaeb_0 sae_0 saeb_0 vdd inverter

$ Unit Under Test
.subckt uut_grid vdd
+sae_0 saeb_0 bl_0 bbl_0 we_0 data_0 wl_0 ml_0 $inputs to uut_grid Subckt
+d_out_1 $outputs to uut_grid Subckt
xprec_0 sae_0 bl_0 bbl_0 prec
xcam_00 wl_0 ml_0 bl_0 bbl_0 vdd cam
xwriting_0 we_0 data_0 bl_0 bbl_0 vdd writing
xsa_0 sae_0 saeb_0 bl_0 bbl_0 d_out_0 vdd sa
.ends
$invoke UUT grid
xuut_grid vdd
+sae_0 saeb_0 bl_0 bbl_0 we_0 data_0 wl_0 ml_0 $inputs to uut_grid
+d_out_0 $outputs to uut_grid
+uut_grid

$ Measurements
.measure tran uut_avg_hold_power avg p(xuut_grid) from=0ns to=0.15ns
.measure tran uut_avg_write_power avg p(xuut_grid) from=0.15ns to=0.35ns
.measure tran uut_avg_read_power avg p(xuut_grid) from=0.7ns to=0.9ns
.measure tran prec_avg_hold_power_0 avg p(xuut_grid.xprec_0) from=0ns to=0.15ns
.measure tran prec_avg_write_power_0 avg p(xuut_grid.xprec_0) from=0.15ns to=0.35ns
.measure tran prec_avg_read_power_0 avg p(xuut_grid.xprec_0) from=0.7ns to=0.9ns
.measure tran cam_avg_hold_power_00 avg p(xuut_grid.xcam_00) from=0ns to=0.15ns
.measure tran cam_avg_write_power_00 avg p(xuut_grid.xcam_00) from=0.15ns to=0.35ns
.measure tran cam_avg_read_power_00 avg p(xuut_grid.xcam_00) from=0.7ns to=0.9ns
.measure tran writing_avg_hold_power_0 avg p(xuut_grid.xwriting_0) from=0ns to=0.15ns
.measure tran writing_avg_write_power_0 avg p(xuut_grid.xwriting_0) from=0.15ns to=0.35ns
.measure tran writing_avg_read_power_0 avg p(xuut_grid.xwriting_0) from=0.7ns to=0.9ns
.measure tran sa_avg_hold_power_0 avg p(xuut_grid.xsa_0) from=0ns to=0.15ns
.measure tran sa_avg_writing_power_0 avg p(xuut_grid.xsa_0) from=0.15ns to=0.35ns
.measure tran sa_avg_read_power_0 avg p(xuut_grid.xsa_0) from=0.7ns to=0.9ns
.measure tran write_q_delay_00 trig v(we_0) val=vdd_10 rise=1 targ v(xuut_grid.xcam_00.q) val=vdd_90 rise=1
.measure tran read_q_delay_00  trig v(sae_0) val=vdd_10 rise=1 targ v(xuut_grid.d_out_0) val=vdd_90 rise=1
.measure tran uut_avg_power avg p(xuut_grid)
$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 1n

.end