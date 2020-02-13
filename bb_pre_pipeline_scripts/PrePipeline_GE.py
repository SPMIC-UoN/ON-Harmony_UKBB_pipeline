#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pdb
import os
import sys
from PIL import Image
import nibabel as nib
import json


path = '/home/ppxan2/Harmonise3T/About_to_process/' + sys.argv[1]
files = []

diff_files = []
diff_files_sizes = []

PA_files = []
PA_files_sizes = []

AP_files = []
AP_files_sizes = []

#Removing SWI files as we are not running this part of the pipelone right now
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'SWI' in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")
        if 'diff' in file and 'nii.gz' in file:
            #print(file + " is size " + str(os.path.getsize(path + "/" +file)))
            diff_files.append(file)
            diff_files_sizes.append(os.path.getsize(path + "/" +file))

        #Adding NORM to ImageType for T1 json
        if 'T1' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                for element in data:
                    data["ImageType"] = "ORIGINAL", "PRIMARY", "OTHER", "NORM"  # <--- add `id` value.
                    f.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, f, indent=4)
                    f.truncate()  # remove remaining part
            print("file " + file + " has had NORM added to FileType in .json file")

        #Removing T2's which we are not using
        if 'FLAIR' in file and '1.5mm' not in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")



         #Adding "NORM" in file type in .json file
        if '1.5mm' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                for element in data:
                    data["ImageType"] = "ORIGINAL", "PRIMARY", "OTHER", "NORM"  # <--- add `id` value.
                    f.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, f, indent=4)
                    f.truncate()  # remove remaining part
            print("file " + file + " has had NORM added to FileType in .json file")

        #removing the 3.3mm files which we are not using
        if 'fMRI' in file and '3.3' in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")

        #Renaming fMRI files so that they follow required convention
        if 'fMRI_96x2.4mm' in file and 'json' in file:
            os.rename(path + "/" + file, path + "/" + "FMRI_RESTING_" + file)
            print("file " + file + " has been renamed to contain FMRI_RESTING")

        if 'fMRI_96x2.4mm' in file and 'nii.gz' in file:
            os.rename(path + "/" + file, path + "/" + "FMRI_RESTING_" + file)
            print("file " + file + " has been renamed to contain FMRI_RESTING")



#Adding Effective echo spacing to resting state .json NOT NEEDED FOR GE
'''
for r, d, f in os.walk(path):
    for file in f:
        if 'fMRI_96x2.4mm' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                for element in data:
                    data["EffectiveEchoSpacing"] = 0.00054  # <--- add `id` value.
                    f.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, f, indent=4)
                    f.truncate()  # remove remaining part
'''

# What the diffusion files should be called to make it easier for selection

diff_PA = path + "/" + diff_files[diff_files_sizes.index(min(diff_files_sizes))]
#os.rename(diff_PA, path + "/" + "diff_PA_" + diff_files[diff_files_sizes.index(min(diff_files_sizes))] )
diff_AP = path + "/"+ diff_files[diff_files_sizes.index(max(diff_files_sizes))]
#os.rename(diff_AP, path + "/" + "diff_AP_" + diff_files[diff_files_sizes.index(max(diff_files_sizes))])

diff_PA_no_ext = os.path.splitext(os.path.splitext(diff_PA)[0])[0]
diff_AP_no_ext = os.path.splitext(os.path.splitext(diff_AP)[0])[0]

#Writing the .bva. and .bvec files into the correct files

f= open(diff_PA_no_ext + ".bval","w+")
f.write("0 0 0 0 0 0 0 0")
f.close()

img = nib.load(diff_PA_no_ext + ".nii.gz")
f= open(diff_PA_no_ext + ".bvec","w+")
for i in range(0,3):
    f.write("0 0 0 0 0 0 0 0  \r\n")
f.close()

#Adding .jsons. bvecs and bvals

