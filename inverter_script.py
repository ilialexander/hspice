#!/usr/bin/env python
import os
from classes.ptm import Ptm

def main():
    # For the given path, get the full path list of transistors models
    dir_name = '/work_bgfs/i/iliabautista/2-Research/2-Simulations/1-HDL/hspice/modelfiles/'

    temp = Ptm("test", "nfet.pm", "pfet.pm")

    # Get the list of all files in directory tree at given path
    models_paths = temp.get_models(dir_name)

    cir_files = temp.set_fet_names(dir_name, models_paths)

    dir_paths = temp.set_uut_dir(cir_files)

    temp.set_fet_subckts(cir_files, dir_paths)

if __name__ == '__main__':
    main()

