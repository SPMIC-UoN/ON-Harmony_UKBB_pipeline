#!/bin/env python
#
# Script name: bb_pipeline_func.py
#
# Description: Script with the functional pipeline.
#			   This script will call the rest of functional functions.
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

import bb_pipeline_tools.bb_logging_tool as LT
import os.path

def bb_pipeline_func(subject, jobHold, fileConfiguration, GDC_Status, fmri_denoising, Machine):

    logger  = LT.initLogging(__file__, subject)
    logDir  = logger.logDir
    baseDir = logDir[0:logDir.rfind('/logs/')]

    jobsToWaitFor = ""

    jobPOSTPROCESS = LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 5 -N "bb_postprocess_struct_' + subject + '" -l ' + logDir + ' -j ' + jobHold + ' $BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct ' + subject)

    #TODO: Embed the checking of the fieldmap inside the independent steps -- Every step should check if the previous one has ended.
    if ('rfMRI' in fileConfiguration) and (fileConfiguration['rfMRI'] != ''):

        jobPREPARE_R = LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 15   -N "bb_prepare_rfMRI_' + subject + '"  -l ' + logDir + ' -j ' + jobPOSTPROCESS + ' $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_rfMRI ' + subject + ' ' + GDC_Status + ' ' + Machine)
        jobFEAT_R =    LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 1200 -N "bb_feat_rfMRI_ns_' + subject + '"  -l ' + logDir + ' -j ' + jobPREPARE_R   + ' feat  ' + baseDir + '/fMRI/rfMRI.fsf')
        jobFIX =       LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 175  -N "bb_fix_'           + subject + '"  -l ' + logDir + ' -j ' + jobFEAT_R      + ' $BB_BIN_DIR/bb_functional_pipeline/bb_fix ' + subject + ' ' + fmri_denoising )
        jobDR  =       LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 120  -N "bb_ICA_dr_'        + subject + '"  -l ' + logDir + ' -j ' + jobFIX         + ' $BB_BIN_DIR/bb_functional_pipeline/bb_ICA_dual_regression ' + subject )
        jobCLEAN =     LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 5    -N "bb_rfMRI_clean_'   + subject + '"  -l ' + logDir + ' -j ' + jobDR          + ' $BB_BIN_DIR/bb_functional_pipeline/bb_clean_fix_logs ' + subject )

        jobsToWaitFor  = jobCLEAN

    else:
        logger.error("There is no rFMRI info. Thus, the Resting State part will not be run")

    if ('tfMRI' in fileConfiguration) and (fileConfiguration['tfMRI'] != ''):
        jobPREPARE_T = LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T  15 -N "bb_prepare_tfMRI_' + subject + '" -l ' + logDir + ' -j ' + jobPOSTPROCESS + ' $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_tfMRI ' + subject + ' ' + GDC_Status + ' ' + Machine)
        jobFEAT_T =    LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 400 -N "bb_feat_tfMRI_'    + subject + '" -l ' + logDir + ' -j ' + jobPREPARE_T   + ' feat  ' + baseDir + '/fMRI/tfMRI.fsf')

        if jobsToWaitFor != "":
            jobsToWaitFor = jobsToWaitFor +',' +jobFEAT_T
        else:
            jobsToWaitFor = '' + jobFEAT_T

    else:
        logger.error("There is no tFMRI info. Thus, the Task Functional part will not be run")

    if jobsToWaitFor=="":
        jobsToWaitFor="-1"

    return jobsToWaitFor
