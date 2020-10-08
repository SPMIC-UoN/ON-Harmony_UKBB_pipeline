#!/bin/env python
#
# Script name: bb_pipeline.py
#
# Description: Main script. This script will call the rest of scripts.
#
# Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson
#
# Copyright 2017 University of Oxford
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import os
import glob
import time
import logging
import sys,argparse,os.path
import bb_logging_tool as LT
from bb_file_manager import bb_file_manager
from bb_basic_QC import bb_basic_QC
from bb_structural_pipeline.bb_pipeline_struct import bb_pipeline_struct
from bb_functional_pipeline.bb_pipeline_func import bb_pipeline_func
from bb_diffusion_pipeline.bb_pipeline_diff import bb_pipeline_diff
from bb_IDP.bb_IDP import bb_IDP

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main():

    parser = MyParser(description='BioBank Pipeline Manager, Runs all modalities by default with pipeline generated SBREF and Fix fmri denoising')
    parser.add_argument("subjectFolder", help='Subject Folder')
    parser.add_argument("Machine", help='The machine on which the data was acquired',choices=['Siemens_P1','Siemens_P2','Siemens_T', 'Phillips', 'GE'])
    parser.add_argument('-S', '--Structural', action='store_true', help="Runs pipeline with strucutural processing")
    parser.add_argument('-F', '--Functional', action='store_true', help="Runs pipeline with functional processing")
    parser.add_argument('-D', '--Diffusion', action='store_true', help="Runs pipeline with diffusion processing")
    parser.add_argument('-IDP', '--IDP', action='store_true', help="Only runs IDP generating part of the pipeline")
    parser.add_argument('-SBREF', '--Acquired_SBREF', action='store_true', help="uses acquired SBREF rather than pipeline generated version")
    #default value for fmri denosing
    fmri_denoising = "Fix"
    parser.add_argument('-fd', '--fmri_denoising', help='method of fmri denoising',choices=['Off', 'Fix', 'Aroma'])

    argsa = parser.parse_args()

    subject = argsa.subjectFolder
    subject = subject.strip()
    Machine = argsa.Machine

    if "Siemens" in Machine:
        Vendor = "Siemens"
    elif "Phillips" in Machine:
        Vendor = "Phillips"
    elif "GE" in Machine:
        Vendor = "GE"


    if argsa.fmri_denoising:
        fmri_denoising = argsa.fmri_denoising

    if Vendor != 'Siemens':
        GDC_Status = "GDC_off"
        Individual_SWI_MAG_coils = "Comb_coils"
    else:
        GDC_Status = "GDC_on"
        Individual_SWI_MAG_coils = "Indiv_coils"
    print("Running Pipeline for Machine: " + Machine)

    #Default value for modality stautus. These will run by default unless optional arguments are entered.
    Structural_status = "1"
    SWI_Status = "SWI_on"
    Functional_status = "1"
    Diffusion_status = "1"

    if argsa.Structural == True and argsa.Functional != True and argsa.Diffusion != True:
        Functional_status = "-1"
        Diffusion_status = "-1"
        print("Only structural processing to run")

    if argsa.Structural == True and argsa.Functional == True and argsa.Diffusion != True:
        Diffusion_status = "-1"
        print("Only structural and functional processing to run")

    if argsa.Structural == True and argsa.Functional != True and argsa.Diffusion == True:
        Functional_status = "-1"
        print("Only structural and diffusion processing to run")

    if argsa.Structural != True and argsa.Functional == True and argsa.Diffusion != True:
        Structural_status = "-1"
        Diffusion_status = "-1"
        print("Only functional processing to run")

    if argsa.Structural != True and argsa.Functional == True and argsa.Diffusion == True:
        Structural_status = "-1"
        print("Only functional and diffusion processing to run")

    if argsa.Structural != True and argsa.Functional != True and argsa.Diffusion == True:
        Structural_status = "-1"
        Functional_status = "-1"
        print("Only diffusion processing to run")

    if argsa.Structural != True and argsa.Functional != True and argsa.Diffusion != True:
        print("Processing of all modalities to run")

    if argsa.IDP == True and argsa.Structural != True and argsa.Functional != True and argsa.Diffusion != True:
        Structural_status = "-1"
        Functional_status = "-1"
        Diffusion_status = "-1"
        print("Only running IDP generating part of the pipeline")


    if argsa.Acquired_SBREF:
        Acquired_SBREF = True
        print("Using acquired SBREF")
    else:
        Acquired_SBREF = False
        print("Using Pipeline generated SBREF")

    print("Method of fmri denosing: " + fmri_denoising)

    if subject[-1] =='/':
        subject = subject[0:len(subject)-1]

    logger = LT.initLogging(__file__, subject)

    logger.info('Running file manager')
    fileConfig = bb_file_manager(subject, Vendor, Acquired_SBREF)
    fileConfig = bb_basic_QC(subject, fileConfig)

    logger.info("File configuration after running file manager: " + str(fileConfig))

    # runTopup ==> Having fieldmap
    if not (( ('AP' in fileConfig ) and  (fileConfig['AP'] != '')) and (('PA' in fileConfig ) and  (fileConfig['PA'] != ''))):
        logger.error("There is no proper DWI data. Thus, the B0 file cannot be generated in order to run topup")
        runTopup = False
    else:
        runTopup = True

    # Default value for job id. SGE does not wait for a job with this id.
    jobSTEP1 = "-1"
    jobSTEP2 = "-1"
    jobSTEP3 = "-1"

    if Structural_status == '1':
        jobSTEP1 = bb_pipeline_struct(subject, runTopup, fileConfig, Vendor , GDC_Status, Individual_SWI_MAG_coils, SWI_Status, Machine )

    # Will only wait for top up if structural pipeline has been scheduled to run
    if Structural_status == '1':
        if runTopup:
            if Functional_status == '1':
                jobSTEP2 = bb_pipeline_func(subject, str(jobSTEP1), fileConfig, GDC_Status, fmri_denoising, Machine)
            if Diffusion_status == '1':
                jobSTEP3 = bb_pipeline_diff(subject, str(jobSTEP1), fileConfig, GDC_Status, Machine)
    else:
            if Functional_status == '1':
                jobSTEP2 = bb_pipeline_func(subject, str(jobSTEP1), fileConfig, GDC_Status, fmri_denoising, Machine)
            if Diffusion_status == '1':
                jobSTEP3 = bb_pipeline_diff(subject, str(jobSTEP1), fileConfig, GDC_Status, Machine)


    jobSTEP4 = bb_IDP(subject, str(jobSTEP1) + "," + jobSTEP2 + "," + jobSTEP3, str(fileConfig))

    LT.finishLogging(logger)

if __name__ == "__main__":
    main()
