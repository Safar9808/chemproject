import math
from scipy import stats
import numpy as np

def AIBN(Oop, Sr):
    R = 8.31434
    t = 80
    T = t + 273.15
    theta = 4.575 * T / 1000
    beta = 3.436 * math.exp(-1200 * 4.19 /(R * T))
    HIn = 0.005
    k2 = 10**(6.6 - 9.8/theta)
    k6 = 10**(9.2 - 6.00/theta)
    ki = 10**(15 - 30.45/theta)
    RH = 7.17

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

    n = len(data1)
    W0 = []
    AIBN = []
    W = []
    Wi = []
    Wok0 = []
    Wok = []
    tau = []
    x = []
    y = []
    for i in range(n):
        W0.append(float(data1[i][1]) / (60 * 22.4))
        W.append(float(data2[i][1]) / (60 * 22.4))
        AIBN.append(float(data2[i][0]))
        Wi.append(2 * beta * ki * AIBN[i])
        Wok0.append(W0[i] + Wi[i] * (1 - beta) / (2 * beta))
        Wok.append(W[i] + Wi[i] * (1 - beta) / (2 * beta))
        tau.append(float(data2[i][2]) * 60)
        x.append(HIn / Wi[i])
        y.append(tau[i])

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    f = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_f = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_f / a)

    x = []
    y = []
    for i in range(n):
        x.append(math.log(Wi[i]))
        y.append(math.log(Wok[i]))

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    n_AIBN = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_n_AIBN = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_n_AIBN / a)

    Ft = []
    for i in range(n):
        Ft.append((Wok0[i] / Wok[i]) * abs(1 - ((Wok[i] ** 2) / (Wok0[i] ** 2))))

    x = []
    y = []
    for i in range(n):
        x.append(math.log(Wi[i]))
        y.append(math.log(Ft[i]))

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    nf_AIBN = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_nf_AIBN = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_nf_AIBN / a)

    x = []
    y = []
    for i in range(n):
        x.append(RH * math.sqrt(Wi[i]))
        y.append(Wok0[i])

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

    x = []
    y = []

    for i in range(n):
        x.append(RH * Wi[i] / (HIn * f))
        y.append(Wok[i])

    a, b, r_value, p_value, std_err = stats.linregress(x,y)
    k2k7 = a
    yrs = []
    for i in range(n):
        yrs.append(a * x[i] + b)

    k7 = k2 / k2k7

    Z = n * sum(map(lambda xx: xx * xx, x)) - sum(x) * sum(x)
    _s = 0
    for i in range(n):
        _s += (y[i] - yrs[i]) ** 2
    Sy = math.sqrt(_s / (n - 1))
    Sa_k2k7 = math.sqrt(n * Sy * Sy / Z)
    eps = abs(100 * Sa_k2k7 / a)
    Sa_k7=k7 * eps / 100
    fk7 = f * k7
    Sa_fk7 = fk7 * math.sqrt(math.pow(Sa_f/f, 2) + math.pow(Sa_k7/k7, 2))

    return AIBN, W, Wok, tau, Wi, Ft, f, n_AIBN, nf_AIBN, fk7, k2k6, k2k7, k7, Sa_f, Sa_n_AIBN, Sa_nf_AIBN, Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7
                                 