for r, d, f in os.walk(path):
    for file in f:
        if diff_PA_no_ext.split('/')[-1] in file and '.nii.gz' in file:
            print("file " + file + " has been renamed to contain diff_PA")
            os.rename(path + "/" + file, path + "/" + "DIFF_PA_6DIRS_B=1000_PEPOLAR_COIL_ECHO1_08.nii.gz")
        if diff_PA_no_ext.split('/')[-1] in file and 'json' in file:
            print("file " + file + " has been renamed to contain diff_PA")
            os.rename(path + "/" + file, path + "/" +"DIFF_PA_6DIRS_B=1000_PEPOLAR_COIL_ECHO1_08.json")
        if diff_PA_no_ext.split('/')[-1] in file and 'bval' in file:
            print("file " + file + " has been added")
            os.rename(path + "/" + file, path + "/" + "DIFF_PA_6DIRS_B=1000_PEPOLAR_COIL_ECHO1_08.bval")
        if diff_PA_no_ext.split('/')[-1] in file and 'bvec' in file:
            print("file " + file + " has been added")
            os.rename(path + "/" + file, path + "/" + "DIFF_PA_6DIRS_B=1000_PEPOLAR_COIL_ECHO1_08.bvec")
        if diff_AP_no_ext.split('/')[-1] in file and '.nii.gz' in file:
            print("file " + file + " has been renamed to contain diff_AP")
            os.rename(path + "/" + file, path + "/" + "DIFF_AP_60DIRS_B=1000_COIL_ECHO1_09.nii.gz")
        if diff_AP_no_ext.split('/')[-1] in file and 'json' in file:
            print("file " + file + " has been renamed to contain diff_AP")
            os.rename(path + "/" + file, path + "/" + "DIFF_AP_60DIRS_B=1000_COIL_ECHO1_09.json")
        if diff_AP_no_ext.split('/')[-1] in file and 'bval' in file:
            print("file " + file + " has been renamed to contain diff_AP")
            os.rename(path + "/" + file, path + "/" + "DIFF_AP_60DIRS_B=1000_COIL_ECHO1_09.bval")
        if diff_AP_no_ext.split('/')[-1] in file and 'bvec' in file:
            print("file " + file + " has been renamed to contain diff_AP")
            os.rename(path + "/" + file, path + "/" + "DIFF_AP_60DIRS_B=1000_COIL_ECHO1_09.bvec")

for r, d, f in os.walk(path):
    for file in f:
        if 'diff' in file and 'P' not in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")

for r, d, f in os.walk(path):
    for file in f:
        if 'SSFSE' in file:
            os.remove(path + "/" + file)
            print("file " + file + " has been removed")

for r, d, f in os.walk(path):
    for file in f:
        if 'ASSET' in file:
            os.remove(path + "/" + file)
            print("file " + file + " has been removed")

for r, d, f in os.walk(path):
    for file in f:
        if 'Stacked' in file:
            os.remove(path + "/" + file)
            print("file " + file + " has been removed")

    #to_delete_AP_json = os.path.splitext(os.path.splitext(to_delete_AP)[0])[0]+ ".json"


#Dealing with .json files for T1
'''
#Adding EffectiveEchoSpacing in json file (but there is no need here as it is already in file)

with open(diff_PA_no_ext + ".json", 'r+') as f:
    data = json.load(f)
    data["id"] = 134 # <--- add `id` value.
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()     # remove remaining part


#Dealing with .json files for diffusion

#Dealing with the json files



with open(diff_PA_no_ext + ".json", 'r+') as f:
    data = json.load(f)
    data["id"] = 134 # <--- add `id` value.
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()     # remove remaining part



    if len(AP_files) > 1:
        #os.remove(to_delete_AP)
        #os.remove(to_delete_AP_json)






    min_value = min(PA_files_sizes)
    min_index = PA_files_sizes.index(min_value)
    print("about to remove")
    to_delete = path + "/"+ PA_files[min_index]
    print(to_delete)
    if len(PA_files) > 1:
        #os.remove(to_delete)
    to_delete_json = os.path.splitext(os.path.splitext(to_delete)[0])[0]+ ".json"
    print(to_delete_json)
    if len(PA_files) > 1:
        #os.remove(to_delete_json)

    to_write = PA_files[(PA_files_sizes.index(max(PA_files_sizes)))]
    to_write = os.path.splitext(os.path.splitext(to_write)[0])[0]
    print("ging to make this file")
    print(to_write + ".bval")
    print(to_write + ".bvec")




    #Writing the .bva. and .cec files into the correct files

f= open(diff_PA_no_ext + ".bval","w+")
f.write("0 0 0 0 0 0 0 0")
f.close()

img = nib.load(diff_PA_no_ext + ".nii.gz")
f= open(diff_PA_no_ext + ".bvec","w+")
for i in range (img.header.get_data_shape()[3]):
    f.write("0 0 0 0 0 0  \r\n")
f.close()


    #os.remove(path + "/"+ PA_files[min_index])


        #for file in PA_files:
'''
