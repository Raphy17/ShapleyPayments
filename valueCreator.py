import random as rnd
from decimal import *
import numpy as np
import time


def get_random_uniform_distribution_float(ranges, N=100000, seed=0):
    distribution = []
    rng = np.random.default_rng(seed)
    for r in ranges:
        distr = rng.uniform(r[0], r[1], N)
        distribution.append(distr)
    return distribution

#works for llg
def get_random_uniform_bernoulli_correlated_distribution_float(ranges, cor=0, N=100000, seed=0):
    #assumes ranges are syymetric
    rng = np.random.default_rng(seed)
    bernoulli = rng.uniform(0, 1, N)
    common_component = rng.uniform(ranges[0][0], ranges[0][1], N)
    identical = bernoulli <= cor
    distribution = []
    for i in range(len(ranges)):
        r = ranges[i]
        distr = rng.uniform(r[0], r[1], N)
        if i < len(ranges)-1: # locals
            distr = np.choose(identical,
                       [distr, common_component])
        distribution.append(distr)

    return distribution


def get_random_uniform_values_decimal(ranges, N):
    values = []
    for i in range(N):
        value_profile = []
        for val_range in ranges:
            value_profile.append(Decimal(rnd.uniform(*val_range)).__round__(14))
        values.append(tuple(value_profile))
    return values

def get_random_beta_distribution_float(ranges,a, b, N=100000, seed=0):
    distribution = []
    rng = np.random.default_rng(seed)
    for r in ranges:
        distr = rng.beta(a=a, b=b, size=N)
        distribution.append(distr)
    return distribution


def get_random_uniform_values_numpy(ranges, N):
    rng = np.random.default_rng(0)
    l = []
    u = []
    for r in ranges:
        l.append(r[0])
        u.append(r[1])
    values = rng.uniform(l, u, (N, len(ranges)))
    return values

def get_perfectly_uniform_values(ranges, Ns):
    if len(Ns) == 0:
        return [()]
    step = Decimal((ranges[0][1]-ranges[0][0]))/Ns[0]
    own_values = []
    x = ranges[0][0]+step/2
    for i in range(Ns[0]):
        own_values.append((x,))
        x += step
    next_values = get_perfectly_uniform_values(ranges[1:],Ns[1:])
    resulting_values = []
    for v1 in own_values:
        for v2 in next_values:
            resulting_values.append(v1+v2)
    return resulting_values


def test(x):
    return sum(x)

# ranges = ((0,1), (0,1), (0,2))
# N = 10
# a = get_random_uniform_values_decimal(ranges, N)
# b = get_random_uniform_values_numpy(ranges, N)
# print(a)
# print(b)
# t = time.time()
# s1 = list(map(test, a))
# t1 = time.time()
# s2 = test(b)
# print(t1-t, time.time()-t1)
# print(s1)
# print(s2)