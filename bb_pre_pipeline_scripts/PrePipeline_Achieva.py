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

diff_files = []
diff_files_sizes = []

PA_files = []
PA_files_sizes = []

AP_files = []
AP_files_sizes = []

#Removing SWI files as we are not running this part of the pipelone right now
# r=root, d=directories, f = files

#Removing WIP from the beggining of file names
for r, d, f in os.walk(path):
    for file in f:
        if 'WIP' in file:
            new_name = file.replace("WIP_", '')
            os.rename(path + "/" + file, path + "/" + new_name)


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


        #Adding "NORM" in file type in .json file for T2
        if 'FLAIR' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                for element in data:
                    data["ImageType"] = "ORIGINAL", "PRIMARY", "OTHER", "NORM"  # <--- add `id` value.
                    f.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, f, indent=4)
                    f.truncate()  # remove remaining part
            print("file " + file + " has had NORM added to FileType in .json file")

        #removing fri files with multiband 6 becuase these had artefacts
        if 'fmri' in file and 'MB4' not in file:
            os.remove(path+ "/" +file)
            print("file " + file + " has been removed")

        # removing fri files with blip because we are not using these
        if 'fmri' in file and 'blip' in file and 'MB1' not in file:
            os.remove(path + "/" + file)
            print("file " + file + " has been removed")

        #Renaming fMRI files so that they follow required convention
        if 'fmri' in file and 'MB4' in file and 'json' in file and 'blip' not in file:
            os.rename(path + "/" + file, path + "/" + "FMRI_RESTING_" + file)
            print("file " + file + " has been renamed to contain FMRI_RESTING")

        if 'fmri' in file and 'MB4' in file and '.nii.gz' in file and 'blip' not in file:
            os.rename(path + "/" + file, path + "/" + "FMRI_RESTING_" + file)
            print("file " + file + " has been renamed to contain FMRI_RESTING")


         #Renaming diffusion files so that they fit the correct file naming convention

        for extension in [".bval",".bvec",".json",".nii.gz"]:
            if 'DTI' in file and 'blip' not in file and extension in file:
                os.rename(path + "/" + file, path + "/" + "diff_AP_" + "DTI_Biobank_2mm_MB3S2_EPI_coil_echo1_401" + extension )
                print("file " + file + " has been renamed to contain diff_PA")


        for extension in [".json", ".nii.gz"]:
            if 'DTI' in file and 'blip' in file and extension in file:
                os.rename(path + "/" + file, path + "/" + "diff_PA_" + file)
                print("file " + file + " has been renamed to contain diff_PA")


#Variable for file name

f = open("Achieva_file_name.txt", "w+")
f.write(sys.argv[1])
f.close()


#Adding Effective echo spacing to resting state .json NOT NEEDED FOR GE

for r, d, f in os.walk(path):
    for file in f:

        if 'FMRI_RESTING' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                data["EffectiveEchoSpacing"] = 0.00054  # <--- add `id` value.
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            f.close()
            print("file " + file + " has had Effective EchoSpacing added to FileType in .json file")
        #Adding Effective Echo Spacing to diffusion file
        if 'diff' in file and 'json' in file:
            with open(path + '/' + file, 'r+') as f:
                data = json.load(f)
                data["EffectiveEchoSpacing"] = 0.00067  # <--- add `id` value.
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            f.close()
            print("file " + file + " has had Effective EchoSpacing added to FileType in .json file")

subprocess.call(['/home/ppxan2/UK_biobank_pipeline/bb_pre_pipeline_scripts/pre_diffusion_scripts_Achieva'])


# What the diffusion files should be called to make it easier for selection
'''
diff_PA = path + "/" + diff_files[diff_files_sizes.index(min(diff_files_sizes))]
#os.rename(diff_PA, path + "/" + "diff_PA_" + diff_files[diff_files_sizes.index(min(diff_files_sizes))] )
diff_AP = path + "/"+ diff_files[diff_files_sizes.index(max(diff_files_sizes))]
#os.rename(diff_AP, path + "/" + "diff_AP_" + diff_files[diff_files_sizes.index(m4ax(diff_files_sizes))])

diff_PA_no_ext = os.path.splitext(os.path.splitext(diff_PA)[0])[0]
diff_AP_no_ext = os.path.splitext(os.path.splitext(diff_AP)[0])[0]

#Writing the .bva. and .bvec files into the correct files

f= open(diff_PA_no_ext + ".bval","w+")
f.write("0 0 0 0 0 0 0 0")
f.close()

img = nib.load(diff_PA_no_ext + ".nii.gz")
f= open(diff_PA_no_ext + ".bvec","w+")
for i in range(0,3):
    f.write("0 0 0 0 0 0  \r\n")
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

'''
###END OF COMMENT#


    #to_delete_AP_json = os.path.splitext(os.path.splitext(to_delete_AP)[0])[0]+ ".json"


#Dealing with .json files for T1

#Adding EffectiveEchoSpacing in json file (but there is no need here as it is already in file)



'''
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
