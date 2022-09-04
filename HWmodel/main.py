import numpy as np
import copy
import yaml

import my_module.create_tree as create
import my_module.calc_price as calc
import my_module.discount_factor as df

with open('./config/config.yaml','r') as yml:
    config=yaml.safe_load(yml)
    N=config["N"]
    delta_p=config["delta_p"]
    delta_t=config["delta_t"]
    T=config["T"]
    S_Rate=config["S_Rate"]
    N_monte=config["N_monte"]
    calc_method=config["calc_method"].lower()

with open('./config/config_tmp.yaml','r') as yml:
    config=yaml.safe_load(yml)
    a=config["a"]
    r_init=config["r_init"]
    sigma=config["sigma"]

h=3

#その他変数定義
N_T=T//delta_t
N=int(N*(delta_p//delta_t)+N_T)
V=sigma**2*delta_t
delta_r=np.sqrt(h*V)
M=-a*delta_t
if a==0:
    Max_node=1000000
else:
    Max_node=np.ceil(-(1-np.sqrt(1-1/h))/M)

discount_bond_price=df.discount_factor(delta_t,N)

HW_tree,trans_prob_tree=create.create_tree(a,r_init,h,M,Max_node,delta_t,delta_r,N,N_T,discount_bond_price)
#プライシング結果を代入する変数を定義
pricing_tree=copy.deepcopy(HW_tree)
#pricing_treeの初期化
for i in range(len(pricing_tree)):
    for node in range(-(len(pricing_tree[i])-1)//2,(len(pricing_tree[i])-1)//2+1):
        if i<N_T:
            pricing_tree[i][node]=0
        else:
            if (i-N_T)%(delta_p/delta_t)==0:
                pricing_tree[i][node]=HW_tree[i][node]-S_Rate
            else:
                pricing_tree[i][node]=0

if calc_method=="backward":
    result=calc.backward(HW_tree,trans_prob_tree,pricing_tree,delta_t)
elif calc_method=="montecarlo":
    result=calc.monte_calro(HW_tree,trans_prob_tree,pricing_tree,delta_t,N_monte)
    
print(round(result,2),"%")