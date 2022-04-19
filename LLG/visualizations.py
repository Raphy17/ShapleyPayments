from LLG.simulations import *
import time

N = 20000
t0 = time.time()
# PLOTS
def plot_expected_utilities(strategies_a, strategies_b, payment_rules, names, N):
    for strategy_a, strategy_b, payment_rule in zip(strategies_a, strategies_b, payment_rules):
        A_values, utilities = simulate_utility(strategy_a, strategy_b, payment_rule, N)
        plt.plot(dec_to_float(A_values), dec_to_float(utilities))
    plt.legend(names)
    plt.title("Expected Utility for different MRCS payment rules")
    plt.xlabel("Value of A")
    plt.ylabel("Expected Utility")
    # plt.savefig("./plots/Expected Utility for different MRCS payment rules")
    plt.show()

def plot_missed_utility(strategies_a1, strategies_a2, strategies_b, payment_rules, names, N):
    for strategy_a1, strategy_a2, strategy_b, payment_rule in zip(strategies_a1, strategies_a2, strategies_b, payment_rules):
        A_values, utilities_a1 = simulate_utility(strategy_a1, strategy_b, payment_rule, N)
        A_values, utilities_a2 = simulate_utility(strategy_a2, strategy_b, payment_rule, N)
        print(utilities_a1)
        print(utilities_a2)
        d = [i - j for i, j in zip(utilities_a2, utilities_a1)]
        float_d = dec_to_float(d)
        plt.plot(A_values, float_d)
    plt.legend(names)
    plt.title("Missed Utility for different MRCS payment rules")
    plt.xlabel("Value of A")
    plt.ylabel("Missed Utility")
    # plt.savefig("./plots/Missed Utility for different MRCS payment rules")
    plt.show()

def plot_missed_utility_composition(stategy_a_1, strategy_a_2, strategy_b, payment, payment_reference_point, sensitivity_of_a, name, N):
    a_vals, util1, util2, diffs = simulate_utility_difference(stategy_a_1, strategy_a_2, strategy_b, payment, payment_reference_point, sensitivity_of_a, N)
    keys = sorted(list(set([k for d in diffs for k in d.keys()])))

    parts = []
    for k in keys:
        part = []
        for d in diffs:
            part.append(d[k])
        parts.append(part)
    labels = [str(k) for k in keys]
    a_vals = dec_to_float(a_vals)
    new_parts = [dec_to_float(part) for part in parts]
    for part in new_parts:
        plt.plot(a_vals, part)
    plt.stackplot(a_vals,*new_parts, labels=labels)
    plt.legend(loc='upper left', title="Derivative")
    plt.xlabel("A Value")
    plt.ylabel("Utility Gain")
    plt.title("Composition of gained Utility when deviating for "+ name)
    # plt.savefig("./plots/Composition of gained Utility when deviating for " + name)
    plt.show()

def plot_different_derivatives(strategies_a, strategies_b, payment_reference_points, sensitivities, names, N):
    for strategy_a, strategy_b, payment_reference_point, sensitivity in zip(strategies_a, strategies_b, payment_reference_points, sensitivities):
        a_vals, derivs = simulate_average_derivative_when_winning(strategy_a, strategy_b, payment_reference_point, sensitivity, N)
        plt.plot(a_vals, derivs)
    plt.legend(names)
    plt.ylabel("Average Derivative")
    plt.title("Average Derivatives of MRCS payment rules")
    plt.xlabel("Value of A")
    # plt.savefig("./plots/Average Derivatives of MRCS payment rules")
    plt.show()

