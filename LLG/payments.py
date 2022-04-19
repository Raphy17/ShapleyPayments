import random as rnd
import matplotlib.pyplot as plt
import numpy as np
from decimal import *
# payment rules
def payment_nearest(payment, bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a+b)
    else:
        payments = payment(bids)

        delta = (g - payments[0] - payments[1])/2
        mrc_payments = (payments[0]+delta, payments[1]+delta, 0)
        if mrc_payments[0]  < 0:
            return (0, g, 0)
        if mrc_payments[1]  < 0:
            return (g, 0, 0)
        if mrc_payments[0] > a:
            return (a, g - a, 0)
        if mrc_payments[1] > b:
            return (g - b, b, 0)
        return mrc_payments

def payoff_shapley_without_seller(bids):
    a, b, g = bids
    if a+b < g:
        return (a/2, b/2, g-(a+b)/2)
    # weak locals
    if a <= g and b <= g:
        return (5*a/6+b/3-g/3, a/3+5*b/6-g/3, 2*g/3-a/6-b/6)
    # strong local 1
    elif b <= g:
        return (a + b / 3 - g / 2, 5 * b/6, g/2-b/6)
    # strong local 2
    elif a <= g:
        return (5*a/6, a/3+b-g/2, g/2-a/6)
    # strong locals
    else:
        return (a-g/6, b-g/6, g/3)

def payoff_shapley_with_seller(bids):
    a, b, g = bids
    if a+b < g:
        return (a/6, b/6, g-(a+b))
    # weak locals
    if a <= g and b <= g:
        return (5*a/12+b/4-g/4, a/4+5*b/12-g/4, g)
    # strong local 1
    elif b <= g:
        return (a/2 + b / 4 - g / 3, 5 * b/12, g)
    # strong local 2
    elif a <= g:
        return (5*a/12, b/2 + a / 2 - g / 3, g)
    # strong locals
    else:
        return (a/2-g/12, b/2-g/12, g)

def payment_first_price(bids):
    a, b, g = bids
    if a + b >= g:
        return (a, b, 0)
    else:
        return (0, 0, g)

def payment_first_price_nearest(bids):
    return payment_nearest(payment_first_price, bids)

def payment_zero(bids):
    return (0, 0, 0)

def payment_zero_nearest(bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a+b)
    elif a >= g/2 and b >= g/2:
        return (g/2, g/2, 0)
    elif a > b:
        return (g-b, b, 0)
    else:
        return (a, g-a, 0)

def payment_vcg(bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a+b)
    else:
        return (max(0, -b+g), max(0, -a+g), 0)

def payment_vcg_nearest(bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a+b)
    else:
        vcg_payments = payment_vcg(bids)
        delta = (g - vcg_payments[0] - vcg_payments[1])/2
        return (vcg_payments[0]+delta, vcg_payments[1]+delta, 0)

def payment_shapley_without_seller(bids):
    a, b, g = bids
    if a + b < g:
        return (a-a, b-b, g-a-b)
    ps = payoff_shapley_without_seller(bids)
    return (a-ps[0], b-ps[1], g-ps[2])

def payment_shapley_without_seller_nearest(bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a + b)
    else:
        shapley_payments = payment_shapley_without_seller(bids)
        delta = (g - shapley_payments[0] - shapley_payments[1]) / 2
        ps = (shapley_payments[0] + delta, shapley_payments[1] + delta, 0)
        if ps[0] > a:
            return (a, g-a, 0)
        if ps[1] > b:
            return (g-b, b, 0)
        return ps

def payment_shapley_with_seller(bids):
    a, b, g = bids
    ps = payoff_shapley_with_seller(bids)
    return (a-ps[0], b-ps[1], g-ps[2])

def payment_shapley_with_seller_nearest(bids):
    a, b, g = bids
    return payment_nearest(payment_shapley_with_seller, bids)

def payment_shapley_payoff_with_seller(bids):
    return payoff_shapley_with_seller(bids)

def payment_shapley_payoff_with_seller_nearest(bids):
    return payment_nearest(payment_shapley_payoff_with_seller, bids)

def payment_shapley_vcg(bids):
    a, b, g = bids
    if g > a + b:
        return (a-a, a-a, a+b)
    if (g > a):
        if (g > b):
            # wl
            paymenta = g/3-b/3
            paymentb = g/3-a/3
        else:
            # sl2
            paymenta = b-b
            paymentb = g/2-a/3
    else:
        if (g > b):
            # sl1
            paymenta = g/2-b/3
            paymentb = a-a
        else:
            # sls
            paymenta = g/6
            paymentb = g/6
    return (paymenta, paymentb, 0)

def payment_bid(bids):
    a, b, g = bids
    if g > a + b:
        return (a-a, b-b, g)
    return (a, b, g-g)

def payment_bid_nearest(bids):
    return payment_nearest(payment_bid, bids)

def payment_shapley_vcg_nearest(bids):
    return payment_nearest(payment_shapley_vcg, bids)

def payment_shapley_ratio(bids):
    a, b, g = bids
    if g > a + b:
        return (0, 0, a+b)
    payoffs = payoff_shapley_without_seller(bids)
    total = payoffs[0] + payoffs[1]
    if total == 0:
        payments = (g/2, g/2, a+b)
    else:
        payments = (g*payoffs[0]/total, g*payoffs[1]/total, 0)
    if payments[0] > a:
        return (a, g-a, 0)
    elif payments[1] > b:
        return (g-b, b, 0)
    return payments

def payment_zero_vcg_middle(bids):
    a, b, g = bids
    p_vcg = payment_vcg(a, b, g)
    payments = []
    for i in p_vcg:
        if i == 0:
            payments.append(0)
        else:
            payments.append(i/2)
    return tuple(payments)

def payment_zero_vcg_middle_nearest(a, b, g):
    return payment_nearest(payment_zero_vcg_middle, a, b, g)

def get_payment_vcg_alpha(alpha):

    def payment_vcg_alpha(bids):
        p_vcg = payment_vcg(bids)
        payments = []
        for i in p_vcg:
            if i == 0:
                payments.append(0)
            else:
                payments.append(i * alpha)
        return payments

    return payment_vcg_alpha
'''
cnt = 0
for i in range(1000):
    a = (rnd.uniform(0, 1))
    b = (rnd.uniform(0, 1))
    g = (rnd.uniform(0, 2))
    x = payment_nearest(payment_shapley_vcg, a, b, g)
    y = payment_nearest(payment_vcg_alpha(a, b, g, ), a, b, g)
    if x[0] >= y[0] + 0.000005 or x[0] <= y[0] - 0.000005 :
        print(a, b, g)
        cnt +=1
        print(x)
        print(y)
        if a < g and b < g:
            print("wl")
        if a > g and b < g:
            print("sl1")
        if a < g and b > g:
            print("sl2")
        if a > g and b > g:
            print("sls")

print(cnt)

'''