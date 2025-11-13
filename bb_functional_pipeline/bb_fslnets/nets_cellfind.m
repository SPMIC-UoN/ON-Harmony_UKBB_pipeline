%
% nets_cellfind - find a string in an array of cells
% Steve Smith 2015-2019
%
% cellindex = nets_cellfind(cellarray,string); 
% cellindex = nets_cellfind(cellarray,string,1); % turn on "wild" (any match anywhere) searching
%

function [cellindex] = nets_cellfind(cellarray,string,varargin);

cellindex=[]; % default return if nothing found

% first check for perfect complete matches and return if any found
for i=1:length(cellarray)
  if strcmp(cellarray{i},string)==1
    cellindex=[cellindex i];
  end
end

% then check for matches where the *start* of items in cellarray match; return if any found
if isempty(cellindex)
  for i=1:length(cellarray)
    if strncmp(cellarray{i},string,length(string))==1
      cellindex=[cellindex i];
    end
  end
end

%%% then check for *any* match within items in cellarray match (if this option turned on)
if nargin==3 & isempty(cellindex)
  for i=1:length(cellarray)
    if ~isempty(strfind(cellarray{i},string))
      cellindex=[cellindex i];
    end
  end
end