def plot_missed_utility_times_derivative(stategies_a1, strategies_a2, strategies_b, payments, payment_reference_points, sensitivities_of_a, names, title, N):
    for stategy_a1, strategy_a2, strategy_b,  payment, payment_reference_point, sensitivity_of_a in zip(stategies_a1, strategies_a2, strategies_b, payments, payment_reference_points, sensitivities_of_a):
        a_vals, util1, util2, diffs = simulate_utility_difference(stategy_a1, strategy_a2, strategy_b, payment, payment_reference_point, sensitivity_of_a, N)
        keys = sorted(list(set([k for d in diffs for k in d.keys()])))
        missed_utility_times_derivative = []
        for i in range(len(diffs)):
            total = Decimal(0)
            for k in keys:
                if k != 0:
                    tmp = int(1 / k)
                    dec_k = Decimal(1) / tmp
                else:
                    dec_k = Decimal(0)
                x = diffs[i][k]
                if x == 0:
                    x = Decimal(x)
                total += x * dec_k
            missed_utility_times_derivative.append(total)
        plt.plot(a_vals,missed_utility_times_derivative, )
    plt.legend(names)
    plt.xlabel("A Value")
    plt.ylabel("Possible Utility Gain * Local Derivative")
    plt.title(title)
    #plt.savefig("./plots1/" + title)
    plt.show()

def plot_probabilities_of_derivatives(strategy_a,strategy_b, payment_reference_point, sensitivity_of_a,name, N):
    A_values, derivatives = probabilities_of_derivatives_depending_on_a(strategy_a,strategy_b, payment_reference_point, sensitivity_of_a, N)
    keys = sorted(list(set([k for d in derivatives for k in d.keys()])))
    parts = []
    for k in keys:
        part = []
        for d in derivatives:
            part.append(d[k]/N)
        parts.append(part)
    labels = [str(k) for k in keys]
    plt.stackplot(A_values, *parts, labels=labels)
    plt.legend(loc='upper left', title="Derivative")
    plt.xlabel("A Value")
    plt.ylabel("Probability")
    plt.title("Probabilities of local derivatives " + name)
    plt.savefig("./plots/Probabilities of local derivatives " + name)
    plt.show()

def plot_derivative_composition_of_misreported_value(stategies_a1, strategies_a2, strategies_b, derivative_slice, name, N):
    a_vals, misreport_compositions = simulate_misreport_composition(stategies_a1, strategies_a2, strategies_b, derivative_slice, N)
    keys = sorted(list(set([k for d in misreport_compositions for k in d.keys()])))
    parts = []
    for k in keys:
        part = []
        for d in misreport_compositions:
            part.append(d[k])
        parts.append(part)
    labels = [str(k) for k in keys]
    a_vals = dec_to_float(a_vals)
    new_parts = [dec_to_float(part) for part in parts]
    plt.stackplot(a_vals, *new_parts, labels=labels)
    plt.legend(loc='upper left', title="Derivative")
    plt.xlabel("A Value")
    plt.ylabel("Misreported Value")
    plt.title("Derivative Composition of Misreported Value for " + name)
    # plt.savefig("./plots/Derivative Composition of Misreported Value for " + name)
    plt.show()

def plot_misreport_times_derivative(stategies_a1, strategies_a2, strategies_b, derivative_slices, names, N):
    for stategy_a1, strategy_a2, strategy_b, derivative_slice in zip(stategies_a1, strategies_a2, strategies_b, derivative_slices):
        a_vals, misreport_compositions = simulate_misreport_composition(stategy_a1, strategy_a2, strategy_b, derivative_slice, N)
        keys = sorted(list(set([k for d in misreport_compositions for k in d.keys()])))
        missed_utility_times_derivative = []
        for i in range(len(misreport_compositions)):
            total = Decimal(0)
            for k in keys:
                if k != 0:
                    tmp = int(1 / k)
                    dec_k = Decimal(1) / tmp
                else:
                    dec_k = Decimal(0)
                x = misreport_compositions[i][k]
                if x == 0:
                    x = Decimal(x)
                total += x * dec_k
            missed_utility_times_derivative.append(total)
        plt.plot(a_vals,missed_utility_times_derivative)
    plt.legend(names)
    plt.xlabel("A Value")
    plt.ylabel("Misreport * Derivative")
    plt.title("Possible Misreport Times Derivative of Misreport (integrated)")
    # plt.savefig("./plots/Possible Misreport Times Derivative of Misreport (integrated)")
    plt.show()

