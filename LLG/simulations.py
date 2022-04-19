from LLG.sensitivities import *
from collections import defaultdict
from strategies import *
from valueCreator import *
from functools import reduce
import operator
# Sensitivities

# todo: document findings, very clear, save plots
# TODO: think about idea: find out payment rule that maximizes win probability/metric from paper
# TODO: histrogram of missed utility/ plot the distribution, maybe explains bumps
# TODO: finalize anylision of bne strategy (make incentives, efficiency revenue more clear etc.)

def dec_to_float(lst):
    return [float(x) for x in lst]

# SIMULATIONS
getcontext().prec = 15

def test_utility(a, bid, payment, N= 300000):
    utility = 0
    for i in range(N):
        b = Decimal(rnd.uniform(0, 1)).__round__(3)
        g = Decimal(rnd.uniform(0, 2)).__round__(3)
        if bid + b >= g:
            utility += a - payment(bid, b, g)[0]
        else:
            utility += 0
    utility = utility/N
    print(utility)
    return utility

# print(strategy_best_response_to_truthful_zero_nearest(Decimal(1)/5))
#a = Decimal(1)/2
#bid.txt = strategy_best_response_to_truthful_zero_nearest(0.5)
#e_BNE_Calculator(a, Decimal("0.01"), payment_zero_nearest)

def simulate_utility(strategy_a, strategy_b, payment, Ns=(200, 400)):
    n = reduce(operator.mul, Ns, 1)
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    for i in range(steps):
        A_values.append(A_values[i]+step)
    utilities = []
    for a in A_values:
        bid_a = strategy_a(a)
        total_utility = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a + bid_b >= g:
                utility = a - payment(bid_a, bid_b, g)[0]
            else:
                utility = 0
            total_utility += utility
        utilities.append(total_utility/n)
    return A_values, utilities

def simulate_utility_difference(strategy_a_1, strategy_a_2, strategy_b, payment, payment_reference_point, sensitivity, Ns=(200, 400)):
    n = reduce(operator.mul, Ns, 1)
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    for i in range(steps):
        A_values.append(A_values[i]+step)
    utilities_1 = []
    utilities_2 = []
    differences = []
    for a in A_values:
        bid_a_1 = strategy_a_1(a)
        bid_a_2 = strategy_a_2(a)
        total_utility_1 = 0
        total_utility_2 = 0
        total_differences = defaultdict(int)
        #for i in range(N):
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a_1 + bid_b >= g:
                payment_of_a_strat_1 = payment(bid_a_1, bid_b, g)[0]
                utility_1 = a - payment_of_a_strat_1
            else:
                utility_1 = 0
            total_utility_1 += utility_1
            if bid_a_2 + bid_b >= g:
                payment_of_a_strat_2 = payment(bid_a_2, bid_b, g)[0]
                utility_2 = a - payment_of_a_strat_2
            else:
                utility_2 = 0
            total_utility_2 += utility_2
            difference = utility_2 - utility_1
            derivative = derivative_of_payment_of_a(bid_a_1, bid_b, g, payment_reference_point, sensitivity)

            total_differences[derivative] += difference
        utilities_1.append(total_utility_1 / n)
        utilities_2.append(total_utility_2 / n)
        for key in total_differences.keys():
            total_differences[key] = total_differences[key]/n
        differences.append(total_differences)

    return A_values, utilities_1, utilities_2, differences

def simulate_misreport_composition(strategy_a_1, strategy_a_2, strategy_b, derivative_slice, Ns=(200, 400)):
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1) / steps
    for i in range(steps):
        A_values.append(A_values[i] + step)
    misreport_compositions = []
    for a in A_values:
        cnt_n = 0
        bid_a_1 = strategy_a_1(a)
        bid_a_2 = strategy_a_2(a)
        misreport_composition = defaultdict(int)
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a_1 + bid_b >= g:
                slice = derivative_slice(bid_b, g)
                cnt_n += 1
                derivative_composition = slice_to_derivative_decomposition(bid_a_1, bid_a_2, slice)
                for key in derivative_composition.keys():
                    misreport_composition[key] += derivative_composition[key]
        for key in misreport_composition.keys():
            misreport_composition[key] = misreport_composition[key]/cnt_n
        misreport_compositions.append(misreport_composition)
    return A_values, misreport_compositions


