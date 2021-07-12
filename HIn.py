import math
from scipy import stats
import numpy as np

def HIn(Oop, Sr):
    R = 8.31434
    t = 80  
    T = t + 273.15
    theta = 4.575 * T / 1000
    beta = 3.436 * math.exp(-1200 * 4.19 /(R * T))  
    RH = 7.17
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

    data2 = []
    with open(Sr, 'r') as f:
        dat = f.readlines()
        for line in dat:
            spl = str.split(line, '\t')
            data2.append(spl)

    n = len(data2)

    W = []     
    HIn = []
    Wok = []    
    tau = []   
    fi = []
    x = []
    y = []

    W0 = float(data1[0][0]) / (60 * 22.4)
    Wok0 = W0 + Wi * (1 - beta) / (2 * beta)

    for i in range(n):
        HIn.append(float(data2[i][0]))
        W.append(float(data2[i][1]) / (60 * 22.4))
        Wok.append(W[i] + Wi * (1 - beta) / (2 * beta))
        tau.append(float(data2[i][2]) * 60)
        fi.append(tau[i] * Wi / HIn[i])
        x.append(HIn[i])
        y.append(tau[i] * Wi)

    fsr = sum(fi) / len(fi)
    
    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa = math.sqrt(n * Sy * Sy / Z)
    eps_f = abs(100 * Sa / a)

    f = a
    Sa_f = Sa

    x = []
    y = []
    for i in range(n):
        x.append(math.log(HIn[i]))
        y.append(math.log(Wok[i]))

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    n_HIn = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_n_HIn = math.sqrt(n * Sy * Sy / Z)
    eps_n_HIn = abs(100 * Sa_n_HIn / a)

    Ft = []
    for i in range(n):
        Ft.append((Wok0 / Wok[i]) * abs(1 - ((Wok[i] ** 2) / (Wok0 ** 2))))

    x = []
    y = []
    for i in range(n):
        x.append(math.log(HIn[i]))
        y.append(math.log(Ft[i]))

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    nf_HIn = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_nf_HIn = math.sqrt(n * Sy * Sy / Z)
    eps_nf_HIn = abs(100 * Sa_nf_HIn / a)

    k2k6 = Wok0 / (RH * math.sqrt(Wi))
    Sa_k2k6=0
    x = []
    y = []
    for i in range(n):
        x.append(RH * Wi / (HIn[i] * f))
        y.append(Wok[i])

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    k2k7 = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_k2k7 = math.sqrt(n * Sy * Sy / Z)
    eps_k2k7 = abs(100 * Sa_k2k7 / a)

    k7 = k2 / k2k7
    Sa_k7 = k7 * eps_k2k7 / 100
    fk7 = f * k7
    Sa_fk7 = fk7 * math.sqrt(math.pow(Sa_f/f, 2) + math.pow(Sa_k7/k7, 2))
    
    return HIn, W, Wok, tau, fi, Ft, f, n_HIn, nf_HIn, fk7, k2k6, k2k7, k7, Sa_f, Sa_n_HIn, Sa_nf_HIn, Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7
    