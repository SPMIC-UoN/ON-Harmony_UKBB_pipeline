%
%
% Script name: swiProcessing.m
%
% Description: Matlab function to run the swMRI processing of Phillips
% scanners where the coils are already combined
%
% Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson
%
% Copyright 2017 University of Oxford
%
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
%
%    http://www.apache.org/licenses/LICENSE-2.0
%
% Unless required by applicable law or agreed to in writing, software
% distributed under the License is distributed on an "AS IS" BASIS,
% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
% See the License for the specific language governing permissions and
% limitations under the License.
%

function swiProcessing(dirName)

  magImgDir=[dirName '/SWI/'];
  phaImgDir=[dirName '/SWI/'];

  magImgFiles=dir([magImgDir 'SWI_TOTAL_MAG_TE2.nii.gz']); 
  phaImgFiles=dir([phaImgDir 'SWI_TOTAL_PHA_TE2.nii.gz']); %For GE this is filtered phase

  %chaDim = size(magImgFiles,1)-2;

  %% read one data set for getting the header
  magImgFileName = [dirName,'/SWI/SWI_TOTAL_MAG_TE2.nii.gz'];
  [magImg dims voxsize] = read_avw(magImgFileName);  magImgNOBIAS=magImg;
  xDim = size(magImg,1);
  yDim = size(magImg,2);
  zDim = size(magImg,3);

  %% build Hanning filter of 96 dim (won't be needed for GE)
  w=window2(97,97,@hann); % because of symetry
  filterLP = zeros(xDim,yDim);
  filterLP(xDim/2+1-96/2:xDim/2+1+96/2,yDim/2+1-96/2:yDim/2+1+96/2) = w;

  SOSImg = zeros(xDim,yDim,zDim);
  complexAvg = complex(zeros(xDim,yDim,zDim),zeros(xDim,yDim,zDim));

  %% loop over channels (NOT looping for non-siemens scanners so for loop removed)

  magImgFileName = [magImgDir,magImgFiles.name];
  phaImgFileName = [phaImgDir,phaImgFiles.name];
  magImg = read_avw(magImgFileName);
  unix(['${FSLDIR}/bin/fslmaths ' phaImgDir '/SWI_TOTAL_PHA_TE2.nii.gz -div 1000 ' phaImgDir '/SWI_TOTAL_PHA_TE2.nii.gz ']); %before reading in scale the intensity
  phaImg = read_avw(phaImgFileName);
  
  %phaImg = -pi*(phaImg - 2048)/2048;
  %phaImg = -pi*(phaImg - 1048)/1048

  complexImg = magImg .* exp(1i*phaImg); %
  phase1 = angle(complexImg);
  mag1 = abs(complexImg);
  %fname=[dirName '/SWI/phase1.nii.gz'];   save_avw(phase1,fname,'f',voxsize);  call_fsl(['fslcpgeom ' phaImgFileName ' ' fname]);
  %fname=[dirName '/SWI/mag1.nii.gz'];   save_avw(mag1,fname,'f',voxsize);  call_fsl(['fslcpgeom ' phaImgFileName ' ' fname]);

  %unix(['${FSLDIR}/bin/prelude -c ' subj_dir '/SWI/complexImg_tmp.nii.gz -u complexImg.nii.gz '])
  %complexImgFileName = [dirName,'/SWI/complexImg_tmp.nii.gz'];
  %complexImg = read_avw(complexImgFileName);
%   phaseHP = zeros(xDim,yDim,zDim);
%     for zInd = 1:zDim
%       complexFFT = fftshift(fft2(ifftshift(complexImg(:,:,zInd))));
%       complexFFT = complexFFT.*filterLP;
%       complexImgLP = fftshift(ifft2(ifftshift(complexFFT)));
%       phaseHP(:,:,zInd) = angle(complexImg(:,:,zInd).*conj(complexImgLP));
%     end
%   complexAvg = magImg.*exp(1i*phaseHP);

  SOSImg = SOSImg.^0.5;
  filteredPha = phaImg;

  maskSWI = zeros(xDim,yDim,zDim);
  maskSWI(filteredPha>0) = 1;
  maskSWI(filteredPha<=0) = 1+filteredPha(filteredPha<=0)/pi;
  maskSWI = maskSWI.^4;
  SWI = magImgNOBIAS.*maskSWI;  % using prescan-normalised mag image instead of bias-fielded SOS

  fname=[dirName '/SWI/filtered_phase.nii.gz'];   save_avw(filteredPha,fname,'f',voxsize);  call_fsl(['fslcpgeom ' phaImgFileName ' ' fname]);
  fname=[dirName '/SWI/SWI.nii.gz'];              save_avw(SWI,fname,'f',voxsize);          call_fsl(['fslcpgeom ' phaImgFileName ' ' fname]);
