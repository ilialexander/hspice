$ Netlist of match_cam
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice//home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/match_cam_script.py
.lib '../models' ptm14hp
.param vdd_50='vdd*.5'
.param vdd_10='vdd*.1'
.param vdd_15='vdd*.15'
.param vdd_90='vdd*.9'
.param vdd_70='vdd*.7'
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

.subckt cam wl ml bl bbl vdd
xnfet_bl  bl  wl q  q  nfet l=lg nfin=1000m
xnfet_bbl bbl wl qb qb nfet l=lg nfin=1000m
xq  qb q  vdd gnd inverter
xqb q  qb vdd gnd inverter
xmatch_q   ml qb gnd_acc_bl gnd nfet l=lg nfin=1000m
xmatch_qb  ml q  gnd_acc_bbl gnd nfet l=lg nfin=1000m
xmatch_bl  gnd_acc_bbl bl  gnd gnd nfet l=lg nfin=1000m
xmatch_bbl gnd_acc_bl bbl gnd gnd nfet l=lg nfin=1000m
.ends

.subckt sa sae saeb bl bbl d_out vdd
xngnd_acc gnd_acc sae  gnd gnd nfet l=lg nfin=1000m
xneq  sa_outb saeb sa_out sa_out nfet l=lg nfin=1000m
xpdiff  sa_outb sa_out  vdd vdd pfet l=lg nfin=1000m
xpdiffb sa_out  sa_outb vdd vdd pfet l=lg nfin=1000m
xndiff  sa_outb bl  gnd_acc gnd nfet l=lg nfin=1000m
xndiffb sa_out  bbl gnd_acc gnd nfet l=lg nfin=1000m
xd_out sa_outb  d_out vdd gnd inverter
.ends
.subckt match_sa ml ml_pre ml_pre_b ml_out vdd
xmlpre_b ml     ml_pre_b vdd vdd pfet l=lg nfin=1000m
xmlpre ml_out_b ml_pre   gnd gnd nfet l=lg nfin=1000m
xml    ml_out_b ml       vdd vdd pfet l=lg nfin=1000m
xd_out ml_out_b ml_out vdd gnd inverter
.ends
$ Sources
vdd vdd gnd vdd
$Sources
vin_wl_0 in_wl_0  gnd  pulse(vdd 0v 0s 1p 1p 0.25n 0.5n)
xwl_0 in_wl_0 wl_0 vdd gnd inverter
vin_ml_pre_0 in_ml_pre_0  gnd  pulse(0v vdd 0.5ns 1p 1p 0.25n 0.5n)
xml_pre_0 in_ml_pre_0 ml_pre_0 vdd gnd inverter
xml_pre_b0 ml_pre_0 ml_pre_b_0 vdd gnd inverter
xdata_0 vdd data_0 vdd gnd inverter
vin_we_0 in_we_0  gnd  pulse(vdd 0v 0n 1p 1p 0.25n 2n)
xwe_0 in_we_0 we_0 vdd gnd inverter
vin_phi0 in_phi_0  gnd  pulse(0v vdd 0.5ns 1p 1p 0.2n 2n)
xphi_0 in_phi_0 phi_0 vdd gnd inverter
vin_sae0 in_sae_0  gnd  pulse(vdd 0v .5ns 1p 1p 0.25n 2n)
xsae_0 in_sae_0 sae_0 vdd gnd inverter
xsaeb_0 sae_0 saeb_0 vdd gnd inverter

$ Unit Under Test
.subckt uut_grid vdd
+sae_0 saeb_0 bl_0 bbl_0 we_0 data_0 wl_0 ml_0 ml_pre_0 ml_pre_b_0 $inputs to uut_grid Subckt
+d_out_1 ml_out_0 $outputs to uut_grid Subckt
xprec_0 sae_0 bl_0 bbl_0 vdd prec
xcam_00 wl_0 ml_0 bl_0 bbl_0 vdd cam
xmatch_sa_0 ml_0 ml_pre_0 ml_pre_b_0 ml_out_0 vdd match_sa
xwriting_0 we_0 data_0 bl_0 bbl_0 vdd writing
xsa_0 sae_0 saeb_0 bl_0 bbl_0 d_out_0 vdd sa
.ends
$invoke UUT grid
xuut_grid vdd
+sae_0 saeb_0 bl_0 bbl_0 we_0 data_0 wl_0 ml_0 ml_pre_0 ml_pre_b_0 $inputs to uut_grid
+d_out_0 ml_out_0 $outputs to uut_grid
+uut_grid

$ Measurements
.measure tran uut_avg_write_power avg p(xuut_grid) from=0 to=60ps
.measure tran uut_avg_hold_power avg p(xuut_grid) from=0.3ns to=0.45ns
.measure tran uut_avg_match_power avg p(xuut_grid) from=0.49ns to=0.52ns
.measure tran prec_avg_write_power_0 avg p(xuut_grid.xprec_0) from=0 to=60ps
.measure tran prec_avg_hold_power_0 avg p(xuut_grid.xprec_0) from=0.3ns to=0.45ns
.measure tran prec_avg_match_power_0 avg p(xuut_grid.xprec_0) from=0.49ns to=0.52ns
.measure tran cam_avg_write_power_00 avg p(xuut_grid.xcam_00) from=0 to=60ps
.measure tran cam_avg_hold_power_00 avg p(xuut_grid.xcam_00) from=0.3ns to=0.45ns
.measure tran cam_avg_match_power_00 avg p(xuut_grid.xcam_00) from=0.49ns to=0.52ns
.measure tran writing_avg_write_power_0 avg p(xuut_grid.xwriting_0) from=0 to=60ps
.measure tran writing_avg_hold_power_0 avg p(xuut_grid.xwriting_0) from=0.3ns to=0.45ns
.measure tran writing_avg_match_power_0 avg p(xuut_grid.xwriting_0) from=0.49ns to=0.52ns
.measure tran sa_avg_writing_power_0 avg p(xuut_grid.xsa_0) from=0 to=60ps
.measure tran sa_avg_hold_power_0 avg p(xuut_grid.xsa_0) from=0.3ns to=0.45ns
.measure tran sa_avg_match_power_0 avg p(xuut_grid.xsa_0) from=0.49ns to=0.52ns
.measure tran write_q_delay_00 trig v(wl_0) val=vdd_10 rise=1 targ v(xuut_grid.xcam_00.q) val=vdd_90 rise=1
.measure tran match_q_delay_00  trig v(wl_0) val=vdd_10 rise=2 targ v(ml_out_0) val=vdd_10 fall=1
.measure tran uut_avg_power avg p(xuut_grid)
$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 1n

.end