def plot_proportional_misreport_composition(stategy_a1, strategy_a2, strategy_b, derivative_slice, name, N):
    a_vals, misreport_compositions = simulate_misreport_composition(stategy_a1, strategy_a2, strategy_b, derivative_slice, N)
    keys = sorted(list(set([k for d in misreport_compositions for k in d.keys()])))
    print(keys)
    parts = []
    for k in keys:
        part = []
        for d in misreport_compositions:
            part.append(d[k])
        parts.append(part)

    for i in range(len(a_vals)):
        sum = 0

        for part in parts:
            sum += part[i]
        print(sum)
        if sum == 0:
            continue
        for part in parts:
            part[i] = part[i]/sum

    labels = [str(k) for k in keys]
    a_vals = dec_to_float(a_vals)
    new_parts = [dec_to_float(part) for part in parts]
    plt.stackplot(a_vals, *new_parts, labels=labels)
    plt.legend(loc='upper left', title="Derivative")
    plt.xlabel("A Value")
    plt.ylabel("Percentage")
    plt.title("Proportional Misreport Composition of " + name)
    plt.savefig("./plots/Proportional Misreport Composition of  " + name)
    plt.show()

def plot_BNE_outcome_composition(strategy_a, strategy_b, payment, name, N):
    lists = simulate_bne_utiliy_outcomes(strategy_a, strategy_b, payment, N)
    utility_advantage = []
    for util_s, util_t in zip(lists[3], lists[4]):
        utility_advantage.append(util_s-util_t)
    lists[3] = lists[4]
    lists[4] = utility_advantage
    new_lists = [dec_to_float(lst) for lst in lists]
    labels = ["same outcome", "both win", "only t wins", "delta s wins"]
    plt.stackplot(*new_lists, labels=labels)
    plt.legend(loc='upper left', title="Derivative")
    plt.xlabel("A Value")
    plt.ylabel("Utility")
    plt.title("Composition of Utility when playing BNE strategy for " + name)
    # plt.savefig("./plots/Composition of gained Utility when deviating for " + name)
    plt.show()

def plot_winning_probability(strategies_a, strategies_b, names, title, N):
    for strategy_a, strategy_b in zip(strategies_a,strategies_b):
        bid_values, probabilities = simulate_probability_of_winning(strategy_a, strategy_b, N)
        plt.plot(bid_values, probabilities)
    plt.legend(names)
    plt.xlabel("A Value")
    plt.ylabel("Probability to Win")
    plt.title(title)
    plt.ylim(ymin=0)
    plt.show()

def plot_average_payments(strategies_a, strategies_b, payments, names, title, N):
    for strategy_a, strategy_b, payment in zip(strategies_a,strategies_b, payments):
        bid_values, payments_of_a = simulate_average_payment_when_winning(strategy_a, strategy_b, payment, N)
        plt.plot(bid_values, payments_of_a)
    plt.legend(names)
    plt.xlabel("A Value")
    plt.ylabel("Average Payment")
    plt.title(title)
    plt.show()

def plot_average_payment_and_winning_probability(strategies_a, strategies_b, payments, names, title, N):
    for strategy_a, strategy_b, payment in zip(strategies_a,strategies_b, payments):
        bid_values, probabilities = simulate_probability_of_winning(strategy_a, strategy_b, N)
        plt.plot(bid_values, probabilities)
        bid_values, payments_of_a = simulate_average_payment_when_winning(strategy_a, strategy_b, payment, N)
        plt.plot(bid_values, payments_of_a)
        #bid_values, utilities = simulate_average_utility_when_winning(strategy_a, strategy_b, payment, N)
        #plt.plot(bid_values, utilities)
    new_names = []
    for name in names:
        new_names.extend([name, name])
    plt.legend(new_names)
    plt.xlabel("A Value")
    plt.ylabel("Average Payment")
    plt.title(title)
    plt.show()

