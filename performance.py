from valueCreator import *
from strategies import *
import numpy as np
import time
from LLG.payments import *
from LLG.sensitivities import *
import L3G.sensitivities as l3g





def deviation(bids, valuations):
    integrals = []
    total_expected_value = 0
    for bid_vector, valuation in zip(bids, valuations):
        total_expected_value += valuation.mean()
        dev = valuation - bid_vector
        integrals.append(dev.mean())
    return sum(integrals)/total_expected_value

def incentive(bids, valuations):
    incentives = []
    total_expected_value = 0
    for bid_vector, value_vector in zip(bids, valuations):
        total_expected_value += value_vector.mean()
        deviation = value_vector - bid_vector
        incentives.append((deviation**2).mean()**0.5)
    return sum(incentives)/total_expected_value

# works only for llg and l3g
def efficiency(bids, valuations):
    sum_locals_bids = np.zeros(len(bids[0]))
    sum_locals_vals = np.zeros(len(valuations[0]))
    for i in range(len(bids)-1):
        sum_locals_bids += bids[i]
        sum_locals_vals += valuations[i]
    efficieny_bids = np.choose(sum_locals_bids < bids[-1], [sum_locals_vals,bids[-1]]).mean()
    efficiency_opt = np.maximum(sum_locals_vals, valuations[-1]).mean()
    return (efficieny_bids/efficiency_opt)

def revenue(bids, valuations):
    # llg
    N = len(valuations[0])
    if len(bids) == 3:
        payment_locals_vcg = np.maximum(np.zeros(N), valuations[2]-valuations[0]) + np.maximum(np.zeros(N), valuations[2]-valuations[1])
        total_value_locals = valuations[0] + valuations[1]
        revenue_vcg = np.choose(total_value_locals> valuations[2], [total_value_locals, payment_locals_vcg]).mean()
        revenue_p = np.minimum(bids[0]+bids[1], bids[2]).mean()
    else:
        payment_locals_vcg = np.maximum(np.zeros(N), valuations[3] - valuations[0]-valuations[1]) + np.maximum(np.zeros(N),valuations[3] - valuations[0] - valuations[2]) + np.maximum(np.zeros(N),valuations[3] - valuations[1] - valuations[2])
        total_value_locals = valuations[0] + valuations[1] + valuations[2]
        revenue_vcg = np.choose( total_value_locals> valuations[3],
                                [total_value_locals, payment_locals_vcg]).mean()
        revenue_p = np.minimum(bids[0] + bids[1] + bids[2], bids[3]).mean()
    return revenue_p/revenue_vcg

def derivatives(bids, payment_reference_point, sensitivity):
    N = len(bids[0])
    bids = [list(x) for x in bids]
    if len(bids) == 3:
        derivatives = [0,0,0]
        cnt = 0
        for i in range(N):
            bids0 = (bids[0][i], bids[1][i], bids[2][i])
            if bids0[0]+bids0[1] < bids0[2]:
                continue
            derivatives[0] += derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)
            # print(bids0)
            # print(derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity))
            bids1 = (bids[1][i], bids[0][i], bids[2][i])
            derivatives[1] += derivative_of_payment_of_a(bids1, payment_reference_point, sensitivity)
            cnt += 1
        print(cnt)
        return [d/N for d in derivatives]
    elif len(bids) == 4:
        derivative = 0
        cnt = 0
        for i in range(N):
            bids0 = (bids[0][i], bids[1][i],bids[2][i], bids[2][i])
            if bids0[0]+bids0[1]+bids0[2] < bids0[3]:
                continue
            derivative += l3g.derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)
            cnt += 1
        return derivative/N
    else:
        raise ValueError

