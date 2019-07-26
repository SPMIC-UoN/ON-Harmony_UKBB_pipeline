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

First install the UK_Biobank Python Conda Environment using `bb_python/python_installation/install_bb_python.sh` (which by default install the recommended python 3.5.1). Then, set the paths in the `init_vars` script.

We can then run the pipeline on theconverted NIFTIs using `bb_pipeline.py` from the bb_pipeline_tools folder. The pipeline assumes NIFTI inputs with a specific filename convention. 
Therefore, perform `Dicom to Nifti conversion` in a certain way using `dcm2niix`. The recommended call is

*dcm2niix -b y -z y -f %p_coil%a_echo%e_%2s -o ../  $DICOMFolder*
