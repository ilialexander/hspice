$ Netlist of sram_lstp
$ This UUT was automatically generated by:
$ /home/i/iliabautista/Desktop/2-Research/2-Simulations/1-HDL/hspice/sram_lstp_write.py
.lib '../models' ptm10lstp
.param vdd_50='vdd*.5'
.param vdd_10='vdd*.1'
.param vdd_15='vdd*.15'
.param vdd_90='vdd*.9'
$ UUT individual unit
.subckt inverter in out vdd gnd
xpfet out in vdd vdd pfet l=lg nfin=1000m
xnfet out in gnd gnd nfet l=lg nfin=1000m
.ends

.subckt prec phi bl bbl vdd
xprecbl  bl  phi vdd vdd pfet l=lg nfin=1000m
xprecbbl bbl phi vdd vdd pfet l=lg nfin=1000m
xprec_eq bl phi bbl  bbl  pfet l=lg nfin=1000m
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

$ Sources
vdd vdd gnd vdd
$Sources
vin_wl_0 in_wl_0  gnd  pulse(vdd 0v 0.05n 1p 1p 0.25n 0.5n)
xwl_0 in_wl_0 wl_0 vdd gnd inverter
xdata_0 vdd data_0 vdd gnd inverter
vin_phi0 in_phi_0  gnd  pulse(0v vdd 0ns 1p 1p 0.051n .5n)
xphi_0 in_phi_0 phi_0 vdd gnd inverter
vin_we_0 in_we_0  gnd  pulse(vdd 0v 0.05n 1p 1p 0.25n 2n)
xwe_0 in_we_0 we_0 vdd gnd inverter

$ Unit Under Test
.subckt uut_grid vdd
+phi_0 bl_0 bbl_0 we_0 data_0 wl_0 $inputs to uut_grid Subckt
$outputs to uut_grid Subckt
xprec_0 phi_0 bl_0 bbl_0 vdd prec
xsram_00 wl_0 bl_0 bbl_0 vdd sram
xwriting_0 we_0 data_0 bl_0 bbl_0 vdd writing
.ends
$invoke UUT grid
xuut_grid vdd
+phi_0 bl_0 bbl_0 we_0 data_0 wl_0 $inputs to uut_grid
$outputs to uut_grid
+uut_grid

$ Measurements
.measure tran uut_avg_write_power avg p(xuut_grid) from=0 to=20ps
.measure tran uut_avg_hold_power avg p(xuut_grid) from=0.27ns to=0.5ns
.measure tran uut_avg_read_power avg p(xuut_grid) from=0.48ns to=0.55ns
.measure tran prec_avg_write_power_0 avg p(xuut_grid.xprec_0) from=0 to=20ps
.measure tran prec_avg_hold_power_0 avg p(xuut_grid.xprec_0) from=0.27ns to=0.5ns
.measure tran prec_avg_read_power_0 avg p(xuut_grid.xprec_0) from=0.48ns to=0.55ns
.measure tran sram_avg_write_power_00 avg p(xuut_grid.xsram_00) from=0 to=20ps
.measure tran sram_avg_hold_power_00 avg p(xuut_grid.xsram_00) from=0.27ns to=0.5ns
.measure tran sram_avg_read_power_00 avg p(xuut_grid.xsram_00) from=0.48ns to=0.55ns
.measure tran writing_avg_write_power_0 avg p(xuut_grid.xwriting_0) from=0 to=20ps
.measure tran writing_avg_hold_power_0 avg p(xuut_grid.xwriting_0) from=0.27ns to=0.5ns
.measure tran writing_avg_read_power_0 avg p(xuut_grid.xwriting_0) from=0.48ns to=0.55ns
.measure tran sa_avg_writing_power_0 avg p(xuut_grid.xsa_0) from=0 to=20ps
.measure tran sa_avg_hold_power_0 avg p(xuut_grid.xsa_0) from=0.27ns to=0.5ns
.measure tran sa_avg_read_power_0 avg p(xuut_grid.xsa_0) from=0.48ns to=0.55ns
.measure tran write_q_delay_00 trig v(wl_0) val=vdd_10 rise=1 targ v(xuut_grid.xsram_00.q) val=vdd_90 rise=1
.measure tran uut_avg_power avg p(xuut_grid)
$ Simulation/Analysis Type
.option post=2 ingold=2
.tran 1p 1n

.end