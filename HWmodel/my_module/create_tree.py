def create_tree(a,r_init,h,M,Max_node,delta_t,delta_r,N,N_T,discount_bond_price):
    import copy
    import numpy as np
    import matplotlib.pyplot as plt
    #tree構造に遷移確率とイールドカーブへのフィッティングを行っていない場合(theta=0)の場合の値格納
    HW_tree=[{0:r_init}]
    trans_prob_tree=[{0:[1/(2*h),1-1/h,1/(2*h)]}]
    for i in range(1,N+1):
        node_num=min(int(Max_node),i)
        tmp_HW_tree={}
        tmp_trans_prob_tree={}
        for node in range(-node_num,node_num+1):
            #遷移確率の計算
            if node==Max_node:
                tmp_trans_prob=[1+(1/h+node**2*M**2+3*node*M)/2,-(1/h+node**2*M**2+2*node*M),(1/h+node**2*M**2+node*M)/2]
            elif node==-Max_node:
                tmp_trans_prob=[(1/h+node**2*M**2-node*M)/2,-(1/h+node**2*M**2-2*node*M),1+(1/h+node**2*M**2-3*node*M)/2]
            else:
                tmp_trans_prob=[(1/h+node**2*M**2+node*M)/2,1-1/h-node**2*M**2,(1/h+node**2*M**2-node*M)/2]

            #1時点内の各nodeを格納
            tmp_HW_tree[node]=a*delta_t*i+delta_r*node+r_init
            tmp_trans_prob_tree[node]=tmp_trans_prob

        #各時点のnodeをまとめた結果を格納
        HW_tree.append(tmp_HW_tree)
        trans_prob_tree.append(tmp_trans_prob_tree)
    #Arrow_Debreu証券の価格を格納する。
    Arrow_Debreu_tree=copy.deepcopy(HW_tree)

    #Arrow_Debreu_treeの初期値を設定
    Arrow_Debreu_tree[0][0]=1.0
    for i in range(1,len(Arrow_Debreu_tree)):
        for node in range(-(len(Arrow_Debreu_tree[i])-1)//2,(len(Arrow_Debreu_tree[i])-1)//2+1):
            Arrow_Debreu_tree[i][node]=0

    #Arrow_Debreu証券の価格を計算する。
    for i in range(len(Arrow_Debreu_tree)-1):
        for node in range(-(len(Arrow_Debreu_tree[i])-1)//2,(len(Arrow_Debreu_tree[i])-1)//2+1):
            if node==Max_node:
                up=node
                middle=node-1
                down=node-2
            elif node==-Max_node:
                up=node+2
                middle=node+1
                down=node
            else:
                up=node+1
                middle=node
                down=node-1
            Arrow_Debreu_tree[i+1][up]+=Arrow_Debreu_tree[i][node]*trans_prob_tree[i][node][0]
            Arrow_Debreu_tree[i+1][middle]+=Arrow_Debreu_tree[i][node]*trans_prob_tree[i][node][1]
            Arrow_Debreu_tree[i+1][down]+=Arrow_Debreu_tree[i][node]*trans_prob_tree[i][node][2]
    #イールドカーブへのフィッティングを行う。
    for i in range(len(Arrow_Debreu_tree)):
        sum_tmp=0
        for node in range(-(len(Arrow_Debreu_tree[i])-1)//2,(len(Arrow_Debreu_tree[i])-1)//2+1):
            sum_tmp+=Arrow_Debreu_tree[i][node]*np.exp(-node*delta_r*delta_t)
        alpha=(np.log(sum_tmp)-np.log(discount_bond_price[i+1]))
        for node in range(-(len(Arrow_Debreu_tree[i])-1)//2,(len(Arrow_Debreu_tree[i])-1)//2+1):
            HW_tree[i][node]+=alpha

    #フィッティング後のtreeの描画
    plt.figure(figsize=(15,7.5))
    for i in range(N+1):
        node_num=min(int(Max_node),i)
        for node in range(-node_num,node_num+1):
            if i==N_T:
                plt.plot(i*delta_t,HW_tree[i][node],".",color="red")
            elif node==0:
                plt.plot(i*delta_t,HW_tree[i][node],".",color="black")
            else:
                plt.plot(i*delta_t,HW_tree[i][node],".",color="gray")
    plt.savefig("./image/HW_tree.jpg")
    
    return HW_tree,trans_prob_tree