def plot_strategy(strategy_a, strategy_b, payment, title):
    bid_values, probabilities = simulate_probability_of_winning(truthful, strategy_b, N)
    bid_values, payments = simulate_average_payment_when_winning(truthful, strategy_b,payment, N)
    strat = []
    deviation = []
    for bid in bid_values:
        best_bid = strategy_a(bid)
        strat.append(best_bid)
        deviation.append(bid - best_bid)
    plt.plot(bid_values, probabilities)
    plt.plot(bid_values, payments)
    plt.plot(bid_values, strat)
    plt.plot(bid_values, deviation)
    plt.plot(bid_values, bid_values, "--")
    plt.legend(["Winning Probability", "Average Payment", "Best Response", "Deviation", "Truthful"])
    plt.xlabel("A Value/Bid")
    #plt.savefig("./plots1/strategies/Strategy " + title)
    plt.title(title)
    plt.show()

N = 20000
truthful_strategies = lambda x: [truthful]*x
bne_strategies = [quadratic_bne, zero_bne, shapley_bne]
br_strategies = [quadratic_br, zero_br, shapley_br]
payment_reference_points = [payment_vcg, payment_zero, payment_shapley_without_seller]
payments = [payment_vcg_nearest, payment_zero_nearest, payment_shapley_without_seller_nearest]
sensitivities = [sensitivity_vcg_of_a, sensitivity_zero_of_a, sensitivity_shapley_without_seller_of_a]
derivative_slices = [derivative_slice_vcg, derivative_slice_zero, derivative_slice_shapley_wo]
payment_rules = ["vcg", "zero", "shapley"]

# EXPECTED UTILITY
# plot_expected_utilities(truthful_strategies, truthful_strategies, payments, payment_rules, N)
# plot_expected_utilities(br_strategies, truthful_strategies, payments,payment_rules, N)

# MISSED UTILITY
#plot_missed_utility(truthful_strategies(3), br_strategies, truthful_strategies ,payments,payment_rules, N)
#plot_missed_utility(truthful_strategies(3), bne_strategies, bne_strategies,payments,payment_rules, N)

# MISSED UTILITY LOCAL DERIVATIVE COMPOSITION
# plot_missed_utility_composition(truthful, strategy_best_response_to_truthful_vcg_nearest, truthful, payment_vcg_nearest, payment_vcg, sensitivity_vcg_of_a, "vcg-nearest", N)
# plot_missed_utility_composition(truthful,strategy_best_response_to_truthful_zero_nearest , truthful, payment_zero_nearest, payment_zero, sensitivity_zero_of_a, "zero-nearest", N)
# plot_missed_utility_composition(truthful,strategy_best_response_to_truthful_shapley_without_nearest, truthful, payment_shapley_without_seller_nearest, payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "shapley-wo-nearest", N)

# MISSED UTILITY TIMES LOCAL DERIVATIVE
#plot_missed_utility_times_derivative(truthful_strategies(3), bne_strategies,bne_strategies, payments, payment_reference_points, sensitivities, payment_rules,"Utility Gain Times Local Derivative when playing against BNE", N)
#plot_missed_utility_times_derivative(truthful_strategies(3), br_strategies,truthful_strategies(3), payments, payment_reference_points, sensitivities, payment_rules,"Utility Gain Times Local Derivative when playing against truthful", N)

# AVERAGE DERIVATIVES
# plot_different_derivatives(truthful_strategies(3), truthful_strategies(3) ,payment_reference_points, sensitivities, ["vcg", "zero", "shapley"], N)
# plot_different_derivatives(truthful_strategies(3), bne_strategies,payment_reference_points, sensitivities, ["vcg", "zero", "shapley"], N)
# plot_different_derivatives(bne_strategies, bne_strategies ,payment_reference_points, sensitivities, ["vcg", "zero", "shapley"], N)

# PROBABILITIES OF DERIVATIVES
# plot_probabilities_of_derivatives(truthful,truthful, payment_vcg, sensitivity_vcg_of_a, "vcg-nearest", N)
# plot_probabilities_of_derivatives(truthful,truthful, payment_zero, sensitivity_zero_of_a, "zero-nearest", N)
# plot_probabilities_of_derivatives(truthful,truthful, payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "shapley-wo-nearest", N)
# plot_probabilities_of_derivatives(truthful,strategy_BNE_vcg_nearest, payment_vcg, sensitivity_vcg_of_a, "vcg-nearest", N)
# plot_probabilities_of_derivatives(truthful,strategy_BNE_zero_nearest, payment_zero, sensitivity_zero_of_a, "zero-nearest", N)
# plot_probabilities_of_derivatives(truthful,strategy_BNE_shapley_without_nearest, payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "shapley-wo-nearest", N)

