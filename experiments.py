from strategies import *
import performance as p
import numpy as np
from valueCreator import get_random_uniform_distribution_float
from valueCreator import get_random_uniform_bernoulli_correlated_distribution_float
from valueCreator import get_random_beta_distribution_float
from LLG.payments import *
from LLG.sensitivities import *
from LLG.simulations import derivative_plot
import L3G.payments as l3p
import L3G.sensitivities as l3s
import random

# names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
# rfps = [payment_vcg, payment_zero, payment_shapley_without_seller, payment_shapley_vcg, payment_bid]
# sensitivities= [sensitivity_vcg_of_a, sensitivity_zero_of_a,sensitivity_shapley_without_seller_of_a, sensitivity_shapvcg_of_a, sensitivity_bid_of_a]
# strategy_path = "LLG/standard/"     # path where strategies are defined
# symmetric = True
# value_ranges = ((0.0,1.0), (0.0,1.0), (0.0, 2.0))
# N = 100000
# setting = "standard LLG"
# values = get_random_uniform_bernoulli_correlated_distribution_float(value_ranges,0.0, N, seed=0)


def print_measure_performance(values, rfps, sensitivities, symmetric,strategy_path, names):
    print("PAYMENT-RULE".rjust(13)+ " | "  + "EFFICIENCY".rjust(
        10) + " | " + "INCENTIVE".rjust(10) + " | " + "REVENUE".rjust(10)+ " | " + "DEVIATION".rjust(10)+ " | " + "LM @ Truth".rjust(10) + " | " + "LM @ T|BNE".rjust(10) + " | " + "LM @ BNE".rjust(10))
    for name, reference_point, sensitivity in zip(names, rfps, sensitivities):
        STRATEGY_PATH_LOCAL1 = ROOT_DIR + '/strategyText/'+strategy_path+name+ ".txt"
        STRATEGY_PATH_LOCAL2 = ROOT_DIR + '/strategyText/'+strategy_path[:-1]+"o/"+name+ ".txt"


        strategy_local1 = get_vectorized_strategy(STRATEGY_PATH_LOCAL1)
        if symmetric:
            strategy_local2 = strategy_local1
        else:
            strategy_local2 = get_vectorized_strategy(STRATEGY_PATH_LOCAL2)         # if symmetric, else enter other strategy path
        strategy_global = truthful


        strategies = [strategy_local1, strategy_local2, strategy_global]


        bids = [s(v) for s,v in zip(strategies, values)]

        efficiency = p.efficiency(bids, values)
        incentives = p.incentive(bids, values)
        revenue = p.revenue(bids, values)
        deviation = p.deviation(bids, values)
        if symmetric:
            local_manipulability_at_truth = p.derivative_of_a(values, reference_point, sensitivity)*2
            local_manipulability_other_bne= p.derivative_of_a([values[0], bids[1], values[-1]], reference_point, sensitivity)*2
            local_manipulability_bne = p.derivative_of_a(bids, reference_point, sensitivity)*2
        else:
            local_manipulability_at_truth = sum(p.derivatives(values, reference_point, sensitivity))
            local_manipulability_other_bne= sum(p.derivatives([values[0], bids[1], values[-1]], reference_point, sensitivity))
            local_manipulability_bne = sum(p.derivatives(bids, reference_point, sensitivity))

        print(name.rjust(13) + " | " + str(efficiency)[:10].rjust(
                    10) + " | " + str(incentives)[:10].rjust(10) + " | " + str(revenue)[:10].rjust(10)+ " | " + str(deviation)[:10].rjust(10)+ " | " + str(local_manipulability_at_truth)[:10].rjust(10) + " | " + str(local_manipulability_other_bne)[:10].rjust(10) + " | " + str(local_manipulability_bne)[:10].rjust(10))

