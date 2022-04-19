import matplotlib.pyplot as plt
from decimal import *
from definitions import ROOT_DIR
import os
import time
import random as rnd
import math
from bisect import bisect_right
import numpy as np

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def truthful(a):
    return a

def get_vtruthful():
    return np.vectorize(truthful)

def strategy_first_price(a):
    return max(0.5 * a - 0.25, 0)

def linearly_interpolate(a_values, bid_values, a):
    if a == 0:
        return bid_values[0]
    if a == 1:
        return bid_values[-1]
    index = 0  #replace through binary search
    while a_values[index] < a:
        index +=1
    # linear interpolation
    a0 = a_values[index-1]
    bid0 = bid_values[index-1]
    a1 = a_values[index]
    bid1 = bid_values[index]
    result = bid0 + (a - a0) * (bid1-bid0) / (a1 - a0)
    return result

def text_strategy_to_a_values_and_bids(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy)):
            if i % 2 == 0:
                a_values.append(float(strategy[i]))
            else:
                bid_values.append(float(strategy[i]))
        return a_values, bid_values

def strategy_factory_linear_interpolation_float(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(float(strategy_line[i]))
            else:
                bid_values.append(float(strategy_line[i]))

    def strategy(a):
        i = bisect_right(a_values, a)
        if i ==len(a_values):
            return bid_values[-1]
            #raise ValueError
        else:
            a0 = a_values[i-1]
            a1 = a_values[i]
            bid0 = bid_values[i-1]
            bid1 = bid_values[i]
            d = (a1 - a0)
            if d == 0:
                return bid_values[i]
            else:
                 return bid0 + (a - a0) * (bid1-bid0) / d

    return strategy


def get_vectorized_strategy(file):
    return np.vectorize(strategy_factory_linear_interpolation_float(file))

def strategy_factory_dict_float(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(float(strategy_line[i]))
            else:
                bid_values.append(float(strategy_line[i]))
    strategy = {}
    for i in range(len(a_values)):
        strategy[a_values[i]] = bid_values[i]

    def strat(a):
        if a in strategy:
            return strategy[a]
        else:
            a = round(a, 4) #precision of 4
            if a in strategy:
                return strategy[a]
            else:
                raise ValueError

    return strat


def strategy_factory_float(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(float(strategy_line[i]))
            else:
                bid_values.append(float(strategy_line[i]))
    strategy = {}
    for i in range(len(a_values)):
        strategy[a_values[i]] = bid_values[i]

    def strat(a):
        result = 0
        if a in strategy:
            result = strategy[a]
        # In case it receives decimal input
        else:
            a = float(a)
            if a in strategy:
                result =  strategy[a]
            else:
                if a > 1 or a < 0:
                    print("INVALID INPUT FOR A")
                    return
                a0 = math.floor(a*10000)/10000
                a1 = math.ceil(a*10000)/10000
                bid0 = strategy[a0]
                bid1 = strategy[a1]
                result = bid0 + (a - a0) * (bid1-bid0) / (a1 - a0)
        #if result <= 0.0001:
        #    result = 0.0
        return result
    return strat

def strategy_factory_decimal(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(Decimal(strategy_line[i]))
            else:
                bid_values.append(Decimal(strategy_line[i]))
    strategy = {}
    for i in range(len(a_values)):
        strategy[a_values[i]] = bid_values[i]
    n = len(a_values)-1 # assumes evenly spaced a values between

    def strat(a):
        if a in strategy:
            result = strategy[a]
        # In case it receives float input
        else:
            a = Decimal(a)
            if a in strategy:
                result = strategy[a]
            else:
                if a > 1 or a < 0:
                    print("ERROR, VALUE NOT BETWEEN 0 AND 1")
                    return
                # assumes evenly spaced a values between 0 and 1
                a0 = Decimal((a*n).__floor__())/n
                a1 = Decimal((a*n).__ceil__())/n
                bid0 = strategy[a0]
                bid1 = strategy[a1]
                result = bid0 + (a - a0) * (bid1-bid0) / (a1 - a0)
        if result < 0:
            result = Decimal(0)
        if result > 1:
            result = Decimal(1)
        return result

    return strat

def strategy_factory_decimal_unsave(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(Decimal(strategy_line[i]))
            else:
                bid_values.append(Decimal(strategy_line[i]))
    strategy = {}
    for i in range(len(a_values)):
        strategy[a_values[i]] = bid_values[i]

    def strat(a):
        if a in strategy:
            return strategy[a]
        else:
            a0 = Decimal((a*10000).__floor__())/10000
            a1 = Decimal((a*10000).__floor__())/10000
            bid0 =  strategy[a0]
            bid1 = strategy[a1]
            result = bid0 + (a - a0) * (bid1-bid0) / (a1 - a0)
            return result

    return (lambda x:strategy[x])

def make_strategy_evenly_spaced(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy_line = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy_line)):
            if i % 2 == 0:
                a_values.append(Decimal(strategy_line[i]))
            else:
                bid_values.append(Decimal(strategy_line[i]))
    A_values = [Decimal(a_values[0])]
    steps = 10000
    step = Decimal(1)/steps
    for i in range(steps):
        A_values.append(A_values[i]+step)
    index = 0
    Bid_values =[]
    for a in A_values:
        while a > a_values[index+1]:
            index += 1
        if a == a_values[index]:
            Bid_values.append(bid_values[index])
            continue
        lower_a = a_values[index]
        bid0 = bid_values[index]
        upper_a = a_values[index+1]
        bid1 = bid_values[index+1]
        result = bid0 + (a - lower_a) * (bid1-bid0) / (upper_a - lower_a)
        Bid_values.append(result)
    output_string = ""
    for i in range(len(A_values)):
        output_string += str(A_values[i])
        output_string += " "
        output_string += str(Bid_values[i])
        output_string += "  "
    print(output_string)

def delta_strategy_factory(strategy, delta):

    def strat(a):
        bid_a = strategy(a) + delta
        if bid_a > a:
            bid_a = a
        if bid_a < 0:
            bid_a = strategy(a) - strategy(a)
        return bid_a

    return strat

def get_standard_path_llg():
    return ROOT_DIR + '/strategyText/LLG/standard/'

def get_standard_path_l3g():
    return ROOT_DIR + '/strategyText/L3G/standard/'

def get_quadratic():
    return strategy_factory_linear_interpolation_float(get_standard_path_llg() + "quadratic.txt")

