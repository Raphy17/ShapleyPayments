from strategies import *
import performance as p
import numpy as np
from valueCreator import get_random_uniform_distribution_float
from valueCreator import get_random_uniform_bernoulli_correlated_distribution_float
from valueCreator import get_random_beta_distribution_float
from LLG.payments import *
from LLG.sensitivities import *
from LLG.simulations import derivative_plot
from LLG.simulations import derivative_plot
import random
from LLG.sensitivities import *
from LLG.simulations import derivative_plot
import random



def expected_derivative(f, N):
    der = 0
    for i in range(N):
        v = random.uniform(0, 1)
        der += f(v)
    return der/N


def expected_derivative_quadratic(v):
    return 1/8

def expected_derivative_proxy(v):
    return (1-v)**2/4

def expected_derivative_shapley(v):
    if v <= 1/3:
        return (1-3*v+11*v**2/3)/4
    return (5-6*v+7/3*v**2)/32  # (v*(1-v)+5/4*(1-v)**2)/8+v**2/24


def expected_derivative_svcg(v):
    s = v**2
    if v <= 0.3:
        a1 = (3/10*s +3/4*s+9/8*s)/6+3/4*s
        a2 = (25/72*s+5/4*s)/6+5/6*s
        a3 = ((1-10/3*v)*7/3*v)/6 + (1-10/3*v)*v+(1-10/3*v)**2/2
        return 0.25-35/36*v+3389/2160*s
        #return (a1+a2+a3)/2
    elif v <= 0.4:
        a1 = (3/10*s +3/4*s+9/8*s)/6+3/4*s
        a2 = ((1-5/2*v)*3/2*v+(1-5/2*v)*5/12*v)/6+v*(1-5/2*v)
        return 95/144*v - 787*s/720
        #return (a1+a2)/2
    else:
        a0 = s/20
        a1 = 1/3*(1-v)**2
        a2 = (1/3*(1-v)**2 + (1-v)*(v-2/3*(1-v))+ (1-v)**2/2)/6
        return 13/72-7/18*v+7/30*s
        #return 13/72-5/18*v+11/90*s
        #return (a0+a1+a2)/2

def expected_derivative_bid(v):
    return v/2-v**2/4


def plot_derivatives(fs, legend):
    values = [0.01 * i for i in range(0, 101)]
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    for i in range(len(fs)):
        f = fs[i]
        color = colors[i+1]
        der = []
        for v in values:
            der.append(f(v))
        plt.plot(values, der, color=color)

    plt.legend(legend, loc=(0.75, 0.6))
    plt.xlabel("Bid")
    plt.ylabel("Expected Derivative")

    #plt.savefig("../figures/Expected Derivative of different MRC-selecting payment rules")
    plt.show()

def plot_MC_derivative(reference_point,sensitivity, name, N):
    values = get_random_uniform_distribution_float(((0,1), (0, 2)), N, seed=0)
    derivative_plot(values, reference_point, sensitivity, name)
    # plt.title("Expected derivative of "+name)
    # plt.ylabel("Derivative")
    # plt.xlabel("Value")
    # plt.show()


N = 100000
fs = [expected_derivative_quadratic, expected_derivative_proxy, expected_derivative_shapley, expected_derivative_svcg, expected_derivative_bid]
names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
rfps = [payment_vcg, payment_zero, payment_shapley_without_seller, payment_shapley_vcg, payment_bid]
sensitivities= [sensitivity_vcg_of_a, sensitivity_zero_of_a,sensitivity_shapley_without_seller_of_a, sensitivity_shapvcg_of_a, sensitivity_bid_of_a]


plot_MC_derivative(rfps[3], sensitivities[3], "svcg", N)

plot_derivatives(fs, names)

#print(expected_derivative(expected_derivative_svcg, N))