#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:09:00 2018

@authors: chris and matt

Find interventions that:
(a) maximize overall benefit, subject to parity constraints
(b) maximize minority benefit
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

def all_of_it(sim, TT, constraint_type):
    
    # 0. load data
    print('sim=' + str(sim))
    print('TT=' + str(TT))
    if constraint_type == "minority":
        _, _, S, X, A, A_oh, neigh = load.get_data(sim, 1)
    else:
        _, _, S, X, A, A_oh, neigh = load.get_data(sim, 0)
    A_ix = np.argmax(A,axis=1)

    n = S.shape[0]
    da = A.shape[-1]

    # 1. load weights of causal model
    DICT = np.load('school_weights_linear_mse_sim' + str(sim) + '_max1_frac.npz')
    w = DICT['w'].T
    w1 = w[0:da,:]
    w2 = w[da:da*2,:]
    w3 = w[da*2:da*3,:]
    w4 = w[da*3:da*4,:]
    neigh = neigh.astype(int)
    x1 = X[:,0]
    x3 = X[:,2]
    
     
    bit_mask=np.zeros([2**neigh.shape[1],neigh.shape[1]])
    ints=np.arange(2**neigh.shape[1],dtype=np.int)
    for i in range(neigh.shape[1]):
        bit_mask[:,i]=ints%2
        ints//=2
    
    
    def EY_inner(index,mask,a):
        neighS = S[index,neigh[index,:]]
        first  = np.dot(a,w1)*np.max(neighS*x1[neigh[index,:]])
        second = np.dot(a,w2)*np.max(neighS*mask)
        third  = np.dot(a,w3)*x3[index]
        fourth = np.dot(a,w4)
        return first + second + third + fourth
    
    def f(index,mask,constraint=0):
        return EY_inner(index,mask,A[np.newaxis,index,:])

    def get_weights(i,newf=f,constraint=0):
        weights=np.empty(bit_mask.shape[0])
        for r in range(bit_mask.shape[0]):
            weights[r]=newf(i,bit_mask[r],constraint)
        return weights
        
    
    all_times = []
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
    print('null allocation')
    print('obj_true: ' + str(obj))
    print('max_const: ' + str(np.max(const)))
    if constraint_type == "minority":
        filename = 'results/null_sim' + str(sim) + '_frac_minority'
        np.savez_compressed(filename, obj=obj, const=const)
    else:
        filename = 'results/null_sim' + str(sim) + '_frac'
        np.savez_compressed(filename, obj=obj, const=const)
    pdb.set_trace()


    for t in range(TT):
        print('t=' + str(t))
        start = time.time()
        #Now build variables
        model = gb.Model()
        
        interventions=model.addVars(np.arange(neigh.shape[0]),
                                              lb=0,#np.zeros(neigh.shape[0]),
                                              ub=1,#np.ones(neigh.shape[0]),
                                              vtype=gb.GRB.BINARY)
        K = 25 
        expr = gb.LinExpr()
        for i in range(n):
            expr += interventions[i]
        model.addConstr(expr, gb.GRB.LESS_EQUAL, K, "k")

        if constraint_type == "parity":
            parity0 = gb.LinExpr()
            for i in range(n):
                if A_oh[i,0] != 0:
                    parity0 += interventions[i]
            model.addConstr(parity0, gb.GRB.EQUAL, K//3, "parity0")
            parity1 = gb.LinExpr()
            for i in range(n):
                if A_oh[i,1] != 0:
                    parity1 += interventions[i]
            model.addConstr(parity1, gb.GRB.EQUAL, K//3, "parity1")
            parity2 = gb.LinExpr()
            for i in range(n):
                if A_oh[i,2] != 0:
                    parity2 += interventions[i]
            model.addConstr(parity2, gb.GRB.EQUAL, K//3, "parity2")
        
        
        def add_constrained_aux(index):
            weights=get_weights(index)
            
            ##counter=np.empty((3,weights.shape[0]))
            ##counter[:]=weights[np.newaxis]
            ##for i in range(3):
            ##    counter[i]-=get_weights(index,count_f,i)
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
            ##if tau is not False:
            ##    for i in range(3):
            ##        model.addConstr(sum(aux[f]*counter[i,f] for f in range(weights.shape[0]))<=tau)
            return aux
            
        aux = list(map(lambda x: add_constrained_aux(x),range(neigh.shape[0])))
        
            
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
        if constraint_type == "parity":
            filename = 'results/max_parity_k' + str(K) + '_sim' + str(sim) + '_frac'
            timename = 'results/time_parity_k' + str(K) + '_sim' + str(sim) + '_t' + str(t+1) + '_frac'
        elif constraint_type == "minority":
            filename = 'results/max_minority_k' + str(K) + '_sim' + str(sim) + '_frac'
            timename = 'results/time_minority_k' + str(K) + '_sim' + str(sim) + '_t' + str(t+1) + '_frac'
        else:
            print('err')
            pdb.set_trace()
        model.write(filename + '.lp')
        np.savez_compressed(filename, sol=sol)
        print('done!')
        print('A dist')
        print(np.sum(A_oh[sol,:],axis=0))
        print(all_times)
        np.savez_compressed(timename, times=all_times)


if __name__ == '__main__':
    all_of_it(5, 1, "parity")
    #all_of_it(5, 1, "minority")
