# Marcin J. Marzejon, Sep 2023
from outliers import smirnov_grubbs as grubbs
from scipy import stats
import numpy as np

# data
vis_beta_P1=[ __obtained_values__ ]
ir_beta_P1=[ __obtained_values__ ]
vis_beta_P26=[ __obtained_values__ ] 
ir_beta_P26=[ __obtained_values__ ]
vis_beta_P36=[ ___obtained_values__ ]
ir_beta_P36=[ __obtained_values__ ]

vis_beta=vis_beta_P1+vis_beta_P26+vis_beta_P36
ir_beta=ir_beta_P1+ir_beta_P26+ir_beta_P36

# Grubb’s test for outliers
# Grubb’s test for outliers. Null hypothesis (H0): there is no outlier in the data.  
# Alternative hypothesis (Ha): there is an outlier in the data. Interpretation: For p>0.05, 
# there is no outlier in the data.
vis_beta=grubbs.test(np.array(vis_beta), alpha=0.05)
ir_beta=grubbs.test(np.array(ir_beta), alpha=0.05)

# Data normality test – Shapiro-Wilk Normality Test
# Shapiro-Wilk test for data normality. Null hypothesis (H0): the sample comes from a normal 
# distribution. Alternative hypothesis (Ha): the sample does not come from a normal # distribution. Interpretation: For p>0.05, normality is assumed.
print(stats.shapiro(vis_beta))
print(stats.shapiro(ir_beta))

# Bartlett’s test for equal variances
# Test to Compare Two Variances for normal populations. Null hypothesis (H0): the variances of # the two groups are equal. Alternative hypothesis (Ha): the variances are different. # Interpretation: For p>0.05, there is no significant difference between the two variances.
print(stats.bartlett(vis_beta, ir_beta))

# Welch Test
# Non-paired Welch Two Sample t-test. Null hypothesis (H0): two population means are equal. # Alternative hypothesis (Ha): two population means are not equal. Interpretation: For p>0.05, # there is no significant difference between the means of two populations.
print(stats.ttest_ind(vis_beta, ir_beta, equal_var=False))

# Beta coefficients ratio and SD
print('The ratio of the beta coefficients (vis/ir): ',np.mean(ir_beta)/np.mean(vis_beta) )
print('SD: ', np.sqrt(np.power((np.std(ir_beta)/np.mean(ir_beta)),2) + np.power((np.std(vis_beta)/np.mean(vis_beta)),2)))
