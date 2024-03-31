% Marcin J Marzejon
% based on: "Psychophysics. A practical Introduction" by F.A.A. Kingdom, N.
% Prisn, 2nd edition, Elsevier 2016, Chapter 4.2, pp. 56-71)

% clear all variables, terminal data, and close all opened Matlab widnows
clear; close all; clc

% Provide stimulus levels (in dB scale):
StimLevels = [ __your_data__ ];
% Provide number of 'yes' answers for various stimulus intensity. Match the
% order to StimLevels values.
NumDetected = [ __your_data__ ];
% number of trials at each brightness level:
NumTrials = [ __your_data__ ];
% recalculate measured answers into percent (fraction detected)
FracDetected = NumDetected./NumTrials;


%% FITTING
% Fitting parameters
% Import logistic fot from Palamedes toolbox. You can also choose another
% logistic function for your application.
PF = @PAL_Logistic;
% paramsFree specifies which of the four parametersd: a b, g, and l, are free 
% parameters, i.e., parameters that the algorithm will attempt to find the 
% best-fitting values for. We put 1 for a free parameter and 0 for a fixed 
% parameter.
% for paramsFree = [1 1 1 1], all parameters are free 
paramsFree = [1 1 1 1];

% provide the values range within the fit parameters will be searched
searchGrid.alpha = StimLevels(1):0.001:StimLevels(length(StimLevels));
searchGrid.beta = logspace(0,3,201);
searchGrid.gamma = 0:0.05:0.3;
searchGrid.lambda = 0:0.05:0.3;

% Fitting procedure
[paramsValues, LL, exitflag, output] = PAL_PFML_Fit(StimLevels, NumDetected,...
    NumTrials, searchGrid, paramsFree, PF);

% scenario': 1 indicates a succesful fit, a negative number indicates 
%       that the likelihood function does not contain a global maximum.
%       For more information, see below or visit
%       www.palamedestoolbox.org/understandingfitting.html

% paramsValues: 1x4 vector containing values of fitted and fixed 
%       parameters of the psychometric function [threshold slope guess-rate 
%       lapse-rate].
disp(['[threshold slope guess-rate lapse-rate] = ', num2str(paramsValues)]);
% LL - Log likelihood associated with the fit
disp(['LL = ', num2str(LL)]);
% exitflag - 1 indicates a succesful fit, a negative number indicates 
%       that the likelihood function does not contain a global maximum.
%       For more information, see below or visit
%       www.palamedestoolbox.org/understandingfitting.html
disp(['exitflag = ', num2str(exitflag)]);
% 'output': message containing some information concerning fitting process.
disp(output)

%% calculate points for fitted curve 
StimLevelsFine = min(StimLevels):(max(StimLevels)- min(StimLevels))/1000:max(StimLevels);
Fit = PF(paramsValues, StimLevelsFine);


%% PLOTTING RESULTS
figure
% plot fit
plot(StimLevelsFine,Fit,'k-','linewidth',2);
hold on;
% plot data points
plot(StimLevels, FracDetected,'r.','markersize',40);
set(gca, 'fontsize',12);
% plot/axis properties
axis([0 .12 .4 1]);
ylim([-0.1 1.1])
xlim auto
xlabel('Relative stimulus brightness [dB]');
ylabel('Fraction detected [%]');

%%  Bootstrap analysis of the fit
% B specifies how many times the routine should simulate the experiment
B = 400;
% run Bootstrap parametric analysis
[SD paramsSim LLSim converged] = ...
    PAL_PFML_BootstrapParametric (StimLevels, NumTrials, paramsValues,...
    paramsFree, B, PF, 'searchGrid', searchGrid);
%   'SD': 1x4 vector containing standard deviations of the PF's parameters
%       across the B fits to simulated data. These are estimates of the
%       standard errors of the parameter estimates.
disp(['SD: ' num2str(SD)])
%   'paramsSim': Bx4 matrix containing the fitted parameters for all B fits
%       to simulated data.
%   'LLSim': vector containing Log Likelihoods associated with all B fits
%       to simulated data.
%   'converged': For each simulation contains a 1 in case the fit was
%       succesfull (i.e., converged) or a 0 in case it did not.

% run goodness of fit analysis
[Dev pDev DevSim converged] = ...
    PAL_PFML_GoodnessOfFit(StimLevels,NumDetected,NumTrials,paramsValues,...
    paramsFree,B,PF,'searchGrid',searchGrid);

%   'Dev': Deviance (transformed likelihood ratio comparing fit of
%       psychometric function to fit of saturated model)
disp(['Dev: ' num2str(Dev)])
%   'pDev': proportion of the B Deviance values from simulations that were
%       greater than Deviance value of data. The greater the value of pDev,
%       the better the fit.
%   'DevSim': vector containing all B simulated Deviance values.
%   'converged': For each simulation contains a 1 in case the fit was
%       succesfull (i.e., converged) or a 0 in case it did not.

% Skipping INF vaues for slope SD value estimation (needed if number of samples is low)
paramsSim2 = paramsSim(isfinite((paramsSim(:,2))), 2);
disp([‘Slope SD: ' num2str(std(paramsSim2))])
