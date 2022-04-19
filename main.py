from experiments import *
from results.result_visualization import *

# MEASURE PERFORMANCE IN LLG
names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
rfps = [payment_vcg, payment_zero, payment_shapley_without_seller, payment_shapley_vcg, payment_bid]
sensitivities= [sensitivity_vcg_of_a, sensitivity_zero_of_a,sensitivity_shapley_without_seller_of_a, sensitivity_shapvcg_of_a, sensitivity_bid_of_a]
strategy_path = "LLG/standard/"
symmetric = True
value_ranges = ((0.0,1.0), (0.0,1.0), (0.0, 2.0))
correlation = 0
N = 100000 # number of Monte Carlo samples, 
setting = "standard LLG"
values = get_random_uniform_bernoulli_correlated_distribution_float(value_ranges,cor=correlation, N=N, seed=0)

print_measure_performance(values, rfps, sensitivities, symmetric,strategy_path, names)

# to automatically measure the performance of groups of settings the write_csv() function in experiments can be used

# MEASURE PERFORMANCE IN L3G
names = ["quadratic", "proxy", "shapley", "svcg", "bid"]
rfps = [l3p.payment_quadratic, l3p.payment_proxy, l3p.payment_shapley_nearest, l3p.payment_shapvcg_nearest, l3p.payment_bid_nearest]
sensitivities= [l3s.sensitivity_vcg_of_a, l3s.sensitivity_zero_of_a,l3s.create_sensitivity_shapley_of_a(), l3s.create_sensitivity_shapvcg_of_a(), l3s.sensitivity_bid_of_a]
strategy_path = "L3G/standard/"
value_ranges = ((0.0,1.0), (0.0,1.0),(0.0, 1.0), (0.0, 3.0))
correlation = 0
N = 100000 # number of Monte Carlo samples
setting = "standard L3G"
values = get_random_uniform_bernoulli_correlated_distribution_float(value_ranges,cor=correlation, N=N, seed=0)

print_measure_derivative_L3G(values, rfps, sensitivities,strategy_path, names)


# MEASURE CORRELATION BETWEEN PERFORMANCE METRICS

payment_rules = ["quadratic", "proxy", "shapley", "svcg", "bid"]
metrics = ['EFF', 'INC', 'REV', 'DEV', 'LM_t', 'LM_t|s*', 'LM_s*'] #also includes DEV metric that measures deviation
metrics = ['EFF', 'INC', 'REV', 'LM_t', 'LM_s*']
metric = 'LM_s*'

# measures correlation between 'metric' and all other metrics in the settings discusses in the thesis

# varying correlation settings
get_correlation_to_metric([result_varying_correlation],metric, payment_rules, metrics, visualize=False)
# varying asymmetry settings
get_correlation_to_metric([result_varying_asymmetry],metric, payment_rules, metrics, visualize=False)
# varying value range settings
get_correlation_to_metric(result_varying_value_ranges,metric, payment_rules, metrics, visualize=False)
# correlation across all settings
get_correlation_to_metric(results[:],metric, payment_rules, metrics, visualize=False)

# to get the specific correlation between two performance metrics
# metric1 = "LM_t|s*"
# metric2 = "LM_t"
# get_correlation(results[:], metric1, metric2, payment_rules[:])


#get_correlation(results[:], "LM_t|s*", "LM_t", payment_rules[:])

