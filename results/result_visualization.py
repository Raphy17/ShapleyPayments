from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
from definitions import ROOT_DIR




def read_result(file):
    results = defaultdict(lambda: defaultdict(list))

    with open(file) as fd:
        lines = fd.readlines()
        metrics = lines[0].strip().split(", ")
        metrics = ["name", 'EFF', 'INC', 'REV', 'DEV', 'LM_t', 'LM_t|s*', 'LM_s*']
        i = 1
        while i < len(lines):
            line = lines[i].strip()
            data = line.split(", ")

            name = data[0]
            for j in range(1, len(metrics)):
                metric = metrics[j]
                value = data[j]
                results[name][metric].append(float(value))

            i += 1
    return results



def print_performance(results):
    correlation = [0.05*i for i in range(21)]
    metrics = ['EFF', 'INC', 'REV', 'DEV', 'LM_t', 'LM_t|s*', 'LM_s*']
    names =  ["quadratic", "proxy", "shapley", "svcg", "bid"]
    for metric in metrics:
        for name in names:
            performace = results[name][metric]
            plt.plot(correlation, performace)
        plt.legend(names)
        plt.title(metric + " depending on correlation")
        plt.xlabel("Correlation")
        plt.ylabel(metric)
        plt.show()

def print_performance_of_payment_rules(results, x_axis,name_x_axis, title):
    metrics = ['EFF', 'INC', 'REV', 'DEV', 'LM_t', 'LM_t|s*', 'LM_s*']
    names =  ["quadratic", "proxy", "shapley", "svcg", "bid"]
    labels = []
    for name in names:
        lm_truth = results[name]['LM_t']
        total_cor = -1
        total_p = 0
        for metric in metrics:
            performace = results[name][metric]
            cor,p = pearsonr(lm_truth,performace)
            total_cor += abs(cor)
            total_p += p
            labels.append(metric + " " + str(round(cor, 3)))
            plt.plot(x_axis, performace)
        print(name, total_cor/6, total_p/6)
        plt.legend(labels)
        plt.title(title + name)
        plt.xlabel(name_x_axis)
        plt.ylabel("performance")
        plt.show()

def average_performance_of_payment_rule(results, payment_rule, metric):
    avg = 0
    divider = 0
    for result in results:
        performance = result[payment_rule][metric]
        avg += sum(performance)
        divider += len(performance)
    return avg/divider


def get_correlation(results, metric1, metric2, payment_rules, visualize=False):
    performances = defaultdict(list)
    for result in results:
        for name in payment_rules:
            performances[metric1].extend(result[name][metric1])
            performances[metric2].extend(result[name][metric2])
    xs = performances[metric1]
    ys = performances[metric2]
    cor, p = pearsonr(xs, ys)
    theta = np.polyfit(xs, ys, 1)
    y_fit = [theta[1] + theta[0] * x for x in xs]

    print(str(round(cor, 2)) + " " + "{0:.0e}".format(p) + " & ", end = "")
    #print(theta)
    #print(metric1, metric2, cor, p)
    if visualize:
        plt.plot(xs, y_fit, color="green")
        plt.scatter(xs, ys, s=10)
        plt.legend([str(round(cor, 2)) +" | "+"{0:.0e}".format(p)])
        plt.title("Correlation between " + metric1 + " and " + metric2 )
        plt.xlabel(metric1)
        plt.ylabel(metric2)
        plt.show()

def get_correlation_to_metric(results, compared_metric, payment_rules, metrics, visualize=False):
    for metric in metrics:
        if metric == compared_metric:
            continue
        get_correlation(results, compared_metric, metric, payment_rules, visualize=visualize)
    print()

result_varying_correlation = read_result(ROOT_DIR + "/results/correlation.txt")
result_varying_asymmetry = read_result(ROOT_DIR + "/results/varying_assymetry.txt")
result_varying_locals = read_result(ROOT_DIR + "/results/varying_locals.txt")
result_varying_global1 = read_result(ROOT_DIR + "/results/varying_global.txt")
result_varying_global2 = read_result(ROOT_DIR + "/results/varying_global2.txt")
result_varying_value_ranges = [result_varying_locals,result_varying_global1,result_varying_global2 ]
results = [result_varying_correlation, result_varying_asymmetry, result_varying_locals, result_varying_global1, result_varying_global2]
payment_rules = ["quadratic", "proxy", "shapley", "svcg", "bid"]
metrics = ['EFF', 'INC', 'REV', 'DEV', 'LM_t', 'LM_t|s*', 'LM_s*']
metrics = ['EFF', 'INC', 'REV', 'LM_t', 'LM_s*']
#payment_rules = [ "proxy", "shapley", "svcg", "bid"]

#get_correlation_to_metric(results[0:1],"LM_t", payment_rules[:], metrics)
#get_correlation_to_metric(results,"LM_s*", payment_rules, metrics)

# get_correlation_to_metric(results[:],"LM_t|s*", payment_rules, metrics)
#
# get_correlation(results[:], "LM_t|s*", m, payment_rules[:])


# correlation = [0.05*i for i in range(21)]
# results = read_result("correlation.txt")
# print_performance_of_payment_rules(results, correlation, "Correlation", "Performance depending on correlation for ")
# print("--")
# varying_assymetry = [0.1*i for i in range(1, 11)]
# results = read_result("varying_assymetry.txt")
# print_performance_of_payment_rules(results, varying_assymetry, "weaker locals value range upper bound", "Performance depending on assymetry for ")
# print("--")
# varying_locals = [0.1*i for i in range(10)]
# results = read_result("varying_locals.txt")
#print_performance_of_payment_rules(results, varying_locals, "local's lower bound", "Performance depending on locals value range for ")
# print("--")
# varying_global= [0.1*i for i in range(15)]
# results = read_result("varying_global.txt")
# print_performance_of_payment_rules(results, varying_global, "global's upper lower bound", "Performance depending on globals value range for ")
# print("--")
# varying_global2 = [0.1*i for i in range(10)]
# results = read_result("varying_global2.txt")
# print_performance_of_payment_rules(results, varying_global2, "global's upper lower bound", "Performance depending on globals value range for ")


