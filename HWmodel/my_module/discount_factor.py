def discount_factor(delta_t,N):
    import numpy as np
    import matplotlib.pyplot as plt
    #割引債価格(仮定)
    time=np.arange(0,(N+2)*delta_t,delta_t)
    discount_bond_price=np.exp(-time**2/10)/10+0.9

    #割引債価格の描画
    plt.figure(figsize=(10,5))
    plt.plot(time,discount_bond_price)
    plt.xlabel("year")
    plt.ylabel("discount factor")
    plt.savefig("./image/discount_factor.jpg")
    return discount_bond_price