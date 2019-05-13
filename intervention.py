#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:09:00 2018

@authors: chris and matt

Edit the functions f and counter_f
and the graph defined by neigh.
f takes an index and the state of a neighbourhood and returns a value
count_f takes the same, and a countervalue state indicated by the a number from
 0-3 indicated by the variable constraint.
N.B. The number of counterfactuals are hard-coded to 3
The objective is \sum_j f_j(X_j)
and
constraints are of the form  f_j(X_j) - count_f_j(X_j,a') <= Tau

where X_j is a binary subset of interventions.
"""

import gurobipy as gb
import numpy as np
import pdb
import gnureadline
import load
import argparse
import math, time

def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def timeSince(since):
    now = time.time()
    s = now - since
    return '%s' % (asMinutes(s))

#def get_arguments():
#    parser = argparse.ArgumentParser(description='interventions with constraints')
#    parser.add_argument('--frac', type=int, metavar='N', default="0")
#    return parser.parse_args()

def all_of_it(sim, frac, TT):
    #args = get_arguments()
    
    # load data
    #sim = 5
    #frac = args.frac
    print('sim=' + str(sim))
    print('frac=' + str(frac))
    print('TT=' + str(TT))
    _, _, S, X, A, neigh = load.get_data(sim, frac)
    _, _, _, _, A_oh, _  = load.get_data(sim, 0)
    n = S.shape[0]
    da = A.shape[-1]
    if frac:
        DICT = np.load('school_weights_linear_mse_sim' + str(sim) + '_max1_frac.npz')
    else:
        DICT = np.load('school_weights_linear_mse_sim' + str(sim) + '_max1.npz')
    w = DICT['w'].T
    
    # get weight matrix, for x2
    w1 = w[0:da,:]
    w2 = w[da:da*2,:]
    w3 = w[da*2:da*3,:]
    w4 = w[da*3:da*4,:]
    neigh = neigh.astype(int)
    # we just care about int_on for now
    x1 = X[:,0]
    x3 = X[:,2]
    
    A_ix = np.argmax(A,axis=1)
    
    bit_mask=np.zeros([2**neigh.shape[1],neigh.shape[1]])
    ints=np.arange(2**neigh.shape[1],dtype=np.int)
    for i in range(neigh.shape[1]):
        bit_mask[:,i]=ints%2
        ints//=2
    
    #Change me
    #scale=np.random.normal(0.5,1,n)# Junk scalar only used for stub of f
    #
    #def f(index,mask,constraint=0):
    #    #print('index=' + str(index))
    #    return scale[index]*mask.sum()
    #
    #def count_f(index,mask,constraint):
    #    #print('i=' + str(index))
    #    #print('const=' + str(constraint))
    #    return scale[index//(constraint+1)]*mask.sum()
    
    def EY(index,mask,a):
        neighS = S[index,neigh[index,:]]
        first  = w1[a]*np.max(neighS*x1[neigh[index,:]])
        second = w2[a]*np.max(neighS*mask)
        third  = w3[a]*x3[index]
        fourth = w4[a]
        return first + second + third + fourth
    
    def EY_inner(index,mask,a):
        neighS = S[index,neigh[index,:]]
        first  = np.dot(a,w1)*np.max(neighS*x1[neigh[index,:]])
        second = np.dot(a,w2)*np.max(neighS*mask)
        third  = np.dot(a,w3)*x3[index]
        fourth = np.dot(a,w4)
        return first + second + third + fourth
    
    def f(index,mask,constraint=0):
        if frac:
            return EY_inner(index,mask,A[np.newaxis,index,:])
        else:
            return EY(index,mask,A_ix[index])
        
    def count_f(index,mask,constraint):
        eya= EY(index,mask,constraint)
        return eya
    
    
    def get_weights(i,newf=f,constraint=0):
        weights=np.empty(bit_mask.shape[0])
        for r in range(bit_mask.shape[0]):
            weights[r]=newf(i,bit_mask[r],constraint)
        return weights
    
    #const = np.zeros((n,3))
    #for i in range(n):
    #    for a in range(3):
    #        const[i,a] = count_f(i,np.ones((neigh.shape[1],)),a)
    #
    all_times = []
    #TAUS = np.linspace(0.04, 0.16, 20)
    #TAU_DIFF = TAUS[1]-TAUS[0]
    #bb = [0.04-(a*TAU_DIFF) for a in np.arange(1,2)] #  we don't go all the way to 6 because it breaks for 2
    #bb = np.flip(bb, axis=0)
    #bb = np.array(bb)
    #cc = [0.16+(a*TAU_DIFF) for a in np.arange(1,6)]
    #cc = np.array(cc)
    #dd = [0.16+(a*TAU_DIFF) for a in np.arange(20,30)]
    #dd = [99999]
    #TAUS = [bb[0]]#np.concatenate((bb,cc))
    # NULL INTERVENTION
    def obj_temp(index,a):
        neighS = S[index,neigh[index,:]]
        first  = np.dot(a,w1)*np.max(neighS*x1[neigh[index,:]])
        #second = np.dot(a,w2)*np.max(neighS*mask)
        third  = np.dot(a,w3)*x3[index]
        fourth = np.dot(a,w4)
        return first + third + fourth
    def obj_counter(index,a):
        neighS = S[index,neigh[index,:]]
        first  = w1[a]*np.max(neighS*x1[neigh[index,:]])
        #second = w2[a]*np.max(neighS*mask)
        third  = w3[a]*x3[index]
        fourth = w4[a]
        return first + third + fourth

    obj = 0
    const = np.zeros((n,3))
    for i in range(n):
        obj_true = obj_temp(i,A[np.newaxis,i,:])
        const[i,0]  = obj_counter(i,0)
        const[i,1 ] = obj_counter(i,1)
        const[i,2]  = obj_counter(i,2)
        obj += obj_true
    pdb.set_trace()

    DICT = np.load('results/TAUS_frac.npz')
    TAUS = DICT['TAUS']
    print('new')
    print('TAUS=' + str(TAUS))
    for t in range(TT):
        print('t=' + str(t))
        for Tau in TAUS:#np.linspace(0.04, 0.16, 20):
            print('running tau=' + str(Tau))
            start = time.time()
            #Now build variables
            model = gb.Model()
            
            interventions=model.addVars(np.arange(neigh.shape[0]),
                                                  lb=0,#np.zeros(neigh.shape[0]),
                                                  ub=1,#np.ones(neigh.shape[0]),
                                                  vtype=gb.GRB.BINARY)
            K = 25 
            expr = gb.LinExpr()
            for i in range(len(interventions)):
                expr += interventions[i]
            model.addConstr(expr, gb.GRB.LESS_EQUAL, K, "k")
            
            
            counter_const=0
            
            def add_constrained_aux(index,tau=False):
                #init=z.copy()
                #init[-1]=1
                weights=get_weights(index)
                
                counter=np.empty((3,weights.shape[0]))
                counter[:]=weights[np.newaxis]
                for i in range(3):
                    counter[i]-=get_weights(index,count_f,i)
                aux= model.addVars(np.arange(bit_mask.shape[0]),#2**neigh.shape[1]),
                                   lb=0,ub=1,
                                   obj=weights,
                                   vtype=gb.GRB.CONTINUOUS)
                model.update()
                for i in range(bit_mask.shape[0]):
                    for j in range(bit_mask.shape[1]):
                        if bit_mask[i,j]:
                            model.addConstr(aux[i]<=interventions[neigh[index,j]])
                        else:
                            model.addConstr(aux[i]<=1-interventions[neigh[index,j]])
                model.addConstr(aux.sum()==1)
                if tau is not False:
                    for i in range(3):
                        model.addConstr(sum(aux[f]*counter[i,f] for f in range(weights.shape[0]))<=tau)
                return aux
            
            aux = list(map(lambda x: add_constrained_aux(x,tau=Tau),range(neigh.shape[0])))
            
                
            model.setObjective(model.getObjective(),gb.GRB.MAXIMIZE)
            model.optimize()
            end = timeSince(start)
            all_times.append(end)
        
            
            if model.status == gb.GRB.Status.OPTIMAL:
                sol = [interventions[i].X for i in range(len(interventions))]
                sol = np.array(sol)
                sol = np.round(sol)
                sol = sol.astype(bool)
            else:
                print('did not work')
                sol = []
            if frac:
                filename = 'results/max_fair_k' + str(K) + '_' + str(Tau) + '_sim' + str(sim) + '_frac'
                timename = 'results/time_max_k' + str(K) + '_sim' + str(sim) + '_t' + str(t+1) + '_frac'
            else:
                filename = 'results/max_fair_k' + str(K) + '_' + str(Tau) + '_sim' + str(sim)
                timename = 'results/time_max_k' + str(K) + '_sim' + str(sim) + '_t' + str(t+1)
            model.write(filename + '.lp')
            np.savez_compressed(filename, sol=sol)
            print('done!')
            print('A dist')
            print(np.sum(A_oh[sol,:],axis=0))
        print(all_times)
        np.savez_compressed(timename, times=all_times, tau=TAUS)#np.linspace(0.04, 0.16, 20))


if __name__ == '__main__':
    all_of_it(5, 1, 5)
