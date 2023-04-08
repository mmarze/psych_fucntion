# psych_fucntion
Software for psychometric function measurement and data analysis

This project enables to:

1) Measure the psychophysical function for a visible stimulus using two-photon perimenetr described in here: https://doi.org/10.1364/BOE.411168. Experimental software is writtne in LabVIEW. It enables for real-time operations peripherial device (subject naswer response button, power meter, shutters, gradient filters, galvanometric scanners, motorized lenses etc). The psychophysical procedure is aa follows: (1) specify number of investigated brightness levels and number of querries at each level, (2) find the visual threshold using the method of adjustment (MOA), (3) calculate the optical power of stimuli based on the specified brightness levels, (4) perform psychophysical function measurement, (5) save results to txt file.
2) Process experimental data – get the distribution of yes/no answers at each brightness level. Also, calculate the real optical power level and its standard deviation.
3) Fit the experimental data in MATLAB using Palamedes toolbox (https://www.palamedestoolbox.org/).
