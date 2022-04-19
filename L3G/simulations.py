from valueCreator import *
from L3G.payments import *
from L3G.sensitivities import *
from strategies import *
import matplotlib.pyplot as plt
from functools import reduce # Valid in Python 2.6+, required in Python 3
import operator
import time


def integrated_derivative(payment, sensitivity_of_a, Ns):
    ranges = ((0,1), (0,1), (0,1), (0, 3))
    N = reduce(operator.mul, Ns, 1)
    sum = 0
    for bids in get_random_uniform_values_decimal(ranges, N):
    # for bids in get_perfectly_uniform_values(ranges, Ns):
        sum += derivative_of_payment_of_a(bids,payment, sensitivity_of_a)
    return sum / N

# t = time.time()
# #0.14299955555581587 0.11773333333333333 0.13311104443690977
# # 0.14017895667544503 0.11443333333333333 0.1308784581915718
# # 0.13810653333328124 0.1109264 0.12821008888892133
# Ns = (50, 50, 50, 150)
# Ns = (10000000,)
# x = integrated_derivative(payment_quadratic, sensitivity_vcg_of_a, Ns)
# y = integrated_derivative(payment_proxy, sensitivity_zero_of_a, Ns)
# z = integrated_derivative(create_payment_shapley_nearest(), create_sensitivity_shapley_of_a(), Ns)
# q = integrated_derivative(payment_shapvcg_nearest, create_sensitivity_shapvcg_of_a(), Ns)
# print(x,y,z,q)
#
# print(time.time()-t)

def integrated_derivative_depending_on_a(payment, sensitivity_of_a, Ns):
    N = reduce(operator.mul, Ns, 1)
    ranges = ((0, 1), (0, 1), (0, 3))
    delta = Decimal("0.02")
    aas = [Decimal("0.001")]
    a = Decimal("0.001")
    derivatives = []
    sum = 0
    for b, c, g in get_perfectly_uniform_values(ranges, Ns):
        bids = (a, b, c, g)
        sum += derivative_of_payment_of_a(bids, payment, sensitivity_of_a)
    derivatives.append(sum / N)
    a = delta
    while a <= 1:
        aas.append(a)
        sum = 0
        for b,c,g in get_perfectly_uniform_values(ranges, Ns):
            bids = (a,b,c,g)
            sum += derivative_of_payment_of_a(bids, payment, sensitivity_of_a)
        derivatives.append(sum/N)
        a += delta
    return aas, derivatives

aas, derivs = integrated_derivative_depending_on_a(payment_quadratic, sensitivity_vcg_of_a, (50, 50, 150))
aas1, derivs1 = integrated_derivative_depending_on_a(payment_proxy, sensitivity_zero_of_a, (50, 50, 150))
aas2, derivs2 = integrated_derivative_depending_on_a(payment_shapley_nearest, create_sensitivity_shapley_of_a(), (50, 50, 150))



plt.plot(aas, derivs)
plt.plot(aas1, derivs1)
plt.plot(aas2, derivs2)
plt.legend(["quadratic", "proxy", "shapley"])
plt.savefig("../plots1/L3G integrated derivative depending on bid.txt")
plt.show()


def verifier_tlg(strategy, payment, a):
    Ns = (50, 50, 150)
    ranges = ((0,1), (0,1), (0,3))
    N = Ns[0]*Ns[1]*Ns[2]
    strat_bid_a = strategy(a)
    print(strat_bid_a)
    bid_as = []
    bid_a = Decimal(0)
    delta = Decimal("0.02")
    #bids = get_perfectly_uniform_values(ranges, Ns)
    bids = get_random_uniform_values_decimal(ranges, N)
    total_values = []
    while bid_a < a:
        total_value = 0
        bid_as.append(bid_a)
        for b,c,g in bids:
            bid_b = strategy(b)
            bid_c = strategy(c)
            if g < bid_a + bid_b + bid_c:
                ps = payment((bid_a,bid_b,bid_c,g))
                total_value += a - ps[0]
        total_values.append(total_value/N)
        bid_a += delta
    return bid_as, total_values

# bids, vals = verifier_tlg(tlg_quadratic_bne,payment_quadratic, Decimal("0.4"))
# bids, vals = verifier_tlg(tlg_proxy_bne, payment_proxy, Decimal("0.6"))
# bids, vals = verifier_tlg(tlg_shapley_bne,payment_shapley_nearest, Decimal("0.6"))


# bids, vals = verifier_tlg(truthful,payment_quadratic, Decimal("1.0"))
# plt.plot(bids, vals)
# plt.show()

# utils = []
# a = 1
# bid_as = []
# bid_a = Decimal(0)
# delta = Decimal("0.02")
#
# total_values = []
# while bid_a < a:
#     bid_as.append(bid_a)
#     x = avg_payment(bid_a, truthful, payment_quadratic)
#     win_prob = (1+bid_a)/3
#     total_values.append((1-x)*win_prob)
#     bid_a += delta
# plt.plot(bid_as, total_values)

#print(avg_payment(Decimal("0.95"), truthful, payment_quadratic))