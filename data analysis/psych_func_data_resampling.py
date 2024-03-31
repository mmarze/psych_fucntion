# Marcin J Marzejon
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
import plotly.express as px

# file_path – path to the dictionary with all measurements data
file_path = sorted(glob.glob(r" #your_path# /*.txt"))
# coeff – ratio of power levels: @pupil plane and measured by power meter in system
coeff = [ #measured values# ]
# thrv – threshold value for a given simulation
thrv = [ #measured values# ]

# read the file, skip the header and unnecessary rows, sort by brightness and replace Y/N with 1/0
# M - number of brightness levels
M=12
# k -number of queries for each brightness level
k=10
df=pd.DataFrame()
i=0

for elem in file_path:
    print(elem)
    buf_data=pd.read_csv(elem, sep='\t', header=6)
    buf_data=buf_data.iloc[:-M-3, 2:5]
    buf_data=buf_data.iloc[-M*k:]
    buf_data=buf_data.replace(to_replace='Y', value=1)
    buf_data=buf_data.replace(to_replace='N', value=0)
    buf_data['Dataset']=i
    buf_data['Coeff']=coeff[i]
    buf_data['Thr']=thrv[i]
    df=df.append(buf_data)
    i=i+1

# recalculate power levels as log values at the pupil plane
df['log10(Pout)']=np.log10(df['Power [W]']*df['Coeff'])
# normalization of the log10(Pout) levels
df['log10(Pout)Norm']=df['log10(Pout)']-df['Thr']

# Combining and resampling
# plot the histogram of brightness levels
fig=px.histogram(df, x='log10(Pout)')
fig.update_layout(bargap=0.2)
fig.show()

# step – bin size on the histogram (VIS – 0.1, IR – 0.05)
step = 0.1
# set new brightness levels
for i in range(len(df)):
    df['#brightness'].iloc[i]=np.floor(df['log10(Pout)Norm'].iloc[i]/step)
df['#brightness']=df['#brightness']-df['#brightness'].min()
# sort dataframe by brightness values
df['#brightness']=df['#brightness'].astype(int)
df.sort_values(by='#brightness')

# calculate parameters for simulations
results = np.zeros((df['#brightness'].max()+1,9))
for i in range(df['#brightness'].max()+1):
    results[i][0]=i
    results[i][1]=df[df['#brightness']==i]['log10(Pout)Norm'].mean()
    results[i][2]=df[df['#brightness']==i]['log10(Pout)Norm'].std()
    results[i][3]=df[df['#brightness']==i]['log10(Pout)Norm'].min()
    results[i][4]=df[df['#brightness']==i]['log10(Pout)Norm'].max()
    results[i][6]=df[df['#brightness']==i]['Answer [Y/N]'].sum()
    results[i][7]=df[df['#brightness']==i]['Answer [Y/N]'].count()
    if i>0:
        results[i][5]=results[i][3]-results[i-1][4]
        results[i][8]=results[i][1]-results[i-1][1]

# results as a dataframe. Drop rows for OutOfNumber==0
df_header=['#brightness', 'mean(log10(Pout)Norm)', 'std(log10(Pout)Norm)', 'min(log10(Pout)Norm)', 'max(log10(Pout)Norm)', 'margin', 'NofY', 'OutOfNumber', 'BRT step']
df_res=pd.DataFrame(results, columns=df_header)
df_res=df_res[df_res['OutOfNumber']!=0]df_res.dropna(axis=0, inplace=True)

# print lists of parameters for simulation
print(list(df_res['mean(log10(Pout))']))
print(list(df_res['NofY']))
print(list(df_res['OutOfNumber']))