# returns probabilities of sg, wl, sl1, sl2, sl
def probabilities_of_bid_profiles():
    s_g, s_wl, s_sl1, s_sl2, s_sl = 0, 0, 0, 0, 0
    values = get_random_uniform_values_decimal(((0, 1), (0, 1), (0, 2)), 10000)
    for a, b, g in values:
        if a + b >= g:
            if a >= g and b >= g:
                s_sl += 1
            elif a >= g:
                s_sl1 += 1
            elif b >= g:
                s_sl2 += 1
            else:
                s_wl += 1
        else:
            s_g += 1
    return (s_g, s_wl, s_sl1, s_sl2, s_sl)
# print(probabilities_of_bid_profiles())

def average_derivative_of_a(strategy_a, strategy_b, payment_reference_point, sensitivity, N=1000000):
    cnt = 0
    for i in range(N):
        a = rnd.uniform(0, 1)
        bid_a = strategy_a(a)
        b = rnd.uniform(0, 1)
        bid_b = strategy_b(b)
        g = rnd.uniform(0, 2)
        bids = (bid_a, bid_b, g)
        cnt += derivative_of_payment_of_a(bids, payment_reference_point, sensitivity)
    return cnt / N
#print(average_derivative_of_a(truthful, truthful, payment_vcg, sensitivity_vcg_of_a, 1000000))
#print(average_derivative_of_a(truthful, truthful, payment_zero, sensitivity_zero_of_a, 500000))
#print(average_derivative_of_a(truthful, truthful, payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, 5000000))
#print(average_derivative_of_a(truthful, truthful, payment_shapley_with_seller, sensitivity_shapley_with_seller_of_a, 1000000))

# print(average_derivative_of_a(payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, 200000))

def average_derivative_times_utility_of_a(payment, payment_reference_point, sensitivity, N=100000):
    cnt = 0
    for i in range(N):
        a = rnd.uniform(0, 1)
        b = rnd.uniform(0, 1)
        g = rnd.uniform(0, 2)
        utility_lost = max(payment(a, b, g)[0] - (g-b), 0)
        cnt += utility_lost * derivative_of_payment_of_a(a, b, g, payment_reference_point, sensitivity)
    return cnt / N
# print(average_derivative_times_utility_of_a(payment_vcg_nearest, payment_vcg, sensitivity_vcg_of_a, 200000))
# print(average_derivative_times_utility_of_a(payment_shapley_without_seller_nearest, payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, 200000))
# print(average_derivative_times_utility_of_a(payment_zero_nearest, payment_zero, sensitivity_zero_of_a, 200000))
# print(average_derivative_times_utility_of_a(payment_shapley_with_seller_nearest, payment_shapley_with_seller, sensitivity_shapley_with_seller_of_a, 200000))

def probabilities_of_derivatives_depending_on_a(strategy_a, strategy_b, payment_reference_point, sensitivity_of_a, Ns=(200, 400)):
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    for i in range(steps):
        A_values.append(A_values[i]+step)
    derivatives = []
    for a in A_values:
        derivative_cnt = defaultdict(int)
        bid_a = strategy_a(a)
        cnt = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            #for i in range(N):
            #b = Decimal(rnd.uniform(0, 1)).__round__(4)
            #g = Decimal(rnd.uniform(0, 2)).__round__(4)
            bid_b = strategy_b(b)
            if bid_a + bid_b >= g:
                derivative = derivative_of_payment_of_a(bid_a, bid_b, g, payment_reference_point, sensitivity_of_a)
                derivative_cnt[derivative] += 1
        derivatives.append(derivative_cnt)
    return A_values, derivatives

