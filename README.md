UK_biobank_pipeline
===================

The `UK_biobank_pipeline` project is a processing pipeline written mainly in Python and bash. It uses [FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) as the basic building blocks.


Dependencies
------------

Most of the dependencies of `UK_biobank_pipeline` are listed in the [requirements.txt](requirements.txt) file.

One additional dependency - [gradunwarp](bb_python/python_installation/gradunwarp_FMRIB.tar.gz) - can be installed with a provided [installation script](bb_python/python_installation/install_bb_python.sh) 


Documentation
-------------

`UK_biobank_pipeline` is explained in detail in the paper [Image Processing and Quality Control for the first 10,000 Brain Imaging Datasets from UK Biobank](http://www.biorxiv.org/content/early/2017/04/24/130385).

First install the UK_Biobank Python Conda Environment by going into the `bb_python/python_installation` directory and calling `./install_bb_python.sh` (which by default installs the recommended python 3.5.1). Then, set the paths in the `init_vars` script and source it from the parent UK-Biobank-pipeline directory.

*. init_vars*

This will activate the UKBB Conda environment. We can then run the pipeline. Once NIFTIs are available, the pipeline can be called using `bb_pipeline.py` (in the bb_pipeline_tools folder, but should be added to PATH by init_vars). So:

*bb_pipeline.py subjectFolder*

where subjectFolder contains the input NIFTI files for a given subject. Notice that the current version of the pipeline expects that subjectFolder is within the parent UKB-pipeline directory (i.e. within $BBDIR).

Notice that the original version performs *gradient non-linearity corrections* on the data using scanner-specific files. In this version, we have turned off the grad-nonlin corrections.

Finally, make sure to add the following three files with `pre-trained models (for BIANCA and FIX)`, following the instructions from https://www.fmrib.ox.ac.uk/ukbiobank/fbp. And copy the two template melodic files from https://www.dropbox.com/s/9fhunsxaetz804n/UKBB_Melodic_IC_templates.zip?dl=0 to the `templates/group` folder.


Input Requirements
------------------

The pipeline assumes NIFTI inputs with a specific filename convention. Therefore, it is recommended to perform `Dicom to Nifti conversion` in a certain way using `dcm2niix`. The recommended call is:

*dcm2niix -b y -z y -f %p_coil%a_echo%e_%2s -o $OutputNIFTIFolder $InputDICOMFolder*

The `minimum input` required to run the pipeline is a T1w image. The pipelines for each modality have their own expectations.


*  **T1w Input**: Ideally a T1w with prescan corrections for non-uniform receiver coil profiles is expected. I.e. Siemens' Prescan Normalize, GE's PURE or Philips' CLEAR. The nifti input filename should start with "T1" (or "t1"). Also, the corresponding .json file should have a value "NORM" amongst the values for entry "ImageType".
*  **T2w Input**: Ideally a T2w with prescan corrections for non-uniform receiver coil profiles is expected. I.e. Siemens' Prescan Normalize, GE's PURE or Philips' CLEAR. The nifti input filename should start with "T2_FLAIR" (or "t2_flair"). Also, the corresponding .json file should have a value "NORM" amongst the values for entry "ImageType".
*  **DMRI Input and SE-fieldmaps**: A pair of blip-reversed dMRI acquisitions is expected, with at least one pair of blip-reversed b0s to be used as a Spin-Echo fieldmap. The nifti input filenames whould start with "diff_AP" and "diff_PA". Each of them should be accompanied with a corresponding .bval and .bvec file (notice that the dcm2niix conversion for some vendors does not return a bval/bvec for dMRI scans that contain only b0s, so this needs to be added manually).