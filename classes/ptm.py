#!/usr/bin/env python

import os

class Ptm:

    def __init__(self, uut, nmodel, pmodel):
        self.uut = uut #unit under test
        self.nmodel = nmodel # n channel model name
        self.pmodel = pmodel # p channel model name

    def get_models(self, directory):
        '''Gathers the list of models files'''
        files_list = os.listdir(directory) # contains all files in directory
        models_full_paths = list() # will hold the list of full paths
        for ea_file in files_list: # iterates over all the entries
            full_path = os.path.join(directory, ea_file) # creates full path
            if os.path.isdir(full_path): # if subdirectory get children files
                models_full_paths += self.get_models(full_path) # recursive get_models for subdirectory's files
            else:
                models_full_paths.append(full_path) # add full_paht to list

        return models_full_paths


    def set_fet_names(self, directory):
        '''Set the names for the subckt files'''
        models_full_paths = self.get_models(directory) # get all fet models        
        # retrieves file names from models_full_paths
        models_files  = [files.replace(directory, '').replace(self.nmodel, '').replace('/', '_') for files in models_full_paths]
        # cleans extra models under pmodels names
        r_subckt_names = [model for model in models_files if self.pmodel not in model]
        models_subckt_names = list()
        # refine the names of the subckt models
        [models_subckt_names.append("".join(reversed(r_subckt_name.split("_")))) for r_subckt_name in r_subckt_names]

        return models_subckt_names


    def set_uut_dir(self, dir_name):
        '''Creates directories for the Unit Under Test (uut)'''
        self.models_subdir = self.set_fet_names(dir_name) # set subckt files names
        local_paths = [self.uut + '/' + self.uut + '_' + subdir_name for subdir_name in self.models_subdir] # set models' directory names
        local_paths.insert(0,self.uut) # add parent directory
        for subdir_name in local_paths: # iterates through paths' list
            try:
                os.mkdir(subdir_name) # creates the directory
            except OSError:
                # if directory exist then prints 'warning' message
                print ("Subdirectory %s already exists. Try deleting it with 'rm -r uut_name' and starting fresh." % subdir_name)
            else:
                print ("Successfully created the directory %s " % subdir_name)

        return local_paths


    def set_fet_subckts(self, local_paths):
        '''Creates the subckt files for the fet models'''
        writing = 0 # flag to start and stop writing
        for path, model_subckt_name in zip(local_paths[1:],self.models_subdir): # iterates through subckt names and paths
            # Creates a new file 
            with open(path + "/" + model_subckt_name, 'w+') as subckt: # open file to write
                subckt.write("$This subckt was automatically generated by:\n") # disclaimere to find script in the future
                subckt.write("$" + os.getcwd() + "/" + __file__ + "\n") # whrite location of script for easy search
                with open('models') as models:
                    for line in models:
                        if ("Example" not in line) & (model_subckt_name in line) & (writing == 0): # condition to start writing subckt
                            writing = 1
                            subckt.write(line)
                        elif (model_subckt_name in line) & (writing == 1): # condition to stop writing subckt
                            subckt.write(line)
                            writing = 0
                        elif (writing == 1): # condition to continue writing subckt
                            subckt.write(line)
                        else:
                            pass

        return None 
