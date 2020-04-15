//This module tests the module 'inverter' 
module inverter_tb;
   wire out;
   reg in, clock;
   always @*
	begin //initial begin
	$monitor ("in=%b,out=%b", in,out);
	#10 assign in = 1;
	#10 assign in = 0;
      	#10 assign in = 1;
      	#10 assign in = 0;
      	#10 assign in = 1;
      	#10 assign in = 0;
      	#10  $finish;
   end

   always begin
      #5  clock =  ! clock;
   end

inverter inverter_tb (
   .I_in  (in),
   .O_out (out)
   );	

endmodule
