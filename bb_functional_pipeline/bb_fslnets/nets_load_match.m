
function [LoadedMatched] = nets_load_match(infile,to_match);

grot=load(infile);
LoadedMatched = zeros(size(to_match,1),size(grot,2)-1) / 0;
[~,grotI,grotJ]=intersect(grot(:,1),to_match(:,1));
LoadedMatched(grotJ,:)=grot(grotI,2:end);

