def backward(HW_tree,trans_prob_tree,pricing_tree,delta_t):
    import numpy as np
    for i in range(len(pricing_tree)-2,-1,-1):
        for node in range(-(len(pricing_tree[i])-1)//2,(len(pricing_tree[i])-1)//2+1):

            if node==(len(pricing_tree[i])-1)//2 and len(pricing_tree[i])==len(pricing_tree[i+1]):
                price_tmp=pricing_tree[i+1][node]*trans_prob_tree[i][node][0]
                price_tmp+=pricing_tree[i+1][node-1]*trans_prob_tree[i][node][1]
                price_tmp+=pricing_tree[i+1][node-2]*trans_prob_tree[i][node][2]

            elif node==-(len(pricing_tree[i])-1)//2 and len(pricing_tree[i])==len(pricing_tree[i+1]):
                price_tmp=pricing_tree[i+1][node+2]*trans_prob_tree[i][node][0]
                price_tmp+=pricing_tree[i+1][node+1]*trans_prob_tree[i][node][1]
                price_tmp+=pricing_tree[i+1][node]*trans_prob_tree[i][node][2]

            else:
                price_tmp=pricing_tree[i+1][node+1]*trans_prob_tree[i][node][0]
                price_tmp+=pricing_tree[i+1][node]*trans_prob_tree[i][node][1]
                price_tmp+=pricing_tree[i+1][node-1]*trans_prob_tree[i][node][2]
            pricing_tree[i][node]=price_tmp*np.exp(-HW_tree[i][node]*delta_t/100)+pricing_tree[i][node]
    return pricing_tree[0][0]

def monte_calro(HW_tree,trans_prob_tree,pricing_tree,delta_t,N_monte):
    import numpy as np
    price_list=[]
    Max_node=int((len(HW_tree[-1])-1)//2)
    for i in range(N_monte):
        rand_list=np.random.rand(len(pricing_tree)-1)
        current_node=0
        price=pricing_tree[0][current_node]
        
        for j in range(len(rand_list)):
            if current_node==Max_node:
                if 0<=rand_list[j]<trans_prob_tree[j][current_node][0]:
                    current_node=current_node
                
                elif trans_prob_tree[j][current_node][0]<=rand_list[j]<trans_prob_tree[j][current_node][0]+trans_prob_tree[j][current_node][1]:
                    current_node=current_node-1
                
                else:
                    current_node=current_node-2
                    
            elif current_node==-Max_node:
                if 0<=rand_list[j]<trans_prob_tree[j][current_node][0]:
                    current_node=current_node+2
                
                elif trans_prob_tree[j][current_node][0]<=rand_list[j]<trans_prob_tree[j][current_node][0]+trans_prob_tree[j][current_node][1]:
                    current_node=current_node+1
                
                else:
                    current_node=current_node
            
            else:
                if 0<=rand_list[j]<trans_prob_tree[j][current_node][0]:
                    current_node=current_node+1
                
                elif trans_prob_tree[j][current_node][0]<=rand_list[j]<trans_prob_tree[j][current_node][0]+trans_prob_tree[j][current_node][1]:
                    current_node=current_node
                
                else:
                    current_node=current_node-1
                    
            price+=pricing_tree[j+1][current_node]*np.exp(-HW_tree[j+1][current_node]*delta_t/100)
        price_list.append(price)
    return np.mean(price_list)