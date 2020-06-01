UK_biobank_pipeline
===================

The `UK_biobank_pipeline` project is a processing pipeline written mainly in Python and bash. It uses [FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) as the basic building blocks.


Dependencies
------------

Most of the dependencies of `UK_biobank_pipeline` are listed in the [requirements.txt](requirements.txt) file.

All additional dependencies can be installed with a provided [installation script](bb_python/python_installation/install_bb_python.sh)


Documentation
-------------

`UK_biobank_pipeline` is explained in detail in the paper [Image Processing and Quality Control for the first 10,000 Brain Imaging Datasets from UK Biobank](http://www.biorxiv.org/content/early/2017/04/24/130385).

First install the UK_Biobank Python Conda Environment by going into the `bb_python/python_installation` directory and calling `./install_bb_python.sh` (which by default installs the recommended python 3.5.1). Then, set the paths in the `init_vars` script and source it from the parent UK-Biobank-pipeline directory.

*. init_vars*

This will activate the UKBB Conda environment. We can then run the pipeline. Once NIFTIs are available, the pipeline can be called using `bb_pipeline.py` (in the bb_pipeline_tools folder, but should be added to PATH by sourcing init_vars). So:

GDC (gradient non linearity corrections) should be turned on for SIEMNS scanners. (The scanner coeff files should be copied into bb_data). For non Siemens scanners we have trusted the GDC performed by the scanner and can turn this off.

*bb_pipeline.py subjectFolder*

where subjectFolder contains the input NIFTI files for a given subject.


The folling bmri_group_means.zip should be downloaded from http://biobank.ctsu.ox.ac.uk/showcase/refer.cgi?id=9028 and extracted into the following directory bb_functional_pipeline/bb_fslnets

Finally,  add the following "UKBiobank.RData." for FIX (BIANCA files already done) from https://www.fmrib.ox.ac.uk/ukbiobank/fb into templates/group folder.

Input Requirements
------------------

The pipeline assumes NIFTI inputs with a specific filename convention. Therefore, it is recommended to perform `Dicom to Nifti conversion` in a certain way using `dcm2niix`. The recommended call is:

*dcm2niix -b y -z y -f %p_coil%a_echo%e_%2s -o $OutputNIFTIFolder $InputDICOMFolder*

The `minimum input` required to run the pipeline is a T1w image. The pipelines have their specific expectations for each modality, as explained below. In general, however, all input filenames should follow the above convention, i.e. filenames should finish with echoX_Y, where X and Y are only numbers. For some GE conversions, this convention does not hold, so filenames should be edited manually.

*  **T1w Input**: Ideally a T1w with prescan corrections for non-uniform receiver coil profiles is expected. I.e. Siemens' Prescan Normalize, GE's PURE or Philips' CLEAR. The nifti input filename should start with "T1" (or "t1"). Also, the corresponding .json file should have a value "NORM" amongst the values for entry "ImageType".
*  **T2w Input**: Ideally a T2w with prescan corrections for non-uniform receiver coil profiles is expected. I.e. Siemens' Prescan Normalize, GE's PURE or Philips' CLEAR. The nifti input filename should start with "T2_FLAIR" (or "t2_flair"). Also, the corresponding .json file should have a value "NORM" amongst the values for entry "ImageType".
*  **DMRI Input and SE-fieldmaps**: A pair of blip-reversed dMRI acquisitions is expected, with at least one pair of blip-reversed b0s to be used as a Spin-Echo fieldmap. The nifti input filenames whould start with "diff_AP" and "diff_PA". Each of them should be accompanied with a corresponding .bval and .bvec file (notice that the dcm2niix conversion for some vendors does not return a bval/bvec for dMRI scans that contain only b0s, so this needs to be added manually). Notice that each of the diff_AP and diff_PA should have at least two volumes and diff_AP is typically the larger of the two files. In the case of single b0 volume image for diff_PA, simply use fslmerge to duplicate the number of volumes (and adjust bval and bvec files accordingly). Also, the corresponding .json files should have an entry ""EffectiveEchoSpacing" with the Echo spacing in seconds given the sequence parameters (i.e. a line inserted like: "EffectiveEchoSpacing": 0.00067, ).
Finally, the pipeline expects that all b-value entries in the .bval files are integers. Philips tends to populate b0 entries with decimals "0.00X", so these need to be replaced with "0".
*  **FMRI resting-state**: A single nifti file with all fMRI volumes is expected and the input filename should contain '\*FMRI\*RESTING*.nii.gz'. The corresponding .json files should have an entry ""EffectiveEchoSpacing" with the Echo spacing in seconds (i.e. a line inserted like for example: "EffectiveEchoSpacing": 0.00054, ).

`dcm2niix and Philips dMRI incompatibility!!` It looks that the latest versions of Philips software and dcm2niix induce a weird behaviour. Once nifti conversion is performed for dMRI data, the sequence of volumes is flipped compared to the acquisition (i.e. last acquired volume appears first in the nifti and so forth). This is OK in general, but could create issues for distortion correction tools that typically assume that the first volume of a dMRI scan is a b=0. To avoid strange behaviour of scripts, take the last volume (which will be a b=0) and put it at the beginning of the dMRI file (changing accordingly the respective entries of the .bval and .bvec file)

**NODDI cuDIMOT**

NODDI (Watson) cudDIOMOT tool is used to give NODDI outputs.

Installation instructions found at: https://users.fmrib.ox.ac.uk/~moisesf/cudimot/Installation.html and save the "bin" folder in the following path:  
*export CUDIMOT="${BB_BIN_DIR}/bb_diffusion_pipeline/bb_NODDI_cuDIMOT"*
