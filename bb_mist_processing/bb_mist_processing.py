#!/bin/env python

import bb_pipeline_tools.bb_logging_tool as LT
import os.path



def bb_mist_processing(subject, jobHold, fileConfiguration, dMRI_MIST_Status):
    logger = LT.initLogging(__file__, subject)
    logDir  = logger.logDir
    baseDir = logDir[0:logDir.rfind('/logs/')]

    jobPREPARE =      LT.runCommand(logger, '${FSLDIR}/bin/fsl_sub -T 100   -N "bb_mist_processing_'            + subject + '" -j ' + jobHold        + '  -l ' + logDir + ' $BB_BIN_DIR/bb_mist_processing/bb_mist_processing ' + subject + " " + dMRI_MIST_Status)


