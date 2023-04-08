import numpy as np
import pandas as pd
pd.set_option("display.precision", 10)

# Expreimental parameters - parameters to change
# file_path - path to the file
file_path = r"/Users/marcin/Desktop/Wed, Mar 15, 2023_2.25.38 PM.txt"
# M - number of brightness levels
M = 12
# k - number of queries for each brightness level
k = 10

# read file and skip the header
exp_data = pd.read_csv(file_path, sep='\t', header=6)
# skip unnecessary rows at the end of the file
exp_data = exp_data.iloc[:-M-1, 2:]
# select psychometric measurement datapoints
exp_data = exp_data.iloc[-M*k:]
# sort the dataset
exp_data = exp_data.sort_values(by='#brightness', axis=0, ascending=True)
# replace Y/N with 1/0 values
exp_data = exp_data.replace(to_replace='Y', value=1)
exp_data = exp_data.replace(to_replace='N', value=0)

# result data container
results = np.zeros((M,4))
# Calculate mean power level, std(power level) and fraction detected stimuli
for i in range(0, M):
    results[i, 0] = exp_data.iloc[k*i:k*(i+1), 1].mean()
    results[i, 1] = exp_data.iloc[k*i:k*(i+1), 1].std()
    results[i, 2] = exp_data.iloc[k*i:k*(i+1), 2].sum()
    results[i, 3] = exp_data.iloc[k*i:k*(i+1), 2].sum()*10
# converts results to pd.DataFrame 
results = pd.DataFrame(results, columns=['mean power [W]', 'power std [W]', 
                                    'No yes answers', 'fraction detected [%]'])
# save results to file
file_path2 = file_path[:-3] + 'xlsx'
results.to_excel(file_path2)