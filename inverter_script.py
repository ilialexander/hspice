#!/usr/bin/env python
import os
from classes.ptm import Ptm

def main():
    # For the given path, get the full path list of transistors models
    dir_name = '/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/modelfiles/'

    temp = Ptm("test", "nfet.pm", "pfet.pm")

    subdir_paths = temp.set_uut_dir(dir_name) # create uut directories and sbudirs

    temp.set_fet_subckts(subdir_paths) # create fet subckt in subdirs

if __name__ == '__main__':
    main()