# MISREPORTED VALUE DERIVATIVE COMPOSITION
# plot_derivative_composition_of_misreported_value(truthful, strategy_best_response_to_truthful_vcg_nearest, truthful, derivative_slice_vcg, "vcg", N)
# plot_derivative_composition_of_misreported_value(truthful,strategy_best_response_to_truthful_zero_nearest , truthful, derivative_slice_zero, "zero", N)
# plot_derivative_composition_of_misreported_value(truthful,strategy_best_response_to_truthful_shapley_without_nearest, truthful, derivative_slice_shapley_wo, "shapley", N)

# PROPORTIONAL MISREPORTED VALUE DERIVATIVE COMPOSITION
# plot_proportional_misreport_composition(truthful, strategy_best_response_to_truthful_vcg_nearest,truthful, derivative_slice_vcg, "vcg", N)
# plot_proportional_misreport_composition(truthful, strategy_best_response_to_truthful_zero_nearest,truthful, derivative_slice_zero, "zero", N)
# plot_proportional_misreport_composition(truthful, strategy_best_response_to_truthful_shapley_without_nearest,truthful, derivative_slice_shapley_wo, "shapley", N)

# MISREPORTED VALUE TIMES DERIVATIVE
# plot_misreport_times_derivative(truthful_strategies(3), br_strategies,truthful_strategies(3), derivative_slices,payment_rules, N)
# plot_misreport_times_derivative(truthful_strategies(3), bne_strategies,bne_strategies, derivative_slices,payment_rules, N)


# WINNING PROBABILITIES
# plot_winning_probability(truthful_strategies(4), [truthful]+ bne_strategies,["truthful"] + payment_rules, "Probability of winning depending on bid.txt", N)
# plot_winning_probability([truthful]+ bne_strategies, [truthful]+ bne_strategies,["truthful"] + payment_rules, "Probability to win when playing bne strategies", N)

# AVERAGE PAYMENTS
# plot_average_payments(truthful_strategies(3), truthful_strategies(3),payments, payment_rules, "average payment for different bids", N)
# plot_average_payments(truthful_strategies(3), bne_strategies,payments, payment_rules, "average payment for different bids", N)

# PLOT STRATEGIES
# plot_strategy(strategy_best_response_to_truthful_vcg_nearest,truthful, payment_vcg_nearest, "Best Response to Truthful Vcg")
# plot_strategy(strategy_best_response_to_truthful_zero_nearest,truthful, payment_zero_nearest, "Best Response to Truthful Zero")
# plot_strategy(strategy_best_response_to_truthful_shapley_without_nearest,truthful, payment_shapley_without_seller_nearest, "Best Response to Truthful Shapley")
# plot_strategy(strategy_BNE_vcg_nearest,strategy_BNE_vcg_nearest, payment_vcg_nearest, "BNE Vcg")
# plot_strategy(strategy_BNE_zero_nearest,strategy_BNE_zero_nearest, payment_zero_nearest, "BNE Zero")
# plot_strategy(strategy_BNE_shapley_without_nearest,strategy_BNE_shapley_without_nearest, payment_shapley_without_seller_nearest, "BNE Shapley")

# BNE OUTCOME COMPOSITION
# plot_BNE_outcome_composition(strategy_BNE_vcg_nearest, strategy_BNE_vcg_nearest, payment_vcg_nearest,"vcg", N)
# plot_BNE_outcome_composition(strategy_BNE_zero_nearest, strategy_BNE_zero_nearest, payment_zero_nearest,"zero", N)
# plot_BNE_outcome_composition(strategy_BNE_shapley_without_nearest, strategy_BNE_shapley_without_nearest, payment_shapley_without_seller_nearest,"shapley", N)




t1 = time.time()
print("Time :", t1-t0)
