import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

T_KN = 21
T_ZN = 19.3
T_TS = 20
S_KN = 33.85
S_ZN = 36.052
S_TS = 33.66
S_NORM = 35
NO3 = 4.5e-5

df = pd.read_csv(r'C:\\Users\\Omid\\Desktop\\SIO 179\\Nitrate\\DataSampled(11-12).csv')
Intensity_signal_data = df[['Lambda',
                            'Idark(DI Lamp Off)',
                            'Iblank(DI Lamp On)',
                            'Ikn(Nitrate = 45,Salinity = 33.885)',
                            'Izn(Zero Nitrate,Salinity = 36.052)',
                            'Ich(DI Water,Salinity = 0,Nitrate = 45)',
                            'Its(Tank Water, First week sampled)']] 
Lambda = df['Lambda'].to_numpy()
Idark = df['Idark(DI Lamp Off)'].to_numpy()
Iblank = df['Iblank(DI Lamp On)'].to_numpy()
Ikn = df['Ikn(Nitrate = 45,Salinity = 33.885)'].to_numpy()
Izn = df['Izn(Zero Nitrate,Salinity = 36.052)'].to_numpy()
Its = df['Its(Tank Water, First week sampled)'].to_numpy()



fig, a = plt.subplots()
a.plot(Lambda[32:92], Idark[32:92],'-', label='Idark')
a.plot(Lambda[32:92], Iblank[32:92],'-', label='Iblank')
a.plot(Lambda[32:92], Ikn[32:92],'-', label='Ikn')
a.plot(Lambda[32:92], Izn[32:92],'-', label='Izn')
a.plot(Lambda[32:92], Its[32:92],'-', label='Its')
plt.title('Intensity Graph')
plt.xlabel('Lambda')
plt.ylabel('Intensity')
legend = a.legend(loc='upper left', shadow=True, fontsize='large')
#legend.get_frame().set_facecolor('C0')
plt.show()

##########################################################################################################################
A_kn = np.log((Ikn - Idark)/
                  (Iblank - Idark)) * -1
A_zn = np.log((Izn - Idark)/
                  (Iblank - Idark)) * -1
A_ts = np.log((Its - Idark)/
                  (Iblank - Idark)) * -1


slope, intercept, r_value, p_value, std_err = stats.linregress(Lambda[86:123],A_kn[86:123])
A_kn = A_kn - ((slope * Lambda) + intercept)

slope, intercept, r_value, p_value, std_err = stats.linregress(Lambda[86:123],A_zn[86:123])
A_zn = A_zn - ((slope * Lambda) + intercept) 

slope, intercept, r_value, p_value, std_err = stats.linregress(Lambda[86:123],A_ts[86:123])
A_ts = A_ts - ((slope * Lambda) + intercept) 


fig, b = plt.subplots()
b.plot(Lambda[32:92], A_kn[32:92],'-', label='A_kn')
b.plot(Lambda[32:92], A_zn[32:92],'-', label='A_zn')
b.plot(Lambda[32:92], A_ts[32:92],'-', label='A_ts')
plt.title('Absorbance Graph')
plt.xlabel('Lambda')
plt.ylabel('Absorbance')
legend = b.legend(loc='upper right', shadow=True, fontsize='large')
plt.show()

########################################################################################################################
ASW_kn = 1.1500276 + 0.0284 * T_KN * np.exp((-0.3101349+0.001222*T_KN)*(Lambda-210)) * S_KN / 35
ASW_zn = 1.1500276 + 0.0284 * T_ZN * np.exp((-0.3101349+0.001222*T_ZN)*(Lambda-210)) * S_ZN / 35
ASW_ts = 1.1500276 + 0.0284 * T_TS * np.exp((-0.3101349+0.001222*T_TS)*(Lambda-210)) * S_TS / 35

fig, c = plt.subplots()
c.plot(Lambda[32:92], ASW_kn[32:92],'-', label='ASW_kn')
c.plot(Lambda[32:92], ASW_zn[32:92],'-', label='ASW_kn')
c.plot(Lambda[32:92], ASW_ts[32:92],'-', label='ASW_kn')
plt.title('ASW Graph')
plt.xlabel('Lambda')
plt.ylabel('ASW')
legend = c.legend(loc='upper right', shadow=True, fontsize='large')
plt.show()
######################################################################################################################## 
ESW_zn_cal = A_zn / S_ZN
ESW_kn = (ESW_zn_cal * ASW_kn) / ASW_zn
ASE_kn = ESW_kn * S_ZN
ENO3 =  (A_kn - ASE_kn) / NO3


fig, d = plt.subplots()
d.plot(Lambda[48:92], ENO3[48:92],'-', label='ENO3-')
plt.title('ENO3- Graph')
plt.xlabel('Lambda')
plt.ylabel('ENO3-')
legend = d.legend(loc='upper right', shadow=True, fontsize='large')
plt.show()        
#######################################################################################################################          
ESW_ts_cal = A_zn / S_ZN
ESW_ts = (ESW_ts_cal * ASW_ts ) / ASW_zn
ASE_ts = ESW_ts * S_TS
Ap = A_ts - ASE_ts

fig, e = plt.subplots()
e.plot(Lambda[48:92], Ap[48:92],'-', label='Ap')
plt.title('Ap Graph')
plt.xlabel('Lambda')
plt.ylabel('Ap')
legend = e.legend(loc='upper right', shadow=True, fontsize='large')
plt.show()  
#######################################################################################################################
slope, intercept, r_value, p_value, std_err = stats.linregress(ENO3[48:86],Ap[48:86])
print('[NO3-] is: ', slope*1000000)
print(Lambda[48:86])
