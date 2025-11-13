#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pdb
import os
import sys
#from PIL import Image
import nibabel as nib
import json
import subprocess


path = '/home/ppxan2/Harmonise3T/About_to_process/' + sys.argv[1]

files = []
PA_files = []
PA_files_sizes = []

AP_files = []
AP_files_sizes = []

#Removing SWI files as we are not running this part of the pipelone roight now
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'SWI' in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")

        if 'diff_PA_MPopt_MB3_3b0_lowflip_coil_echo1' in file and 'nii.gz' in file:
            print(file + " is size " + str(os.path.getsize(path + "/" +file)))
            PA_files.append(file)
            PA_files_sizes.append(os.path.getsize(path + "/" +file))

        if 'diff_AP' in file and 'nii.gz' in file:
            print(file + " is size " + str(os.path.getsize(path + "/" +file)))
            AP_files.append(file)
            AP_files_sizes.append(os.path.getsize(path + "/" +file))

        if 'FMRI' in file and 'FMRI_RESTING' not in file:
            os.rename(path + "/" + file,path + "/" +"FMRI_RESTING_"+file)
            print(file)

    to_delete_AP = path + "/"+ AP_files[AP_files_sizes.index(min(AP_files_sizes))]
    to_delete_AP_json = os.path.splitext(os.path.splitext(to_delete_AP)[0])[0]+ ".json"

    if len(AP_files) > 1:
        os.remove(to_delete_AP)
        os.remove(to_delete_AP_json)






    min_value = min(PA_files_sizes)
    min_index = PA_files_sizes.index(min_value)
    print("about to remove")
    to_delete = path + "/"+ PA_files[min_index]
    print(to_delete)
    if len(PA_files) > 1:
        os.remove(to_delete)
    to_delete_json = os.path.splitext(os.path.splitext(to_delete)[0])[0]+ ".json"
    print(to_delete_json)
    if len(PA_files) > 1:
        os.remove(to_delete_json)

    to_write = PA_files[(PA_files_sizes.index(max(PA_files_sizes)))]
    to_write = os.path.splitext(os.path.splitext(to_write)[0])[0]
    print("ging to make this file")
    print(to_write + ".bval")
    print(to_write + ".bvec")


    #Writing the .bva. and .cec files into the correct files

    f= open(path + "/" + to_write + ".bval","w+")
    f.write("0 0 0 0 0 0")
    f.close()

    img = nib.load(path + "/" + to_write + ".nii.gz")
    f= open(path + "/" + to_write + ".bvec","w+")
    for i in range (img.header.get_data_shape()[3]):
        f.write("0 0 0 0 0 0  \r\n")
    f.close()


    #os.remove(path + "/"+ PA_files[min_index])


        #for file in PA_files:
