
% nets_unconfound(y,conf) 
% nets_unconfound(y,conf,-1) 
% regresses conf out of y, handling missing data
% data, confounds and output are all demeaned unless the "-1" option is included

function yd=nets_unconfound(y,conf,varargin)

DEMEAN=1;
if nargin==3
  DEMEAN=0;
end

if DEMEAN
  y = nets_demean(y);
  conf = nets_demean(conf);
end

if sum(isnan(y(:)))+sum(isnan(conf(:))) == 0   % if there's no missing data, can use faster code

  conf=nets_svds(conf,rank(conf)); beta=pinv(conf)*y; beta(abs(beta)<1e-10)=0; yd=y-conf*beta;

  if DEMEAN
    yd = nets_demean( yd );
  end

else

  yd = (y*0)/0; % set to all NaN because we are not going to necessarily write into all elements below

  for i=1:size(y,2)
    grot=~isnan(sum([y(:,i) conf],2));
    grotconf = conf(grot,:);
    if DEMEAN
      grotconf=nets_demean(grotconf);
    end

    grotconf=nets_svds(grotconf,rank(grotconf)); beta=pinv(grotconf)*y(grot,i); beta(abs(beta)<1e-10)=0; yd(grot,i)=y(grot,i)-grotconf*beta;

    if DEMEAN
      yd(grot,i) = nets_demean( yd(grot,i) );
    end
  end

end