def derivative_of_a(bids, payment_reference_point, sensitivity):
    N = len(bids[0])
    bids = [list(x) for x in bids]
    if len(bids) == 3:
        derivative = 0
        cnt = 0
        for i in range(N):
            bids0 = (bids[0][i], bids[1][i], bids[2][i])
            if bids0[0]+bids0[1] < bids0[2]:
                continue
            derivative += derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)
            cnt += 1
        return derivative/N
    elif len(bids) == 4:
        derivative = 0
        cnt = 0
        for i in range(N):
            bids0 = (bids[0][i], bids[1][i],bids[2][i], bids[3][i])
            if bids0[0]+bids0[1]+bids0[2] < bids0[3]:
                continue
            derivative += l3g.derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)
            cnt += 1
        return derivative/N
    else:
        raise ValueError

def derivative_when_winning(bids, payment_reference_point, sensitivity):
    N = len(bids[0])
    bids = [list(x) for x in bids]
    if len(bids) == 3:
        derivatives = [0,0,0]
        cnt = 0
        for i in range(N):
            bids0 = (bids[0][i], bids[1][i], bids[2][i])
            if bids0[0]+bids0[1] < bids0[2]:
                continue
            derivatives[0] += derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)
            # print(bids0)
            # print(derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity))
            bids1 = (bids[1][i], bids[0][i], bids[2][i])
            derivatives[1] += derivative_of_payment_of_a(bids1, payment_reference_point, sensitivity)
            cnt += 1
        return [d/N for d in derivatives]
    elif len(bids) == 4:
        pass
    else:
        raise ValueError

#alternative way toi calcualte ffiuciency given uniform distributions
def test_efficiency(bids, valuations):
    sum_locals_vals = np.zeros(len(valuations[0]))
    deviations = valuations[0]-bids[0]+valuations[1]-bids[1]
    deviations = deviations**2
    deviations = deviations/2.0
    deviations = deviations.mean()/2
    for i in range(len(bids)-1):
        sum_locals_vals += valuations[i]
    efficiency_opt = np.maximum(sum_locals_vals, valuations[-1]).mean()
    return 1-(deviations/efficiency_opt)

def test_efficiency2(bids, valuations):
    sum_locals_vals = np.zeros(len(valuations[0]))
    deviations = (valuations[0]-bids[0])*(valuations[1]-bids[1])
    deviations = deviations.mean()
    #print(deviations)
    inc = incentive(bids, valuations)
    inc = ((inc/2)**2)  #*2/2
    res = (inc + deviations)
    res= res/2
    for i in range(len(bids)-1):
        sum_locals_vals += valuations[i]
    efficiency_opt = np.maximum(sum_locals_vals, valuations[-1]).mean()
    #print(efficiency_opt)
    return 1-(res/efficiency_opt)



## legacy from here on out

def trapzoid_integral_y_vals(delta_x, y_vals):
    # assuming equispaced xvals
    sum = y_vals[0] + y_vals[-1]
    for i in range(1, len(y_vals)-1):
        sum += 2*y_vals[i]
    return sum*delta_x/2

def trapzoid_integral(x0, xn, delta_x, fun):
    # assuming equispaced xvals
    sum = fun(x0) + fun(xn)
    x = x0 + delta_x
    while x < xn:
        sum += 2*fun(x)
        x += delta_x
    return sum*delta_x/2

def incentive_numeric(x0, xn, delta, strategy):
    sum = 0
    x = x0+delta/2
    cnt = 0
    while x < xn:
        sum += (x-strategy(x))**2
        x += delta
        cnt += 1

    return float(sum*delta)**0.5

#this assumes the symmetric case
def monteCarlo_revenue_llg(strategy, N):
    revenue = 0
    revenue_vcg = 0
    for value in get_random_uniform_values_numpy(((0,1), (0,1), (0,2)), N):
        a, b, g = value
        if g > a + b:
            revenue_vcg += a + b
        else:
            revenue_vcg += max(0, g-b) + max(0, g-a)
        bid_a = strategy(a)
        bid_b = strategy(b)
        if g > bid_a + bid_b:
            revenue += bid_a + bid_b
        else:
            revenue += g
    return revenue/revenue_vcg