def simulate_bne_utiliy_outcomes(strategy_a, strategy_b, payment, Ns=(200, 400)):
    n = reduce(operator.mul, Ns, 1)
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1) / steps
    for i in range(steps):
        A_values.append(A_values[i] + step)
    utilities_same = []
    utilities_s_better = []
    utilities_s_better_delta = []
    utilities_t_better = []
    for a in A_values:
        bid_a = strategy_a(a)
        total_utility_same = Decimal(0)
        total_utility_s_better = Decimal(0)
        total_utility_s_better_delta = Decimal(0)
        total_utility_t_better = Decimal(0)
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if a + bid_b >= g:
                if bid_a + bid_b >= g:
                    utility_t = a - payment(a, bid_b, g)[0]
                    utility_s = a - payment(bid_a, bid_b, g)[0]
                    if utility_t == utility_s:
                        total_utility_same += utility_t
                    else:
                        total_utility_s_better += utility_t
                        total_utility_s_better_delta += (utility_s - utility_t)
                else:
                    total_utility_t_better += a - payment(a, bid_b, g)[0]
        utilities_same.append(total_utility_same/n)
        utilities_s_better.append(total_utility_s_better/n)
        utilities_s_better_delta.append(total_utility_s_better_delta/n)
        utilities_t_better.append(total_utility_t_better/n)
    return [A_values, utilities_same, utilities_s_better, utilities_s_better_delta, utilities_t_better]

def simulate_average_derivative_when_winning(strategy_a, strategy_b, payment_reference_point, sensitivity, Ns=(200, 400)):
    derivatives = []
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    for i in range(steps):
        A_values.append(A_values[i]+step)
    for a in A_values:
        cnt_N = 0
        bid_a = strategy_a(a)
        total_derivative = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            #for i in range(N):
            #b = Decimal(rnd.uniform(0, 1)).__round__(4)
            #g = Decimal(rnd.uniform(0, 2)).__round__(4)
            bid_b = strategy_b(b)
            if bid_a + bid_b >= g:
                derivative = derivative_of_payment_of_a(bid_a, bid_b, g, payment_reference_point, sensitivity)
                cnt_N += 1
                total_derivative += derivative
        derivatives.append(total_derivative / cnt_N)
    return A_values, derivatives

def simulate_probability_of_winning(strategy_a, strategy_b, Ns=(200, 400)):
    n = reduce(operator.mul, Ns, 1)
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    probabilities = []
    for i in range(steps):
        A_values.append(A_values[i]+step)
    for a in A_values:
        bid_a = strategy_a(a)
        cnt = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a + bid_b > g:
                cnt += 1
            elif bid_a + bid_b == g:
                cnt += 0.5
        probabilities.append(cnt/n)
    return A_values, probabilities

def simulate_average_payment_when_winning(strategy_a, strategy_b, payment, Ns=(200, 400)):
    A_values = [Decimal(0)]
    steps = 100
    step = Decimal(1)/steps
    payments = []
    for i in range(steps):
        A_values.append(A_values[i]+step)
    for a in A_values:
        bid_a = strategy_a(a)
        total_payment = 0
        cnt = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a + bid_b >= g:
                total_payment += payment(bid_a, bid_b, g)[0]
                cnt += 1
        payments.append(total_payment/cnt)
    return A_values, payments

def simulate_average_utility_when_winning(strategy_a, strategy_b, payment, Ns=(200, 400)):
    A_values = [Decimal(0)]
    steps = 20
    step = Decimal(1)/steps
    utilities = []
    for i in range(steps):
        A_values.append(A_values[i]+step)
    for a in A_values:
        bid_a = strategy_a(a)
        total_utility = 0
        cnt = 0
        values = get_perfectly_uniform_values(((Decimal(0), Decimal(1)), (Decimal(0), Decimal(2))), Ns)
        for b, g in values:
            bid_b = strategy_b(b)
            if bid_a + bid_b >= g:
                total_utility += a - payment(bid_a, bid_b, g)[0]
                cnt += 1
        utilities.append(total_utility/cnt)
    return A_values, utilities

