import pdb
import numpy as np

### for linear
##tau = np.linspace(0.13, 0.28, num=20)
##tau = tau[2:]
##fair_tau = tau[4]
##
### unfair
##filename = 'results/fair_k' + str(25) + '_' + str(0.28) + '_sim' + str(5) + '_int' + str(2) + '.npz'
##DICT = np.load(filename)
##unfair_sol = DICT['sol'].astype(int)
##
### fair
###filename = 'results/fair_k' + str(25) + '_' + str(fair_tau) + '_sim' + str(5) + '_int' + str(2) + '.npz'
###DICT = np.load(filename)
###fair_sol = DICT['sol'].astype(int)

# for max
#constrained
DICT = np.load('results/TAUS_frac.npz')
TAUS = DICT['TAUS']
#tau = np.linspace(0.04, 0.16, 20)
#tau = tau[1:]
fair_tau_max1 = TAUS[0]#tau[1]
filename = 'results/max_fair_k' + str(25) + '_' + str(fair_tau_max1) + '_sim' + str(5) + '_frac.npz'
DICT = np.load(filename)
fair_max_sol1 = DICT['sol'].astype(int)

fair_tau_max2 = TAUS[10]
filename = 'results/max_fair_k' + str(25) + '_' + str(fair_tau_max2) + '_sim' + str(5) + '_frac.npz'
DICT = np.load(filename)
fair_max_sol2 = DICT['sol'].astype(int)

#unconstrained
unfair_tau = TAUS[-1]
filename = 'results/max_fair_k' + str(25) + '_' + str(unfair_tau) + '_sim' + str(5) + '_frac.npz'
DICT = np.load(filename)
unfair_sol = DICT['sol'].astype(int)

n = len(fair_max_sol1)

filename = 'results/max_parity_k' + str(25) + '_sim' + str(5) + '_frac' 
DICT = np.load(filename + '.npz')
parity_sol = DICT['sol'].astype(int)

fr = open('final_data_interventions_max_frac.csv','r') 
fw = open('final_data_interventions_max_frac_results.csv','w')
i = 0
for line in fr:
    line = line.strip()
    if i == 0:
        line += ",int_parity"
        line += ",int_unfair"
        line += ",int_max_fair1"
        line += ",int_max_fair2\n"
        fw.write(line) 
        i = i+1
        continue
    line += "," + str(parity_sol[i-1])
    line += "," + str(unfair_sol[i-1])
    line += "," + str(fair_max_sol1[i-1])
    line += "," + str(fair_max_sol2[i-1]) + "\n"
    i = i + 1
    fw.write(line)
fw.close()
fr.close()
    


filename = 'results/max_minority_k' + str(25) + '_sim' + str(5) + '_frac'
DICT = np.load(filename + '.npz')
sol = DICT['sol'].astype(int)





fr = open('final_data_interventions_max_frac_minority.csv','r')
fw = open('final_data_interventions_max_frac_minority_results.csv','w')
i = 0
for line in fr:
    line = line.strip()
    if i == 0:
        line += ",int\n"
        fw.write(line) 
        i = i+1
        continue
    line += "," + str(sol[i-1]) + "\n"
    i = i + 1
    fw.write(line)
fw.close()
fr.close()