def get_performance(values, reference_point, sensitivity, symmetric,strategy_paths, name):

    strategy_local1 = get_vectorized_strategy(strategy_paths[0])
    if symmetric:
        strategy_local2 = strategy_local1
    else:
        strategy_local2 = get_vectorized_strategy(strategy_paths[1])         # if symmetric, else enter other strategy path
    strategy_global = truthful

    strategies = [strategy_local1, strategy_local2, strategy_global]

    bids = [s(v) for s,v in zip(strategies, values)]

    efficiency = p.efficiency(bids, values)
    incentives = p.incentive(bids, values)
    revenue = p.revenue(bids, values)
    deviations = p.deviation(bids, values)
    if symmetric:
        local_manipulability_at_truth = p.derivative_of_a(values, reference_point, sensitivity)*2
        local_manipulability_other_bne= p.derivative_of_a([values[0], bids[1], values[-1]], reference_point, sensitivity)*2
        local_manipulability_bne = p.derivative_of_a(bids, reference_point, sensitivity)*2
    else:
        local_manipulability_at_truth = sum(p.derivatives(values, reference_point, sensitivity))
        local_manipulability_other_bne= sum(p.derivatives([values[0], bids[1], values[-1]], reference_point, sensitivity))
        local_manipulability_bne = sum(p.derivatives(bids, reference_point, sensitivity))
    return efficiency, incentives, revenue, deviations, local_manipulability_at_truth, local_manipulability_other_bne, local_manipulability_bne


def plot_der_dev(names, rfps, sensitivities):
    value_ranges = ((0.0,1.0), (0.0, 2.0))
    N = 100000
    values = get_random_uniform_distribution_float(value_ranges, N, seed=0)
    for name, reference_point, sensitivity in zip(names, rfps, sensitivities):
        STRATEGY_PATH_LOCAL1 = ROOT_DIR + '/strategyText/LLG/standard/'+name+ ".txt"
        strategy_local1 = get_vectorized_strategy(STRATEGY_PATH_LOCAL1)

        aas = np.array([i/100 for i in range(100)])
        bs = strategy_local1(aas)
        deviations = (aas-bs)
        plt.plot(aas, deviations)

        derivative_plot(values, reference_point, sensitivity, name)
        plt.title("Comparison Derivative ~ Deviation for "+name)
        plt.ylabel("Derivative/Deviation")
        plt.xlabel("Value")
        plt.legend(["Deviation", "Derivative"])
        plt.show()

def calculate_derivatives(values, rfps, sensitivities, names, setting):
    print(" Setting:    ".rjust(13)+ "    "+setting)
    print("PAYMENT-RULE".rjust(13)+ " | "  + "LM @ Truth".rjust(10))
    for name, reference_point, sensitivity in zip(names, rfps, sensitivities):
        integrated_derivatives_at_truth = p.derivative_of_a(values, reference_point, sensitivity)
        print(name.rjust(13) + " | " + str(integrated_derivatives_at_truth)[:10].rjust(10))


def write_csv():
    N = 5000000
    names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
    rfps = [payment_vcg, payment_zero, payment_shapley_without_seller, payment_shapley_vcg, payment_bid]
    sensitivities= [sensitivity_vcg_of_a, sensitivity_zero_of_a,sensitivity_shapley_without_seller_of_a, sensitivity_shapvcg_of_a, sensitivity_bid_of_a]

    symmetric = False
    symmetric = True

    output_path = "results/varying_global2.txt"
    #output_path = "results/varying_assymetry.txt"
    #output_path = "results/varying_global.txt"
    #output_path = "results/varying_locals.txt"
    #output_path = "results/correlation.txt"

    strategy_path = "LLG/varying_global2/"
    #strategy_path = "LLG/varying_assymetry/"
    #strategy_path = "LLG/varying_global/"
    #strategy_path = "LLG/varying_locals/"
    #strategy_path = "LLG/correlation/"

    columns = "name, EFF, INC, REV, DEV, LM_t, LM_t|bne, LM_bne\n"
    f = open(output_path, "a")
    f.write(columns)
    f.close()

    for i in range(0, 10):
    #for i in range(1, 11):
    #for i in range(0, 15):
    #for i in range(0, 10):
    #for i in range(0, 105, 5):

        value_ranges = ((0, 1), (0, 1), (0.1*i, 2-0.1*i))
        #value_ranges = ((0.0, 1.0), (0,0.1*i), (0, 1+0.1*i))
        #value_ranges = ((0.5,1.0), (0.5,1.0), (0.1*i, 3-0.1*i))
        #value_ranges = ((i*0.1,1.0), (i*0.1,1.0), (i*0.2, 2.0))
        #value_ranges = ((0.0,1.0), (0.0,1.0), (0.0, 2.0))

        correlation = 0
        #correlation = 0.01*i

        values = get_random_uniform_bernoulli_correlated_distribution_float(value_ranges, correlation, N, seed=0)

        for name, reference_point, sensitivity  in zip(names, rfps, sensitivities):
            path_local1 = ROOT_DIR + '/strategyText/'+strategy_path+str(i)+"/"+name+ ".txt"
            path_local2 = ROOT_DIR + '/strategyText/'+strategy_path+str(i)+"o/"+name+ ".txt"
            performance = get_performance(values, reference_point, sensitivity, symmetric,[path_local1, path_local2], name)
            performance_string = name +", "+", ".join([str(x) for x in performance]) +"\n"
            f = open(output_path, "a")
            f.write(performance_string)
            f.close()


