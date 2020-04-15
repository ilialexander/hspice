// Created by ihdl
module inverter(I_in,O_out);
   // input(s)
   input I_in;
   // output(s)
   output O_out;

   // inverts input and assigns to output
   assign O_out = !I_in;
   
endmodule // inverter
