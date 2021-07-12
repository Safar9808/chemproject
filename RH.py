import math
from scipy import stats
import numpy as np

def RH(Oop, Sr):
    R = 8.31434
    t = 80  
    T = t + 273.15
    theta = 4.575 * T / 1000    
    beta = 3.436 * math.exp(-1200 * 4.19 /(R * T)) 
    HIn = 0.005
    k2 = 10**(6.6 - 9.8/theta) 
    k6 = 10**(9.2 - 6.00/theta) 
    ki = 10**(15 - 30.45/theta) 
    AIBN = 0.05
    Wi = 2 * beta * ki * AIBN  

    data1 = []
    with open(Oop, 'r') as f:
        dat = f.readlines()
        for line in dat:
            spl = str.split(line, '\t')
            data1.append(spl)

    n = len(data1)

    data2 = []
    with open(Sr, 'r') as f:
        dat = f.readlines()
        for line in dat:
            spl = str.split(line, '\t')
            data2.append(spl)

    W0 = []     
    Wok0 = []   
    RH = []
    W = []    
    Wok = []   
    tau = []  
    fi = []
    x = []
    y = []

    for i in range(n):
        W0.append(float(data1[i][1]) / (60 * 22.4))
        Wok0.append(W0[i] + Wi * (1 - beta) / (2 * beta))
        RH.append(float(data2[i][0]))
        W.append(float(data2[i][1]) / (60 * 22.4))
        Wok.append(W[i] + Wi * (1 - beta) / (2 * beta))
        tau.append(float(data2[i][2]) * 60)
        fi.append(tau[i] * Wi / HIn)
        x.append(math.log(RH[i]))
        y.append(math.log(Wok[i]))

    fsr = sum(fi) / len(fi)
    Sa_fsr=0
    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    n_RH = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_n_RH = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_n_RH / a)

    Ft = []
    for i in range(n):
        Ft.append((Wok0[i] / Wok[i]) * abs(1 - ((Wok[i] ** 2) / (Wok0[i] ** 2))))

    x = [math.log(i) for i in RH]
    y = [math.log(i) for i in Ft]
    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    nf_RH = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)
        
    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_nf_RH = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_nf_RH / a)

    x = [math.sqrt(Wi) * i for i in RH]
    y = Wok0
    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    k2k6 = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)
        
    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_k2k6 = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_k2k6 / a)

    lit = k2 / math.sqrt(k6)
    x = [Wi * i / (HIn * fsr) for i in RH]
    y = Wok
    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    k2k7 = a
    k7 = k2 / k2k7
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)
        
    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_k2k7 = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_k2k7 / a)
    Sa_k7 = k7 * eps / 100

    fk7 = fsr * k7 
    Sa_fk7=Sa_k7+Sa_fsr
    return RH, W, Wok, tau, fi, Ft, fsr, n_RH, nf_RH, fk7, k2k6, k2k7, k7, Sa_fsr, Sa_n_RH, Sa_nf_RH, Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7