def verifier_llg(strategy, payment, a):
    Ns = (100, 200)
    ranges = ((0.75,1), (1.0,2.5))
    N = 100000
    strat_bid_a = strategy(a)
    print(strat_bid_a)
    bid_as = []
    bid_a = 0
    delta = 0.01
    distr = get_random_uniform_distribution_float(ranges, N)
    bids = [list(x) for x in distr]
    #bids = get_random_uniform_values_decimal(ranges, N)
    total_values = []

    while bid_a < a:
        total_value = 0
        bid_as.append(bid_a)
        for b,g in zip(bids[0], bids[1]):
            bid_b = strategy(b)
            if g < bid_a + bid_b:
                total_value += a - payment((bid_a,bid_b,g))[0]
        total_values.append(total_value/N)
        bid_a += delta
    return bid_as, total_values

# test_strat = strategy_factory_linear_interpolation_float("C:\Projects\Shapley_project\strategyText\LLG\experiments/1\proxy.txt")
# bids, vals = verifier_llg(test_strat,payment_zero_nearest, 0.76)
# #bids1, vals1 = verifier_llg(zero_bne, payment_zero_nearest, Decimal("0.35"))
# #bids2, vals2 = verifier_llg(shapley_bne,payment_shapley_without_seller_nearest, Decimal("0.35"))
# plt.plot(bids, vals)
# #plt.plot(bids1, vals1)
# #plt.plot(bids2, vals2)
# #plt.legend(["quadratic", "proxy", "shapley"])
# plt.show()
# ind = vals.index(max(vals))
# print(bids[ind])

def integrated_derivative(payment, sensitivity_of_a, Ns):
    ranges = ((0,1), (0,1), (0, 2))
    N = reduce(operator.mul, Ns, 1)
    sum = 0
    # for bids in get_random_uniform_values_decimal(ranges, N):
    for bids in get_perfectly_uniform_values(ranges, Ns):
        sum += derivative_of_payment_of_a(bids,payment, sensitivity_of_a)
    return sum / (N/2)


# Ns = (100, 100, 200)
# x = integrated_derivative(payment_vcg, sensitivity_vcg_of_a, Ns)
# y = integrated_derivative(payment_zero, sensitivity_zero_of_a, Ns)
# z = integrated_derivative(payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, Ns)
# q = integrated_derivative(payment_shapley_vcg, sensitivity_shapvcg_of_a, Ns)
# print(x, y, z, q)


def derivative_plot(bids, payment_reference_point, sensitivity, name):
    N = len(bids[0])
    bids = [list(x) for x in bids]
    bs = list(bids[0])
    gs = list(bids[1])
    derivatives = []
    aas = []
    for j in range(21):
        a = j/20
        aas.append(a)
        derivative = 0
        for b, g in zip(bs, gs):
            bids0 = (a, b, g)
            derivative += derivative_of_payment_of_a(bids0,payment_reference_point, sensitivity)

        derivatives.append(derivative/N)
    plt.plot(aas,derivatives)



def derivative_plot2(payment_reference_point, sensitivity,name, N):
    derivatives = []
    aas = []
    for j in range(21):
        a = j/20
        aas.append(a)
        derivative = 0
        cnt = 0
        for i in range(N):
            b = rnd.uniform(0, 1)
            g = rnd.uniform(0, 2)
            bids = (a, b, g)

            derivative += derivative_of_payment_of_a(bids,payment_reference_point, sensitivity)
            cnt += 1
        derivatives.append(derivative/N)
    plt.title("Expected Derivative " + name)
    plt.ylabel("Expected Derivative")
    plt.xlabel("Value")
    plt.plot(aas,derivatives)
    plt.show()

# rfps = [payment_vcg, payment_zero, payment_shapley_without_seller, payment_shapley_vcg]
# sensitivities= [sensitivity_vcg_of_a, sensitivity_zero_of_a,sensitivity_shapley_without_seller_of_a, sensitivity_shapvcg_of_a]
# derivative_plot2(rfps[0], sensitivities[0], "quadratic", 1000000)