def print_measure_derivative_L3G(values, rfps, sensitivities,strategy_path, names):
    print("PAYMENT-RULE".rjust(13)+ " | "  + "EFFICIENCY".rjust(
        10) + " | " + "INCENTIVE".rjust(10) + " | " + "REVENUE".rjust(10)+ " | " + "DEVIATION".rjust(10)+ " | " + "LM @ Truth".rjust(10) + " | " + "LM @ T|BNE".rjust(10))
    for name, reference_point, sensitivity in zip(names, rfps, sensitivities):
        STRATEGY_PATH_LOCAL1 = ROOT_DIR + '/strategyText/'+strategy_path+name+ ".txt"

        strategy_local1 = get_vectorized_strategy(STRATEGY_PATH_LOCAL1)
        strategy_local2 = strategy_local1
        strategy_local3 = strategy_local1
        strategy_global = truthful


        strategies = [strategy_local1, strategy_local2,strategy_local3, strategy_global]


        bids = [s(v) for s,v in zip(strategies, values)]

        efficiency = p.efficiency(bids, values)
        incentives = p.incentive(bids, values)
        revenue = p.revenue(bids, values)
        deviation = p.deviation(bids, values)
        local_manipulability_at_truth = p.derivative_of_a(values, reference_point, sensitivity)*3
        local_manipulability_other_bne= p.derivative_of_a([values[0], bids[1],bids[2], values[-1]], reference_point, sensitivity)*3
        local_manipulability_bne = p.derivative_of_a(bids, reference_point, sensitivity)*3


        print(name.rjust(13) + " | " + str(efficiency)[:10].rjust(
            10) + " | " + str(incentives)[:10].rjust(10) + " | " + str(revenue)[:10].rjust(10)+ " | " + str(deviation)[:10].rjust(10)+ " | " + str(local_manipulability_at_truth)[:10].rjust(10) + " | " + str(local_manipulability_other_bne)[:10].rjust(10) + " | " + str(local_manipulability_bne)[:10].rjust(10))


# plot_der_dev(names, rfps, sensitivities)
#print_measure_performance(values, rfps, sensitivities, symmetric,strategy_path, names)
# calculate_derivatives(values, rfps, sensitivities, names, setting)

#write_csv()



# names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
# rfps = [l3p.payment_quadratic, l3p.payment_proxy, l3p.payment_shapley_nearest, l3p.payment_shapvcg_nearest, l3p.payment_bid_nearest]
# sensitivities= [l3s.sensitivity_vcg_of_a, l3s.sensitivity_zero_of_a,l3s.create_sensitivity_shapley_of_a(), l3s.create_sensitivity_shapvcg_of_a(), l3s.sensitivity_bid_of_a]
# strategy_path = "L3G/standard/"
# value_ranges = ((0.0,1.0), (0.0,1.0),(0.0, 1.0), (0.0, 3.0))
# N = 10000000
# setting = str(value_ranges)
# values = get_random_uniform_bernoulli_correlated_distribution_float(value_ranges,0.0, N, seed=0)
#
# print_measure_derivative_L3G(values, rfps[4:], sensitivities[4:],strategy_path, names[4:])