def monteCarlo_revenue_tlg(strategy, N):
    revenue = 0
    revenue_vcg = 0
    for value in get_random_uniform_values_numpy(((0,1), (0,1),(0,1), (0,3)), N):
        a, b,c, g = value
        if g > a + b + c:
            revenue_vcg += a + b + c
        else:
            revenue_vcg += max(0, g-b-c) + max(0, g-a-c) + max(0, g-a-b)
        bid_a = strategy(a)
        bid_b = strategy(b)
        bid_c = strategy(c)
        if g > bid_a + bid_b + bid_c:
            revenue += bid_a + bid_b + bid_c
        else:
            revenue += g
    #revenue = revenue/N
    #revenue_vcg = revenue_vcg/N
    return revenue/revenue_vcg

def monteCarlo_efficiency_llg(strategy, N):
    efficiency = 0
    efficiency_opt = 0
    for value in get_random_uniform_values_numpy(((0,1), (0,1), (0,2)), N):
        a, b, g = value
        if g > a + b:
            efficiency_opt += g
        else:
            efficiency_opt += a + b
        bid_a = strategy(a)
        bid_b = strategy(b)
        if g > bid_a + bid_b:
            efficiency += g
        else:
            efficiency += a + b
    #efficiency = efficiency/N
    #efficiency_opt = efficiency_opt/N
    return efficiency/efficiency_opt

def monteCarlo_efficiency_tlg(strategy, N):
    efficiency = 0
    efficiency_opt = 0
    for value in get_random_uniform_values_decimal(((0,1), (0,1),(0,1), (0,3)), N):
        a, b,c, g = value
        if g > a + b+c:
            efficiency_opt += g
        else:
            efficiency_opt += a + b+c
        bid_a = strategy(a)
        bid_b = strategy(b)
        bid_c = strategy(c)
        if g > bid_a + bid_b+bid_c:
            efficiency += g
        else:
            efficiency += a + b+c
    #efficiency = efficiency/N
    #efficiency_opt = efficiency_opt/N
    return efficiency/efficiency_opt

def monteCarlo_incentive_llg(strategy, N):
    incentive = 0
    for values in get_random_uniform_values_decimal(((0,1),), N):
        a = values[0]
        bid_a = strategy(a)
        difference = a - bid_a
        incentive += difference*difference

    efficiency = incentive/N

    return float(efficiency)**0.5

def llg_stats(strategies, names, N=100000):
    print("PAYMENT-RULE".rjust(13)+" | " + "INTEGRAL".rjust(10) +" | " +"EFFICIENCY".rjust(10)+" | "+"INCENTIVE".rjust(10)+" | "+"REVENUE".rjust(10))
    for strategy, name in zip(strategies,names):
        integral = 0.5-float(trapzoid_integral(Decimal(0),Decimal(1), Decimal("0.01"), strategy))
        incen = incentive_numeric(Decimal(0), Decimal(1), Decimal("0.01"), strategy) * 2
        efficiency = monteCarlo_efficiency_llg(strategy, N)
        revenue = monteCarlo_revenue_llg(strategy, N)
        print(name.rjust(13) + " | " + str(integral)[:10].rjust(10) + " | " + str(efficiency)[:10].rjust(10) + " | " + str(incen)[:10].rjust(10) + " | " + str(revenue)[:10].rjust(10))


def tlg_stats(strategies, names, N=100000):
    print("PAYMENT-RULE".rjust(13) + " | " + "INTEGRAL".rjust(10) + " | " + "EFFICIENCY".rjust(
        10) + " | " + "INCENTIVE".rjust(10) + " | " + "REVENUE".rjust(10))
    for strategy, name in zip(strategies, names):
        integral = 0.5 - float(trapzoid_integral(Decimal(0), Decimal(1), Decimal("0.01"), strategy))
        incen = incentive_numeric(Decimal(0), Decimal(1), Decimal("0.01"), strategy) * 3
        efficiency = monteCarlo_efficiency_tlg(strategy, N)
        revenue = monteCarlo_revenue_tlg(strategy, N)
        print(name.rjust(13) + " | " + str(integral)[:10].rjust(10) + " | " + str(efficiency)[:10].rjust(
            10) + " | " + str(incen)[:10].rjust(10) + " | " + str(revenue)[:10].rjust(10))